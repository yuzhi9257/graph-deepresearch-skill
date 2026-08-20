---
name: graph-deepresearch
description: |
  Graph-based deep research with DAG orchestration, fact verification, and source attribution.
  Use when the user asks to research a complex topic, investigate a subject deeply, conduct
  multi-angle analysis, or says "research X", "investigate Y", "deep dive into Z", "look into
  W thoroughly", or needs fact-based analysis with cited sources. Produces structured reports
  with verified facts, confidence levels, and complete source chains.
  Triggers: deep research, investigate, research topic, fact-based analysis, source-cited report,
  multi-source research, comprehensive analysis, thorough investigation.
---

# Graph Deep Research

DAG-orchestrated deep research with mandatory fact verification and source attribution.

**Architecture: 1 main agent + N worker subagents + 1 verifier subagent**

The main agent owns planning, coordination, and final synthesis. Research workers and
the verifier are dispatched as parallel subagents with isolated contexts. This is not
optional — the pipeline **requires** subagent dispatch for parallel workers and
independent verification.

## Core Principles

1. **Rules before model** — Follow the pipeline structure, don't improvise
2. **Structure before freedom** — DAG plan first, then execute
3. **Human before auto** — Final report requires human review
4. **Sources on every fact** — No claim without a URL + date + credibility rating
5. **Parallel by default** — Workers run as concurrent subagents, not sequential steps
6. **Verify independently** — Verifier subagent sees only one finding at a time, never other workers' outputs

## When to Use

### ✅ Use this skill when

The user's request involves **multi-source, fact-based research that benefits from parallel investigation and independent verification.**

| Trigger | Example phrases |
|---------|------------------|
| Multi-angle research | "Research X from multiple perspectives", "Deep dive into Y", "Investigate Z thoroughly" |
| Fact-based analysis | "What's the current state of X?", "Is it true that Y?", "Fact-check this claim" |
| Comparative study | "Compare A vs B vs C", "What are the pros and cons of X?", "Evaluate options for Y" |
| Investigative research | "Look into the X controversy", "What really happened with Y?", "Dig into Z" |
| Decision support | "Should we adopt X?", "What are the risks of Y?", "Help me evaluate Z" |
| Source-cited reporting | "Give me a research report on X with sources", "Cite your sources for Y" |

**Rule of thumb:** If the answer requires consulting 3+ independent sources and synthesizing them, use this skill. If it can be answered from one source, use a simpler tool.

### ❌ Do NOT use when

| Scenario | Why not | Use instead |
|----------|---------|-------------|
| Simple factual lookup | One search answers it, pipeline is overkill | `tvly search "X"` directly |
| Quick summary needed | User wants speed, not depth | Direct LLM response or single search |
| Pure opinion/brainstorming | No facts to verify, no sources to cite | General conversation |
| Code debugging / technical help | Not a research task | Use coding skills |
| Real-time data (stock prices, live scores) | Sources change by the minute, pipeline is too slow | Direct API call |
| Personal advice (medical, legal, financial) | Research skill is not a professional advisor | Consult a professional |
| Topic has < 3 searchable angles | Too narrow for DAG decomposition | Single search + LLM synthesis |
| User wants a 1-paragraph answer | Report format is overkill | Direct response |
| Creative writing / fiction | No facts to verify | General LLM |
| Historical consensus (well-established facts) | No need for multi-source verification | Direct LLM response |

### Decision Flowchart

```
User request arrives
    │
    ├── Can it be answered with 1 search? ──Yes──→ Use tvly search directly
    │
    ├── Does it need multiple sources? ──No──→ Direct LLM response
    │
    ├── Are there facts to verify? ──No──→ Not a research task
    │
    ├── Is it real-time data? ──Yes──→ Use API, not this pipeline
    │
    └── None of the above ──→ USE THIS SKILL
```

---

## The 5-Stage Pipeline

### Stage 1: Plan (Decompose) — Main Agent Only

Decompose the research topic into 3-5 independent sub-questions.

