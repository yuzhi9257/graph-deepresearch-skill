# Verification Protocol

Independent fact verification with cross-checking and source validation.

## Core Principle

**The verifier operates in isolation.** It must NOT see other workers' outputs during verification. This prevents confirmation bias and ensures independent judgment.

## Verification Workflow

```
Findings from Workers
        ↓
┌─────────────────────────┐
│  Verifier Agent         │
│  (independent context)  │
│                         │
│  1. Check each finding  │
│  2. Validate sources    │
│  3. Cross-reference     │
│  4. Flag issues         │
└─────────────────────────┘
        ↓
Verification Report
```

## Verification Checks

### 1. Source Accessibility

**Question:** Does this URL actually exist and load?

**Procedure:**
```bash
# Verify URL is accessible
curl -s -o /dev/null -w "%{http_code}" "https://example.com/article"
# Should return 200
```

**Common issues:**
- 404: Source removed or URL changed
- 403: Access restricted (may still be valid)
- Timeout: Site down, try again later
- Redirect: Check final destination

### 2. Source Credibility

**Question:** Is this source trustworthy?

**Credibility matrix:**

| Type | Credibility | Notes |
|------|-------------|-------|
| Official docs | High | Company's own documentation |
| SEC/regulatory filings | High | Legal obligation for accuracy |
| Academic papers | High | Peer-reviewed |
| Established news | Medium-High | Editorial standards |
| Tech blogs (reputable) | Medium | Author expertise varies |
| Community forums | Medium-Low | Consensus matters |
| Social media | Low | Sentiment only |

**Red flags:**
- Anonymous author
- No publication date
- Sensationalist headlines
- No other sources citing it
- Domain recently created

### 3. Claim Accuracy

**Question:** Does the source actually say what's claimed?

**Procedure:**
1. Read the source content (not just the snippet)
2. Find the specific passage supporting the claim
3. Check for context manipulation
4. Verify direct quotes are accurate

**Example verification:**
```json
{
  "claim": "PAT has hundreds of daily users",
  "source_url": "https://wallstreetcn.com/articles/3778014",
  "verification": {
    "found_in_source": true,
    "exact_quote": "数百名投资人日常使用",
    "context_accurate": true,
    "note": "Matches claim, but source is a translation, not original"
  }
}
```

### 4. Temporal Validity

**Question:** Is this information still current?

**Checks:**
- Publication date vs current date
- Whether topic is time-sensitive
- Whether superseded by newer information
- Whether claim has an expiration

**Freshness rules:**
| Topic Type | Max Age | Action if Older |
|------------|---------|-----------------|
| Technology | 1 year | Verify still current |
| Market data | 1 quarter | Mark as potentially outdated |
| Personnel | 6 months | Verify still in role |
| Regulations | 1 year | Verify not superseded |
| Historical facts | No limit | Accept as-is |

### 5. Cross-Consistency

**Question:** Do multiple sources agree?

**Procedure:**
1. Group claims on the same topic
2. Compare claims across sources
3. Note agreements and contradictions
4. Assess which version is more credible

**Cross-reference matrix:**
```json
{
  "topic": "PAT user count",
  "sources": [
    {"claim": "hundreds of users", "credibility": "high", "type": "official"},
    {"claim": "500+ users", "credibility": "medium", "type": "media"},
    {"claim": "thousands of users", "credibility": "low", "type": "social"}
  ],
  "consensus": "hundreds",
  "confidence": 0.85,
  "note": "Official source says 'hundreds', social media exaggerates"
}
```

### 6. Completeness

**Question:** Are important perspectives missing?

**Checks:**
- Are there counter-arguments?
- Are there alternative explanations?
- Are there limitations acknowledged?
- Is the source balanced or one-sided?

## Verifier Output Schema

```json
{
  "verification_id": "v_20260819_001",
  "findings_reviewed": 15,
  "verification_result": "PASS|PASS_WITH_CAVEATS|FAIL",
  
  "detailed_results": [
    {
      "finding_id": "q1_f3",
      "claim": "Original claim text",
      "checks": {
        "source_accessible": true,
        "source_credible": true,
        "claim_accurate": true,
        "temporally_valid": true,
        "cross_consistent": true,
        "complete": false
      },
      "issues_found": [
        {
          "type": "completeness",
          "severity": "medium",
          "description": "Missing counter-argument from competitor perspective",
          "recommendation": "Add opposing viewpoint"
        }
      ],
      "adjusted_confidence": 0.85
    }
  ],
  
  "cross_references": [
    {
      "topic": "User adoption metrics",
      "claims": ["q1_f1", "q3_f2", "q3_f5"],
      "status": "consistent",
      "consensus": "Hundreds of daily users",
      "confidence_boost": 0.1
    }
  ],
  
  "missing_sources": [
    {
      "claim": "Specific adoption numbers",
      "reason": "Only one source, needs corroboration",
      "recommendation": "Search for additional sources"
    }
  ],
  
  "summary": {
    "total_verified": 12,
    "total_issues": 3,
    "high_severity": 0,
    "medium_severity": 2,
    "low_severity": 1
  }
}
```

## Issue Severity Levels

| Level | Definition | Action |
|-------|------------|--------|
| **High** | Fact is wrong or source doesn't exist | Must fix before publishing |
| **Medium** | Source is weak or context is misleading | Should fix, note in report |
| **Low** | Minor incompleteness or formatting | Can note, not blocking |

## Confidence Adjustment Rules

Apply these modifiers based on verification results:

| Condition | Modifier |
|-----------|----------|
| Cross-referenced by 3+ sources | +0.15 |
| Cross-referenced by 2 sources | +0.10 |
| Single high-credibility source | +0.05 |
| Single medium-credibility source | 0 |
| Single low-credibility source | -0.10 |
| Source inaccessible | -0.20 |
| Claim not found in source | -0.30 |
| Contradicted by other sources | -0.25 |
| Temporally outdated | -0.15 to -0.30 |

## Verification Report Template

```markdown
## Verification Report

**Date:** YYYY-MM-DD
**Findings Reviewed:** [N]
**Result:** PASS / PASS_WITH_CAVEATS / FAIL

### Issues Found

| # | Finding | Issue | Severity | Fix |
|---|---------|-------|----------|-----|
| 1 | [claim] | [issue] | [level] | [action] |

### Cross-References

| Topic | Sources | Status | Confidence |
|-------|---------|--------|------------|
| [topic] | [list] | consistent/contradictory | [score] |

### Missing Sources

| Claim | Reason | Recommendation |
|-------|--------|----------------|
| [claim] | [why] | [what to do] |

### Summary

- Verified: [N] findings
- Issues: [N] ([H] high, [M] medium, [L] low)
- Overall: [PASS/CAVEATS/FAIL]
```
