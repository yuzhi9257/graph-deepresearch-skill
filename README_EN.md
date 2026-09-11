# graph-deepresearch-skill

[中文](README.md)

Graph-based deep research skill: DAG orchestration, parallel investigation, independent fact verification, adversarial review, and full source attribution. Follows the open [Agent Skills](https://agentskills.io) spec and works with Claude Code, Codex, Cursor, ZCode, and 20+ other clients.

## Skills

### [graph-deepresearch](SKILL.md) 🔍

Decomposes a complex research topic into independent sub-questions, dispatches parallel subagent workers to investigate, then has every claim independently verified by a fact-checker and challenged by an adversarial reviewer. Produces structured reports (Markdown + JSON) with cited sources and confidence levels.

**Use when:**

- "Research X in depth"
- "Investigate Y from multiple angles"
- "Fact-check this claim for me"
- "Compare A vs B and give me a report with sources"

## Pipeline

```
Plan → Worker (parallel) → Verify + Adversarial → Merge → Report
```

- Each sub-question is researched by its own subagent worker, all in parallel
- Every claim passes both a verifier (confirm) and an adversarial agent (disprove), isolated from each other
- Decision-support topics optionally run principle-based reasoning: facts → multi-scenario projections (optimistic / base / pessimistic)
- Every claim carries a source URL, credibility rating, and confidence score

## Install

One command via the [skills CLI](https://skills.sh/):

```bash
npx skills add yuzhi9257/graph-deepresearch-skill
```

Or symlink manually into your agent's skills directory:

```bash
git clone https://github.com/yuzhi9257/graph-deepresearch-skill.git
ln -s "$(pwd)/graph-deepresearch-skill" ~/.agents/skills/graph-deepresearch
```

## Prerequisites

Research workers use Tavily search by default (free tier available):

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash && tvly login
```

When Tavily is unavailable the pipeline falls back to web_fetch, then to LLM knowledge with mandatory staleness warnings.

## Output Validation

```bash
python scripts/validate_output.py research_output.json
```

## Structure

```
├── SKILL.md
├── references/
│   ├── search-strategies.md
│   ├── verification.md
│   ├── output-formats.md
│   └── pitfalls.md
└── scripts/
    └── validate_output.py
```

## License

[MIT](LICENSE)