**Rules:**
- Each sub-question must be independently researchable (no dependencies between them)
- If B requires A's results to answer, the decomposition is not deep enough
- Aim for 3-5 sub-questions (fewer = too broad, more = too fragmented)

**Output format (YAML):**

```yaml
topic: "Main research question"
subquestions:
  - id: q1
    question: "Sub-question 1"
    search_queries:
      - "query term 1"
      - "query term 2"
    sources_priority: [official, academic, news]
  - id: q2
    question: "Sub-question 2"
    search_queries:
      - "query term 1"
    sources_priority: [official, tech_blog, news]
```

**Source priority levels:**
1. `official` — Company/org websites, official documentation
2. `academic` — Peer-reviewed papers, university research
3. `tech_blog` — Reputable technical blogs (Medium, Dev.to, etc.)
4. `news` — Established news outlets (Reuters, Bloomberg, etc.)
5. `community` — Reddit, HN, forums (use with caution)
6. `social` — Twitter, Weibo (lowest weight, sentiment only)

---

### Stage 1.5: Determine Research Type & Ask About Principles

After decomposing the topic, the main agent must decide: **is this fact-finding or decision-support?**

**Decision rule:**
- If the user's request implies a choice, strategy, evaluation, or recommendation → **decision-support**
- If the user just wants to know the current state of something → **fact-finding**

| User says | Type |
|-----------|------|
| "Research what AI tools banks are using" | fact-finding |
| "Should we adopt AI agents for our workflow?" | decision-support |
| "Compare LangGraph vs CrewAI" | decision-support |
| "What's the market size for X?" | fact-finding |
| "Should we invest in X?" | decision-support |

#### If fact-finding → skip to Stage 2, no principles needed.

#### If decision-support → ask the user about principles:

```
我发现这是一个需要决策判断的研究课题。为了让研究不仅停留在"事实是什么"，
而是进一步推演出"基于事实，可能的未来走向是什么"，我需要一个原则库。

📌 什么是原则库？
原则库是你积累的因果规则——"当 X 发生时，Y 通常会跟上"。
比如："当新技术渗透率 < 15% 时，监管通常滞后 12-18 个月"。
顶级投资机构用了数十年才沉淀出他们的原则库。

📁 你有原则库吗？
- 有 → 请提供文件路径或直接贴出来，我会读取并用于推演
- 没有 → 我会使用公认分析框架作为替代：
  • SWOT 分析（优势/劣势/机会/威胁）
  • Porter 五力模型
  • PESTEL 宏观环境分析
  • 技术成熟度曲线（Gartner Hype Cycle）
  • 跨行业历史类比（从类似案例推演）
  • 不确定性矩阵（概率 × 影响）
- 不确定 → 告诉我你的领域，我推荐合适的框架

请选择（1=有原则库 / 2=用公认框架 / 3=推荐框架）：
```

**User response handling:**

| Response | Action |
|----------|--------|
| Provides a file path | Read the file, extract principles, use for Stage 3 reasoning |
| Provides inline text | Parse as principles, use for Stage 3 reasoning |
| "2" or "用公认框架" | Load built-in framework set (SWOT, Porter, PESTEL, etc.) |
| "3" or "推荐框架" | Ask user's domain, recommend 2-3 most relevant frameworks, then load |
| Skips / says no | Skip principle-matching entirely, proceed with fact-finding pipeline |

The principles/frameworks will be used in Stage 3 (Reasoning Agent) to produce multi-scenario projections.

---

### Stage 2: Worker (Parallel Research) — SUBAGENT DISPATCH REQUIRED

**⚠️ CRITICAL: You MUST use the `subagent` tool with `parallel` mode to dispatch workers.**

Each sub-question gets its own subagent worker. All workers run concurrently.
Do NOT run workers sequentially. Do NOT do the research yourself.

#### Dispatch Procedure

After completing Stage 1, dispatch all workers in a single `subagent` call:

