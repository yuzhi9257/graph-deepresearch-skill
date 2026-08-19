# graph-deepresearch

Graph-based deep research with DAG orchestration, fact verification, and source attribution.

## What It Does

Turns complex research questions into structured, source-cited reports using a 5-stage pipeline:

```
Plan → Worker (parallel) → Verify → Merge → Report
```

**Key features:**
- DAG-orchestrated parallel research
- Mandatory fact verification with independent cross-check
- Source attribution on every claim
- Confidence scoring (High/Medium/Low)
- Both Markdown and JSON output

## Installation

```bash
# Using npx skills CLI
npx skills add your-username/graph-deepresearch-skill@graph-deepresearch -g

# Or install manually
git clone https://github.com/your-username/graph-deepresearch-skill.git
cp -r graph-deepresearch ~/.pi/agent/skills/
```

## Prerequisites

- **tavily-search** (primary search tool): `curl -fsSL https://cli.tavily.com/install.sh | bash && tvly login`
- An AI agent that supports SKILL.md files (Pi, Claude Code, Cursor, etc.)

## Quick Start

```
User: Research the current state of AI agents in finance

Agent:
1. Decomposes into sub-questions (regulation, tools, case studies)
2. Searches each independently using tavily
3. Verifies findings in isolated context
4. Merges into unified report
5. Outputs Markdown + JSON with full source chain
```

## Pipeline Stages

### 1. Plan (Decompose)

Break the research topic into 3-5 independent sub-questions.

```yaml
topic: "AI in Finance"
subquestions:
  - id: q1
    question: "What AI tools are banks using?"
    search_queries: ["bank AI tools", "financial AI applications"]
  - id: q2
    question: "How do regulators view AI in trading?"
    search_queries: ["AI trading regulation", "SEC AI guidance"]
```

### 2. Worker (Parallel Research)

Each sub-question gets its own research worker. Workers run in parallel.

**Output per worker:**
```json
{
  "claim": "Banks use AI for fraud detection",
  "source": {
    "url": "https://example.com/article",
    "title": "Article Title",
    "date": "2026-08-19",
    "type": "news",
    "credibility": "medium"
  },
  "confidence": 0.85
}
```

### 3. Verify (Independent Cross-Check)

A separate verifier reviews all findings without seeing other workers' outputs.

**Checks:**
- Source accessibility (does the URL work?)
- Source credibility (is it trustworthy?)
- Claim accuracy (does the source actually say this?)
- Cross-consistency (do sources agree?)

### 4. Merge (Synthesize)

Combine verified findings into a unified view:
- High-confidence facts (multiple sources)
- Medium-confidence facts (single reliable source)
- Uncertain/unverified claims

### 5. Report (Output)

Generate final report in both formats:

**Markdown:** Human-readable report with tables and source links

**JSON:** Machine-readable data for programmatic use

## Output Example

### Markdown

```markdown
# Research Report: AI in Finance

**Date:** 2026-08-19
**Confidence:** High

## Executive Summary
Banks are adopting AI primarily for fraud detection, risk assessment, and customer service...

## Key Findings

### Verified Facts (Multiple Sources)
| # | Fact | Sources | Confidence |
|---|------|---------|------------|
| 1 | JPMorgan uses AI for contract review | [Source 1], [Source 2] | 0.95 |

### High-Confidence Information
| # | Fact | Source | Confidence |
|---|------|--------|------------|
| 1 | AI trading volume increased 40% YoY | [Source](url) | 0.80 |
```

### JSON

```json
{
  "metadata": {
    "topic": "AI in Finance",
    "date": "2026-08-19",
    "confidence_level": "high"
  },
  "findings": {
    "verified": [...],
    "high_confidence": [...],
    "uncertain": [...]
  },
  "sources": [...]
}
```

## Search Tools

| Tool | Priority | Requirements |
|------|----------|--------------|
| tavily-search | Primary | API key (free tier available) |
| web_fetch | Fallback | None |
| LLM Knowledge | Last resort | N/A (staleness warning required) |

## Confidence Levels

| Level | Criteria |
|-------|----------|
| High (0.9+) | Multiple independent high-quality sources |
| Medium (0.7-0.89) | Single reliable source |
| Low (0.5-0.69) | Limited evidence |
| Unverified (<0.5) | Cannot confirm |

## Validation

Validate JSON output:

```bash
python scripts/validate_output.py research_output.json
```

## Project Structure

```
graph-deepresearch/
├── SKILL.md                    # Main skill file
├── README.md                   # This file
├── references/
│   ├── search-strategies.md    # Search tool configurations
│   ├── verification.md         # Fact verification protocol
│   ├── output-formats.md       # Schema definitions
│   └── pitfalls.md             # Common mistakes
├── scripts/
│   └── validate_output.py      # JSON validation
└── examples/
    └── ...                     # Example outputs
```

## When to Use

**Use for:**
- Complex research from multiple angles
- Fact-based analysis with cited sources
- Comparative studies
- Investigative research

**Don't use for:**
- Simple factual lookup (use `tvly search` directly)
- Quick summaries (no deep research needed)
- Opinion-based topics (no facts to verify)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests/examples if applicable
5. Submit a pull request

## License

MIT

## Acknowledgments

Inspired by principles of AI-assisted research:
- Rules before model
- Structure before freedom
- Human before auto
