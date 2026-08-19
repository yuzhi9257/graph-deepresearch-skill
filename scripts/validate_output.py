#!/usr/bin/env python3
"""
Validate graph-deepresearch JSON output against the schema.

Usage:
    python validate_output.py research_output.json
    python validate_output.py research_output.json --fix
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


# Simplified schema validation (no external dependencies)
REQUIRED_TOP_LEVEL = ["metadata", "executive_summary", "findings", "sources"]
REQUIRED_METADATA = ["topic", "date", "pipeline_version", "tools_used"]
REQUIRED_FINDING_KEYS = ["claim", "source", "confidence"]
REQUIRED_SOURCE_KEYS = ["url", "type", "credibility"]
VALID_SOURCE_TYPES = ["official", "academic", "tech_blog", "news", "community", "social", "llm_knowledge"]
VALID_CREDIBILITY = ["high", "medium", "low"]
VALID_CONFIDENCE_LEVELS = ["high", "medium", "low"]


def validate_metadata(metadata: Dict) -> List[str]:
    """Validate metadata section."""
    errors = []
    
    for field in REQUIRED_METADATA:
        if field not in metadata:
            errors.append(f"metadata: missing required field '{field}'")
    
    if "date" in metadata:
        date = metadata["date"]
        if not isinstance(date, str) or len(date) != 10:
            errors.append(f"metadata.date: must be YYYY-MM-DD format, got '{date}'")
    
    if "confidence_level" in metadata:
        if metadata["confidence_level"] not in VALID_CONFIDENCE_LEVELS:
            errors.append(f"metadata.confidence_level: must be one of {VALID_CONFIDENCE_LEVELS}")
    
    if "tools_used" in metadata:
        if not isinstance(metadata["tools_used"], list):
            errors.append("metadata.tools_used: must be a list")
    
    return errors


def validate_source(source: Dict, path: str, allow_empty_url: bool = False) -> List[str]:
    """Validate a single source object."""
    errors = []
    
    # For uncertain findings, URL may be missing
    required_fields = REQUIRED_SOURCE_KEYS if not allow_empty_url else ["type", "credibility"]
    for field in required_fields:
        if field not in source:
            errors.append(f"{path}: missing required field '{field}'")
    
    if "type" in source and source["type"] not in VALID_SOURCE_TYPES:
        errors.append(f"{path}.type: must be one of {VALID_SOURCE_TYPES}")
    
    if "credibility" in source and source["credibility"] not in VALID_CREDIBILITY:
        errors.append(f"{path}.credibility: must be one of {VALID_CREDIBILITY}")
    
    if "url" in source:
        url = source["url"]
        if not url.startswith(("http://", "https://")):
            errors.append(f"{path}.url: must start with http:// or https://")
    
    return errors


def validate_finding(finding: Dict, path: str) -> List[str]:
    """Validate a single finding object."""
    errors = []
    
    for field in REQUIRED_FINDING_KEYS:
        if field not in finding:
            errors.append(f"{path}: missing required field '{field}'")
    
    if "source" in finding:
        # Allow empty URL for uncertain/unverified findings
        allow_empty = finding.get("verification_status") == "needs_verification"
        errors.extend(validate_source(finding["source"], f"{path}.source", allow_empty_url=allow_empty))
    
    if "confidence" in finding:
        conf = finding["confidence"]
        if not isinstance(conf, (int, float)) or conf < 0 or conf > 1:
            errors.append(f"{path}.confidence: must be a number between 0 and 1")
    
    return errors


def validate_findings(findings: Dict) -> List[str]:
    """Validate the findings section."""
    errors = []
    
    required_categories = ["verified", "high_confidence", "uncertain"]
    for cat in required_categories:
        if cat not in findings:
            errors.append(f"findings: missing required category '{cat}'")
        elif not isinstance(findings[cat], list):
            errors.append(f"findings.{cat}: must be a list")
        else:
            for i, finding in enumerate(findings[cat]):
                errors.extend(validate_finding(finding, f"findings.{cat}[{i}]"))
    
    return errors


def validate_sources(sources: List) -> List[str]:
    """Validate the sources section."""
    errors = []
    
    if not isinstance(sources, list):
        errors.append("sources: must be a list")
        return errors
    
    for i, source in enumerate(sources):
        errors.extend(validate_source(source, f"sources[{i}]"))
    
    return errors


def validate_report(data: Dict) -> Tuple[bool, List[str]]:
    """Validate a complete research report."""
    all_errors = []
    
    # Check top-level fields
    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            all_errors.append(f"Missing required top-level field: '{field}'")
    
    # Validate sections
    if "metadata" in data:
        all_errors.extend(validate_metadata(data["metadata"]))
    
    if "findings" in data:
        all_errors.extend(validate_findings(data["findings"]))
    
    if "sources" in data:
        all_errors.extend(validate_sources(data["sources"]))
    
    # Check executive_summary
    if "executive_summary" in data:
        if not isinstance(data["executive_summary"], str):
            all_errors.append("executive_summary: must be a string")
        elif len(data["executive_summary"]) < 10:
            all_errors.append("executive_summary: too short (minimum 10 characters)")
    
    return len(all_errors) == 0, all_errors


def main():
    parser = argparse.ArgumentParser(description="Validate graph-deepresearch JSON output")
    parser.add_argument("file", help="Path to JSON file to validate")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix common issues")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation")
    
    args = parser.parse_args()
    
    # Load file
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {args.file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)
    
    # Validate
    is_valid, errors = validate_report(data)
    
    if is_valid:
        print(f"✅ Validation passed: {args.file}")
        print(f"   Topic: {data.get('metadata', {}).get('topic', 'N/A')}")
        print(f"   Date: {data.get('metadata', {}).get('date', 'N/A')}")
        
        findings = data.get("findings", {})
        verified = len(findings.get("verified", []))
        high_conf = len(findings.get("high_confidence", []))
        uncertain = len(findings.get("uncertain", []))
        print(f"   Findings: {verified} verified, {high_conf} high-confidence, {uncertain} uncertain")
        print(f"   Sources: {len(data.get('sources', []))}")
        
        sys.exit(0)
    else:
        print(f"❌ Validation failed: {args.file}")
        print(f"   Found {len(errors)} error(s):")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