```
subagent({
  tasks: [
    {
      agent: "default",
      task: "You are a research worker. Your job: research sub-question q1.\n\nSub-question: {question text}\nSearch queries: {queries}\nSource priority: {priorities}\n\nProcedure:\n1. Run: tvly search \"{query}\" --depth advanced --max-results 5 --json  for each query\n2. Extract key facts from results\n3. Attach source (url, title, date, type, credibility) to every fact\n4. Rate confidence (0.0-1.0)\n5. Output ONLY valid JSON in this exact format:\n{worker_output_schema}\n\nRules:\n- Do NOT include findings from other sub-questions\n- Do NOT speculate or use LLM knowledge — only cite sources you actually found\n- If a search returns nothing useful, say so explicitly"
    },
    {
      agent: "default",
      task: "You are a research worker. Your job: research sub-question q2.\n\n...(same structure)..."
    }
  ]
})
```

#### Worker Output Schema

Each worker subagent MUST return valid JSON matching this schema:

```json
{
  "subquestion_id": "q1",
  "subquestion": "Original question text",
  "findings": [
    {
      "claim": "Specific factual claim",
      "source": {
        "url": "https://example.com/article",
        "title": "Article Title",
        "date": "2026-08-19",
        "type": "official|academic|tech_blog|news|community|social",
        "credibility": "high|medium|low"
      },
      "confidence": 0.95,
      "evidence": "Direct quote or paraphrase from source"
    }
  ],
  "uncertainties": [
    "List of claims that could not be fully verified"
  ]
}
```

**Confidence levels:**
- **High (0.9+)**: Multiple independent high-quality sources confirm
- **Medium (0.7-0.89)**: Single reliable source, or multiple lower-credibility sources
- **Low (0.5-0.69)**: Limited evidence, requires further verification
- **Unverified (<0.5)**: Cannot confirm, mark as uncertain

### Stage 3: Verify & Adversarial Review — SUBAGENT DISPATCH REQUIRED

**⚠️ CRITICAL: You MUST dispatch TWO independent subagent types per finding:
1. Verifier — confirms the claim is factually correct
2. Adversarial Agent — actively seeks counter-evidence and opposing viewpoints**

Both operate in isolated contexts. Neither sees the other's output or other workers' results.
对抗审查 Agent 必须设，对抗幻觉与确认偏误。

#### 3a. Dispatch Verifier (Fact Check)

After collecting all worker results, dispatch one verifier subagent per finding:

```
subagent({
  agent: "default",
  task: "You are an independent fact verifier. Verify the following claim.\n\nClaim: {claim text}\nSource URL: {url}\nSource title: {title}\nClaimed confidence: {confidence}\n\nVerification steps:\n1. Run: tvly search \"{exact claim}\" --depth basic --max-results 3 --json\n2. Check: Does the source URL actually exist? Is it accessible?\n3. Check: Does the source actually say what's claimed?\n4. Check: Is the source credible (official, academic, news)?\n5. Check: Is it current (within last 6 months)?\n6. Check: Do other sources corroborate this?\n\nOutput ONLY valid JSON:\n{\n  \"finding_id\": \"{id}\",\n  \"role\": \"verifier\",\n  \"result\": \"PASS|PASS_WITH_CAVEATS|FAIL\",\n  \"issues\": [],\n  \"revised_confidence\": 0.85,\n  \"reasoning\": \"...\"\n}\n\nRules:\n- Be skeptical. Default assumption: claims may be wrong until verified.\n- If the URL is dead, mark FAIL.\n- If the source says something different from the claim, mark FAIL.\n- If you cannot access the source, mark PASS_WITH_CAVEATS."
})
```

#### 3b. Dispatch Adversarial Agent (Counter-Evidence Search)

**In parallel with the verifier**, dispatch an adversarial agent that actively tries to
**disprove** the claim. This agent's job is NOT to confirm — it's to find holes.

