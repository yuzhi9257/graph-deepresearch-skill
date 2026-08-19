# Output Formats

Schema definitions for Markdown reports and JSON data outputs.

## File Naming Convention

```
research_{topic_slug}_{YYYYMMDD}.md
research_{topic_slug}_{YYYYMMDD}.json
```

Example:
```
research_ai_finance_agents_20260819.md
research_ai_finance_agents_20260819.json
```

## Markdown Report Schema

```markdown
# Research Report: [Topic Title]

**Date:** YYYY-MM-DD
**Confidence:** High / Medium / Low
**Pipeline Version:** 1.0.0
**Researcher:** AI Agent (graph-deepresearch)

---

## Executive Summary

[2-3 sentences summarizing the most important findings. Written for someone who will only read this section.]

---

## Key Findings

### Verified Facts (Multiple Sources)

Claims confirmed by 2+ independent credible sources.

| # | Fact | Sources | Confidence |
|---|------|---------|------------|
| 1 | [Fact statement] | [Source 1], [Source 2] | 0.95 |

### High-Confidence Information (Single Reliable Source)

Claims from one credible source that couldn't be independently corroborated.

| # | Fact | Source | Confidence |
|---|------|--------|------------|
| 1 | [Fact statement] | [Source](url) | 0.80 |

### Uncertain / Unverified

Claims that couldn't be fully verified or require further research.

| # | Information | Reason | Recommendation |
|---|-------------|--------|----------------|
| 1 | [Claim] | Insufficient sources | Search for additional evidence |

---

## Contradictions & Controversies

[Document any conflicting findings between sources. If none, state "No contradictions found."]

### Contradiction 1: [Topic]

| Source A | Source B | Assessment |
|----------|----------|------------|
| [Claim from A] | [Claim from B] | [Which is more credible and why] |

---

## Source List

All sources used, sorted by credibility.

### Official Sources
1. **[Title](URL)** — Publication Date
   - Type: Official documentation / Press release / SEC filing
   - Credibility: High

### Academic Sources
1. **[Title](URL)** — Publication Date
   - Type: Journal paper / Conference paper / Preprint
   - Credibility: High

### News Sources
1. **[Title](URL)** — Publication Date
   - Type: News article / Analysis
   - Credibility: Medium-High

### Tech Blogs
1. **[Title](URL)** — Publication Date
   - Type: Tutorial / Analysis / Opinion
   - Credibility: Medium

### Community Sources
1. **[Title](URL)** — Publication Date
   - Type: Forum discussion / Blog post
   - Credibility: Medium-Low

---

## Methodology

### Research Parameters
- **Topic:** [Main research question]
- **Time range:** [Date range of sources]
- **Sources consulted:** [Total number]
- **Search tools:** tavily-search, web_fetch

### Search Queries Used
1. "[query 1]" — [N results]
2. "[query 2]" — [N results]
3. "[query 3]" — [N results]

### Limitations
- [What was not covered]
- [What sources were unavailable]
- [What time constraints existed]

---

## Confidence Assessment

| Category | Count | Avg Confidence | Notes |
|----------|-------|----------------|-------|
| Verified Facts | X | 0.95 | Multiple sources |
| High-Confidence | X | 0.80 | Single source |
| Uncertain | X | N/A | Needs verification |
| **Total** | **X** | **0.XX** | |

---

## Appendix: Research Process

### Stage 1: Plan
Decomposed into [N] sub-questions:
1. [Sub-question 1]
2. [Sub-question 2]
3. [Sub-question 3]

### Stage 2: Worker Results
[N] workers completed, [N] findings extracted.

### Stage 3: Verification
[N] findings verified, [N] issues found.

### Stage 4: Merge
Synthesized into unified view.

### Stage 5: Report
Generated Markdown and JSON outputs.
```

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Graph Deep Research Output",
  "type": "object",
  "required": ["metadata", "executive_summary", "findings", "sources"],
  
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["topic", "date", "pipeline_version", "tools_used"],
      "properties": {
        "topic": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "pipeline_version": {"type": "string"},
        "confidence_level": {"type": "string", "enum": ["high", "medium", "low"]},
        "tools_used": {
          "type": "array",
          "items": {"type": "string"}
        },
        "search_queries": {
          "type": "array",
          "items": {"type": "string"}
        },
        "sources_consulted": {"type": "integer"}
      }
    },
    
    "executive_summary": {"type": "string"},
    
    "findings": {
      "type": "object",
      "required": ["verified", "high_confidence", "uncertain"],
      "properties": {
        "verified": {
          "type": "array",
          "items": {"$ref": "#/definitions/finding"}
        },
        "high_confidence": {
          "type": "array",
          "items": {"$ref": "#/definitions/finding"}
        },
        "uncertain": {
          "type": "array",
          "items": {"$ref": "#/definitions/finding"}
        }
      }
    },
    
    "contradictions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "topic": {"type": "string"},
          "source_a": {"type": "object"},
          "source_b": {"type": "object"},
          "assessment": {"type": "string"}
        }
      }
    },
    
    "sources": {
      "type": "array",
      "items": {"$ref": "#/definitions/source"}
    },
    
    "methodology": {
      "type": "object",
      "properties": {
        "time_range": {"type": "string"},
        "limitations": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    
    "confidence_assessment": {
      "type": "object",
      "properties": {
        "verified_count": {"type": "integer"},
        "high_confidence_count": {"type": "integer"},
        "uncertain_count": {"type": "integer"},
        "average_confidence": {"type": "number"}
      }
    },
    
    "verification_report": {"$ref": "#/definitions/verification"}
  },
  
  "definitions": {
    "finding": {
      "type": "object",
      "required": ["claim", "source", "confidence"],
      "properties": {
        "id": {"type": "string"},
        "claim": {"type": "string"},
        "source": {"$ref": "#/definitions/source"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence": {"type": "string"},
        "verification_status": {
          "type": "string",
          "enum": ["verified", "needs_verification", "unverified"]
        }
      }
    },
    
    "source": {
      "type": "object",
      "required": ["url", "type", "credibility"],
      "properties": {
        "url": {"type": "string", "format": "uri"},
        "title": {"type": "string"},
        "date": {"type": "string"},
        "type": {
          "type": "string",
          "enum": ["official", "academic", "tech_blog", "news", "community", "social", "llm_knowledge"]
        },
        "credibility": {
          "type": "string",
          "enum": ["high", "medium", "low"]
        }
      }
    },
    
    "verification": {
      "type": "object",
      "properties": {
        "result": {
          "type": "string",
          "enum": ["PASS", "PASS_WITH_CAVEATS", "FAIL"]
        },
        "findings_reviewed": {"type": "integer"},
        "issues_found": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "finding_id": {"type": "string"},
              "issue": {"type": "string"},
              "severity": {"type": "string", "enum": ["high", "medium", "low"]},
              "recommendation": {"type": "string"}
            }
          }
        }
      }
    }
  }
}
```

## Example JSON Output

```json
{
  "metadata": {
    "topic": "AI Agent Applications in Finance",
    "date": "2026-08-19",
    "pipeline_version": "1.0.0",
    "confidence_level": "high",
    "tools_used": ["tavily-search", "web_fetch"],
    "search_queries": [
      "AI agent finance official",
      "AI agent architecture patterns",
      "hedge fund AI comparison"
    ],
    "sources_consulted": 15
  },
  
  "executive_summary": "Major financial institutions are deploying AI agents built on dual-agent architectures for research and analysis workflows. These systems combine conversational interfaces with coding capabilities to automate complex financial analysis tasks.",
  
  "findings": {
    "verified": [
      {
        "id": "q1_f1",
        "claim": "Multiple financial firms presented AI agent systems at major tech conferences in 2026",
        "source": {
          "url": "https://www.youtube.com/watch?v=example",
          "title": "AI Agents in Finance Conference Talk",
          "date": "2026-08-16",
          "type": "official",
          "credibility": "high"
        },
        "confidence": 0.95,
        "evidence": "Direct video of official presentation"
      }
    ],
    "high_confidence": [
      {
        "id": "q1_f2",
        "claim": "Internal AI tools have hundreds of daily users across financial institutions",
        "source": {
          "url": "https://techcrunch.com/example",
          "title": "Financial AI Adoption Report",
          "date": "2026-08-17",
          "type": "news",
          "credibility": "medium"
        },
        "confidence": 0.80,
        "evidence": "Industry analysis and adoption metrics"
      }
    ],
    "uncertain": [
      {
        "id": "q2_f1",
        "claim": "New AI agent frameworks achieve 4x speed improvement",
        "source": {
          "type": "social",
          "credibility": "low"
        },
        "confidence": 0.40,
        "verification_status": "needs_verification"
      }
    ]
  },
  
  "contradictions": [],
  
  "sources": [
    {
      "url": "https://www.youtube.com/watch?v=example",
      "title": "AI Agents in Finance Conference Talk",
      "date": "2026-08-16",
      "type": "official",
      "credibility": "high"
    }
  ],
  
  "methodology": {
    "time_range": "2026-08-01 to 2026-08-19",
    "limitations": [
      "Primary sources limited to English-language official presentations",
      "Chinese translations may introduce interpretation errors"
    ]
  },
  
  "confidence_assessment": {
    "verified_count": 5,
    "high_confidence_count": 8,
    "uncertain_count": 2,
    "average_confidence": 0.82
  }
}
```
