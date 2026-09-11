# Common Pitfalls

Mistakes to avoid and how to fix them.

## 1. Parallel Execution Violations

### ❌ Wrong: Sequential by Default

```
Worker 1 → results → Worker 2 → results → Worker 3 → results → Verify
```

**Problem:** Workers wait for each other unnecessarily. Slow and creates dependency.

### ✅ Correct: True Parallel Fan-Out

```
Worker 1 ─┐
Worker 2 ─┼─→ Verify → Merge → Report
Worker 3 ─┘
```

**Fix:** Ensure sub-questions are truly independent. If B needs A's output, the decomposition is wrong.

### Detection

Ask: "Does Worker 2 ever read Worker 1's output before starting?"
If yes → Wrong. Redesign the sub-questions.

---

## 2. Verification Bypass

### ❌ Wrong: Worker Output = Final Output

```
Worker results → Report (no verification)
```

**Problem:** No independent check. Errors propagate to final report.

### ✅ Correct: Verification Gate

```
Worker results → Verify → Merge → Report
```

**Fix:** Always include the Verify stage. Even a quick cross-check catches obvious errors.

### Detection

Check: "Is there a separate verifier agent that doesn't see other workers' outputs?"
If no → Missing verification.

---

## 3. Source Attribution Missing

### ❌ Wrong: Unsourced Claims

```json
{
  "claim": "Product X has hundreds of users"
}
```

**Problem:** Cannot verify, cannot trace, cannot trust.

### ✅ Correct: Full Source Chain

```json
{
  "claim": "Product X has hundreds of users",
  "source": {
    "url": "https://example.com/article",
    "title": "Example News Report",
    "date": "YYYY-MM-DD",
    "type": "news",
    "credibility": "medium"
  }
}
```

**Fix:** Require source object for every finding. Reject findings without sources.

### Detection

Count: "How many findings have no source?"
If > 0 → Incomplete.

---

## 4. LLM Knowledge Presented as Fact

### ❌ Wrong: No Staleness Warning

```json
{
  "claim": "Company X has 1000 employees",
  "confidence": 0.9
}
```

**Problem:** LLM data may be outdated. Presenting as fact is misleading.

### ✅ Correct: Marked as LLM Knowledge

```json
{
  "claim": "Company X has 1000 employees (as of YYYY, may be outdated)",
  "source": {
    "type": "llm_knowledge",
    "cutoff_date": "YYYY-MM",
    "warning": "Verify with recent sources"
  },
  "confidence": 0.5
}
```

**Fix:** Always timestamp LLM knowledge. Apply confidence penalty. Recommend verification.

### Detection

Check: "Are there findings with confidence > 0.7 that have no real source?"
If yes → Likely unverified LLM knowledge.

---

## 5. Confirmation Bias in Verification

### ❌ Wrong: Verifier Sees All Workers' Outputs

```
Worker 1 results ─┐
Worker 2 results ─┼─→ Verifier → Report
Worker 3 results ─┘
```

**Problem:** Verifier unconsciously agrees with majority view.

### ✅ Correct: Isolated Verification

```
Worker 1 results ──→ Verifier 1 ─┐
Worker 2 results ──→ Verifier 2 ─┼─→ Cross-check → Report
Worker 3 results ──→ Verifier 3 ─┘
```

Or at minimum:

```
Worker results ──→ (pause) ──→ Verifier (fresh context, no worker outputs)
```

**Fix:** Verifier receives only the claims to verify, not the full context of how they were found.

### Detection

Ask: "Does the verifier know which worker produced each finding?"
If yes → Bias risk.

---

## 6. Over-Decomposition

### ❌ Wrong: Too Many Micro-Questions

```
Sub-questions: 15 items, each asking about one tiny fact
```

**Problem:** Excessive overhead, no coherent research angles, hard to synthesize.

### ✅ Correct: Balanced Decomposition

```
Sub-questions: 3-5 items, each a complete research angle
```

**Fix:** Each sub-question should be:
- Independently researchable
- Meaningful on its own
- Answerable with 3-10 sources

**Rule of thumb:** 3-5 sub-questions for most research tasks.

### Detection

Count: "Are there more than 7 sub-questions?"
If yes → Likely over-decomposed.

---

## 7. Under-Decomposition

### ❌ Wrong: Too Broad Sub-Questions

```
Sub-questions: ["Tell me about AI in finance"]
```

**Problem:** Too broad to research effectively. Worker will produce shallow results.

### ✅ Correct: Focused Sub-Questions

```
Sub-questions: [
  "What AI tools are major banks using?",
  "How do regulators view AI in trading?",
  "What are the ROI metrics for AI in finance?"
]
```

**Fix:** Break broad topics into specific, answerable questions.

### Detection

Ask: "Can a worker answer this with 3-5 focused searches?"
If no → Too broad.

---

## 8. Contradictions Ignored

### ❌ Wrong: Pick One Version

```json
{
  "claim": "X is true",
  "sources": ["Source A says yes", "Source B says no"],
  "confidence": 0.8
}
```

**Problem:** Contradiction exists but is hidden.

### ✅ Correct: Document Contradiction

```json
{
  "contradiction": {
    "topic": "X",
    "position_a": {"claim": "X is true", "source": "A"},
    "position_b": {"claim": "X is false", "source": "B"},
    "assessment": "Source A is more recent and official",
    "resolution": "A is likely correct"
  }
}
```

**Fix:** Always document contradictions. Let the reader decide or provide your assessment with reasoning.

### Detection

Check: "Are there claims where multiple sources disagree?"
If yes → Must be documented.

---

## 9. Confidence Inflation

### ❌ Wrong: Everything High Confidence

```json
{
  "findings": [
    {"confidence": 0.95},
    {"confidence": 0.95},
    {"confidence": 0.95}
  ]
}
```

**Problem:** No differentiation. Reader can't assess reliability.

### ✅ Correct: Honest Confidence Distribution

```json
{
  "findings": [
    {"confidence": 0.95, "reason": "Multiple official sources"},
    {"confidence": 0.75, "reason": "Single reliable source"},
    {"confidence": 0.50, "reason": "Unverified claim"}
  ]
}
```

**Fix:** Apply confidence rules consistently. Use the full range from 0.3 to 0.95.

### Detection

Check: "What's the standard deviation of confidence scores?"
If < 0.1 → Likely inflated or not differentiated.

---

## 10. Report Without Methodology

### ❌ Wrong: No Transparency

```markdown
# Research Report

## Findings
1. Fact A
2. Fact B
```

**Problem:** Reader can't assess how research was conducted.

### ✅ Correct: Full Methodology

```markdown
# Research Report

## Methodology
- Search tools: tavily-search
- Sources consulted: 15
- Time range: YYYY-MM-DD to YYYY-MM-DD
- Limitations: No access to proprietary databases

## Findings
1. Fact A (Source: [link])
2. Fact B (Source: [link])
```

**Fix:** Always include methodology section. Be transparent about tools, sources, and limitations.

### Detection

Check: "Does the report explain HOW the research was done?"
If no → Missing methodology.

---

## Quick Self-Check

Before publishing any research report, verify:

- [ ] All sub-questions were researched independently
- [ ] Every finding has a source with URL, date, and type
- [ ] A verifier reviewed all findings
- [ ] LLM knowledge is marked with staleness warning
- [ ] Contradictions are documented
- [ ] Confidence scores vary (not all the same)
- [ ] Methodology section exists
- [ ] Limitations are acknowledged