```
subagent({
  agent: "default",
  task: "You are an adversarial fact-checker. Your job is to find counter-evidence AGAINST the following claim. You are the skeptic.\n\nClaim: {claim text}\nSource URL: {url}\nOriginal confidence: {confidence}\n\nAdversarial procedure:\n1. Run: tvly search \"{claim} false OR incorrect OR debunked OR counter\" --depth advanced --max-results 5 --json\n2. Run: tvly search \"{opposite/contrarian angle}\" --depth basic --max-results 3 --json\n3. Search for: known failures, exceptions, edge cases, criticisms, controversies\n4. Search for: more recent information that might contradict this claim\n5. Search for: expert opinions that disagree\n\nOutput ONLY valid JSON:\n{\n  \"finding_id\": \"{id}\",\n  \"role\": \"adversarial\",\n  \"counter_evidence_found\": true|false,\n  \"counters\": [\n    {\n      \"type\": \"direct_contradiction|partial_contradiction|missing_context|edge_case|outdated|misleading|debunked\",\n      \"claim_against\": \"What the counter-evidence says\",\n      \"source\": {\n        \"url\": \"...\",\n        \"title\": \"...\",\n        \"credibility\": \"high|medium|low\"\n      },\n      \"severity\": \"critical|significant|minor\",\n      \"note\": \"How this undermines the original claim\"\n    }\n  ],\n  \"missing_perspectives\": [\n    \"Important viewpoints or data NOT represented in the original finding\"\n  ],\n  \"confidence_adjustment\": -0.15,\n  \"reasoning\": \"Found X contradicting sources...\"\n}\n\nRules:\n- Your job is to DISPROVE, not confirm. Be aggressive.\n- Search for the opposite claim, not the same claim.\n- Look for critics, dissenters, failed cases, exceptions.\n- If you find nothing against it, say so honestly — don't fabricate counters.\n- Severity: critical = completely invalidates claim, significant = weakens it, minor = adds nuance."
})
```

#### 3c. Combine Results (Main Agent)

After both subagents return, the main agent combines their outputs:

| Verifier Result | Adversarial Result | Final Disposition |
|-----------------|-------------------|-------------------|
| PASS | No counter-evidence | ✅ **Verified** — keep original confidence |
| PASS | Minor counters | ✅ **Verified with caveats** — note the nuances |
| PASS_WITH_CAVEATS | Significant counters | ⚠️ **Contested** — move to Uncertain, note both sides |
| PASS_WITH_CAVEATS | No counter-evidence | ⚠️ **Verified with caveats** — keep with notes |
| FAIL | Any | ❌ **Rejected** — move to Uncertain, explain failure |
| Any | Critical counter | ❌ **Contested** — move to Uncertain, present both views |

Apply confidence adjustment from adversarial agent:
```
final_confidence = verifier.revised_confidence + adversarial.confidence_adjustment
```

#### Verification Checklist

| Check | Question | Failure = |
|-------|----------|-----------|
| Source accessibility | Does this URL actually work? | FAIL |
| Source credibility | Is this official or a secondary interpretation? | PASS_WITH_CAVEATS |
| Claim accuracy | Does the source actually say what's claimed? | FAIL |
| Temporal validity | Was this published recently enough to be relevant? | PASS_WITH_CAVEATS |
| Cross-consistency | Do multiple sources agree? | PASS_WITH_CAVEATS |
| **Adversarial: contradiction** | **Did the adversarial agent find direct contradictions?** | **Contested** |
| **Adversarial: missing context** | **Are important perspectives missing?** | **Contested** |

#### Combined Output Schema

```json
{
  "finding_id": "q1_f3",
  "verification": {
    "result": "PASS|PASS_WITH_CAVEATS|FAIL",
    "issues": [],
    "revised_confidence": 0.85,
    "reasoning": "..."
  },
  "adversarial": {
    "counter_evidence_found": true,
    "counters": [
      {
        "type": "partial_contradiction",
        "claim_against": "Some sources report lower numbers",
        "source": { "url": "...", "credibility": "medium" },
        "severity": "significant",
        "note": "Original claim cites upper bound without noting variance"
      }
    ],
    "missing_perspectives": ["Industry critics argue..."],
    "confidence_adjustment": -0.10
  },
  "final_disposition": "verified_with_caveats",
  "final_confidence": 0.75
}
```

---

### Stage 3.5: Principle-Matching Reasoning (Conditional) — SUBAGENT DISPATCH REQUIRED

**This stage ONLY runs when Stage 1.5 determined this is decision-support AND the user provided principles or chose built-in frameworks.**

Skip this stage entirely for fact-finding research.

#### Input

The main agent collects:
1. All verified findings from Stage 3 (final_disposition = verified or verified_with_caveats only)
2. The user's principles (from file or inline), OR the built-in framework set

#### 3.5a. Dispatch Reasoning Agent

Dispatch one reasoning subagent with the verified facts + principles/frameworks:

```
subagent({
  agent: "default",
  task: "You are a strategic reasoning agent. Your job: take verified facts and run them through a principles library to produce multi-scenario projections.\n\n## Verified Facts\n{JSON array of verified findings from Stage 3}\n\n## Principles Library\n{user-provided principles OR built-in frameworks}\n\n## Procedure\n1. For each major finding, identify which principles/frameworks apply\n2. For each applicable principle, derive a scenario projection:\n   - Optimistic scenario (best case + trigger conditions)\n   - Base scenario (most likely + trigger conditions)\n   - Pessimistic scenario (worst case + trigger conditions)\n   - Each scenario gets a probability estimate and supporting reasoning\n3. Identify cross-cutting themes: which findings compound or contradict each other\n4. Flag any principle that has NO matching fact (the principle is irrelevant to this topic)\n5. Flag any finding that has NO matching principle (unprecedented, no precedent to reason from)\n\n## Output Schema (valid JSON only)\n{\n  \"topic\": \"...\",\n  \"reasoning_type\": \"principles|frameworks\",\n  \"scenario_projections\": [\n    {\n      \"scenario\": \"optimistic|base|pessimistic\",\n      \"probability\": 0.35,\n      \"description\": \"What this scenario looks like\",\n      \"trigger_conditions\": [\"What must be true for this scenario\"],\n      \"supporting_facts\": [\"finding_id_1\", \"finding_id_2\"],\n      \"applicable_principles\": [\"principle_id or framework name\"]\n    }\n  ],\n  \"cross_cutting_themes\": [\n    {\n      \"theme\": \"...\",\n      \"related_findings\": [\"q1_f1\", \"q2_f3\"],\n      \"implication\": \"...\"\n    }\n  ],\n  \"unprecedented_findings\": [\n    {\n      \"finding_id\": \"q3_f2\",\n      \"reason\": \"No historical precedent or applicable principle found\",\n      \"risk_level\": \"high|medium|low\"\n    }\n  ],\n  \"irrelevant_principles\": [\n    {\n      \"principle\": \"...\",\n      \"reason\": \"No matching facts in this research\"\n    }\n  ]\n}\n\n## Rules\n- Never invent facts. Only reason from verified findings provided.\n- Never assign probability > 50% to any single scenario (if you think one is > 50%, split it into sub-scenarios).\n- Always provide trigger conditions for each scenario.\n- If a principle conflicts with facts, note the conflict — don't ignore the principle or the fact.\n- For built-in frameworks (SWOT/Porter/etc.), apply them systematically, not just mention them."
})
```

#### 3.5b. Adversarial Review of Reasoning (Optional but Recommended)

Dispatch an adversarial agent to challenge the reasoning output:

```
subagent({
  agent: "default",
  task: "You are an adversarial reasoning reviewer. Challenge the following scenario projections.\n\nScenario Projections:\n{reasoning agent output}\n\nOriginal Verified Facts:\n{facts}\n\nYour job:\n1. Are the probabilities realistic? Do they sum to ~100%?\n2. Are trigger conditions specific enough to be testable?\n3. Are there obvious scenarios that were missed?\n4. Are the supporting facts actually relevant to each scenario?\n5. Does any scenario rest on a single low-confidence finding?\n6. Is this just plausible-sounding storytelling, or does it follow logically from the facts?\n\nOutput valid JSON:\n{\n  \"challenges\": [\n    {\n      \"target_scenario\": \"optimistic\",\n      \"issue\": \"...\",\n      \"severity\": \"critical|significant|minor\"\n    }\n  ],\n  \"missed_scenarios\": [\"...\"],\n  \"overconfident_claims\": [\"...\"],\n  \"overall_quality\": \"solid|needs_revision|unreliable\"\n}\n\nRules:\n- Be constructive, not just negative.\n- Focus on logical gaps, not stylistic preferences."
})
```

#### 3.5c. Integrate Reasoning Output (Main Agent)

If adversarial review says `needs_revision` or `unreliable`, the main agent should revise the reasoning before proceeding.

The reasoning output is added to the report as a new section: **"Scenario Analysis"**.

---

### Stage 4: Merge (Synthesize) — Main Agent Only

Combine verified findings into a unified view.

**Merge rules:**
1. Prioritize high-confidence findings
2. Cross-referenced facts get confidence boost (+0.05 per additional source)
3. Single-source findings stay at original confidence
4. FAIL findings go to "Uncertain" section with explanation
5. PASS_WITH_CAVEATS findings are included with caveat notes
6. Contradictions must be noted explicitly
7. If verifier reduced confidence, use the verifier's revised number

### Stage 5: Report (Output) — Main Agent Only

Generate final report in both Markdown and JSON formats.

#### Markdown Report Structure

```markdown
# Research Report: [Topic]

**Date:** YYYY-MM-DD
**Confidence:** High/Medium/Low (based on overall evidence quality)
**Researcher:** AI Agent (graph-deepresearch pipeline)
**Pipeline:** DAG-orchestrated, {N} workers parallel, {N} claims verified

## Executive Summary
2-3 sentence overview of key findings.

## Key Findings

### Verified Facts (Multiple Sources)
| # | Fact | Source | Confidence |
|---|------|--------|------------|
| 1 | ... | [Source](url) | High |

### High-Confidence Information (Single Reliable Source)
| # | Fact | Source | Confidence |
|---|------|--------|------------|
| 1 | ... | [Source](url) | Medium |

### Uncertain / Unverified
| # | Information | Reason | Recommendation |
|---|-------------|--------|----------------|
| 1 | ... | Insufficient sources | Further research needed |

## Contradictions & Controversies
[If any conflicting findings exist]

## Source List
[All sources, sorted by credibility]

1. [Official] Title - URL (Date)
2. [Academic] Title - URL (Date)
...

## Verification & Adversarial Summary
| Finding ID | Original Conf. | Verifier | Adversarial | Counters | Final Disposition | Final Conf. |
|------------|---------------|----------|-------------|----------|-------------------|-------------|
| q1_f1 | 0.95 | PASS | No counters | 0 | ✅ Verified | 0.95 |
| q1_f2 | 0.80 | PASS_WITH_CAVEATS | Minor counters | 1 | ✅ Verified w/ caveats | 0.70 |
| q2_f1 | 0.40 | FAIL | Significant counters | 2 | ❌ Contested | 0.25 |

## Methodology
- **Search tools used:** tavily-search, web_fetch
- **Time range:** [date range]
- **Sources consulted:** [number]
- **Workers dispatched:** [number]
- **Claims verified:** [number]
- **Limitations:** [what was not covered]
```

#### JSON Output Structure

```json
{
  "metadata": {
    "topic": "...",
    "date": "2026-08-19",
    "pipeline_version": "2.0.0",
    "tools_used": ["tavily-search", "web_fetch"],
    "workers_dispatched": 4,
    "claims_verified": 12,
    "claims_adversarially_reviewed": 12
  },
  "executive_summary": "...",
  "findings": {
    "verified": [...],
    "high_confidence": [...],
    "uncertain": [...]
  },
  "contradictions": [...],
  "sources": [...],
  "verification_summary": [...],
  "methodology": {...},
  "confidence_assessment": {...}
}
```

---

## Search Tool Configuration

See [references/search-strategies.md](references/search-strategies.md) for:
- Tavily search commands and options
- web_fetch fallback procedures
- LLM knowledge handling (with staleness warnings)
- Source prioritization rules

## Handling LLM Knowledge Limitations

**Critical:** LLM training data has a cutoff date. When using LLM knowledge:

1. **Always timestamp it:** "Based on knowledge up to [date]"
2. **Never present as fact:** Mark as "LLM Knowledge (unverified, may be outdated)"
3. **Recommend verification:** Always suggest searching for recent updates
4. **Cross-check when possible:** If search tools are available, verify LLM claims

**Example marking:**
```json
{
  "claim": "...",
  "source": {
    "type": "llm_knowledge",
    "cutoff_date": "2026-01",
    "note": "May be outdated, verify with search"
  },
  "confidence": 0.5,
  "verification_status": "needs_verification"
}
```

---

## Pitfalls to Avoid

See [references/pitfalls.md](references/pitfalls.md) for detailed guidance.

**Quick reference:**
- ❌ Don't do research yourself — dispatch worker subagents
- ❌ Don't run workers sequentially — use parallel mode
- ❌ Don't let the verifier see other workers' outputs
- ❌ Don't let the adversarial agent see the verifier's output
- ❌ Don't skip the verification stage
- ❌ Don't skip the adversarial review — confirmation bias kills research quality
- ❌ Don't present LLM knowledge as verified fact
- ❌ Don't merge findings without a verification pass
- ✅ Do dispatch workers via `subagent({ tasks: [...] })` in parallel
- ✅ Do dispatch verifier + adversarial agent in parallel per finding
- ✅ Do let the adversarial agent search for the OPPOSITE claim
- ✅ Do combine verifier + adversarial results before dispositioning findings
- ✅ Do attach sources to every claim
- ✅ Do timestamp all information
- ✅ Do distinguish facts from interpretation
- ✅ Do note contradictions explicitly

---

## Full Execution Example

```
User: Research the current state of AI agents in finance

Main Agent (Stage 1 - Plan):
  Decomposes into:
    q1: "What AI tools are banks currently using?"
    q2: "How do regulators view AI in trading?"
    q3: "What are real-world case studies of AI in finance?"
    q4: "What is the market size for AI in financial services?"

Main Agent (Stage 2 - Dispatch Workers):
  subagent({
    tasks: [
      { agent: "default", task: "Research q1: What AI tools are banks using?..." },
      { agent: "default", task: "Research q2: How do regulators view AI in trading?..." },
      { agent: "default", task: "Research q3: What are real-world AI finance cases?..." },
      { agent: "default", task: "Research q4: What is the AI finance market size?..." }
    ]
  })
  → All 4 workers run in parallel, return JSON findings

Main Agent (Stage 3 - Dispatch Verifier + Adversarial Agent):
  For each finding from workers, dispatch TWO subagents IN PARALLEL:
    subagent({ task: "Verify this claim: {claim} from {url}..." })
    subagent({ task: "Find counter-evidence AGAINST: {claim}..." })
  → Verifier returns PASS/PASS_WITH_CAVEATS/FAIL
  → Adversarial returns counters + confidence adjustment
  → Main agent combines into final_disposition

Main Agent (Stage 4 - Merge):
  Combines verified findings, applies confidence adjustments

Main Agent (Stage 5 - Report):
  Generates Markdown + JSON report, saves to files
```

---

## Output Files

Save research outputs to:
- `research_{topic}_{YYYYMMDD}.md` — Human-readable report
- `research_{topic}_{YYYYMMDD}.json` — Machine-readable data

## References

- [Search Strategies](references/search-strategies.md) — Tool configurations and fallbacks
- [Verification Protocol](references/verification.md) — Detailed fact-checking procedures
- [Output Formats](references/output-formats.md) — Schema definitions for Markdown and JSON
- [Common Pitfalls](references/pitfalls.md) — Mistakes to avoid and how to fix them
