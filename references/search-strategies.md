# Search Strategies

Configure search tools for different research scenarios.

## Tool Priority

1. **tavily-search** — Primary (requires API key)
2. **web_fetch** — Fallback (no API key needed)
3. **LLM Knowledge** — Last resort (staleness warning required)

## 1. Tavily Search

### Prerequisites

```bash
# Install if not present
curl -fsSL https://cli.tavily.com/install.sh | bash && tvly login

# Verify installation
tvly --version
```

### Search Commands

**Basic search:**
```bash
tvly search "query" --json
```

**Advanced search (more results, higher relevance):**
```bash
tvly search "query" --depth advanced --max-results 10 --json
```

**Time-filtered search:**
```bash
# Recent news (last week)
tvly search "query" --time-range week --topic news --json

# Last month
tvly search "query" --time-range month --json

# Custom date range
tvly search "query" --start-date YYYY-MM-DD --end-date YYYY-MM-DD --json
```

**Domain-filtered search:**
```bash
# Only official sources
tvly search "query" --include-domains company.com,docs.company.com --json

# Exclude low-quality sources
tvly search "query" --exclude-domains quora.com,pinterest.com --json
```

**With full content:**
```bash
# Include raw page content (saves separate fetch)
tvly search "query" --include-raw-content --max-results 3 --json
```

### Search Depth Selection

| Depth | Speed | Best For |
|-------|-------|----------|
| `ultra-fast` | Fastest | Quick lookups, autocomplete |
| `fast` | Fast | General research with chunks |
| `basic` | Medium | Default, good balance |
| `advanced` | Slowest | High-precision, critical facts |

**Recommendation:** Use `advanced` for Stage 2 (Worker), `basic` for quick checks.

### Source Type Detection

Parse Tavily results to determine source type:

```python
def classify_source(url, title):
    """Classify source by URL patterns and title keywords."""
    url_lower = url.lower()
    
    # Official sources
    if any(domain in url_lower for domain in ['.gov', '.edu', 'official']):
        return 'official'
    if 'docs.' in url_lower or 'documentation' in title.lower():
        return 'official'
    
    # Academic
    if any(domain in url_lower for domain in ['arxiv.org', 'scholar.google', 'pubmed']):
        return 'academic'
    if 'journal' in title.lower() or 'research' in title.lower():
        return 'academic'
    
    # Tech blogs
    if any(domain in url_lower for domain in ['medium.com', 'dev.to', 'hashnode']):
        return 'tech_blog'
    if 'blog' in url_lower or 'tutorial' in title.lower():
        return 'tech_blog'
    
    # News
    if any(domain in url_lower for domain in ['reuters.com', 'bloomberg.com', 'wsj.com']):
        return 'news'
    
    # Community
    if any(domain in url_lower for domain in ['reddit.com', 'news.ycombinator.com', 'stackoverflow.com']):
        return 'community'
    
    # Social
    if any(domain in url_lower for domain in ['twitter.com', 'x.com', 'weibo.com']):
        return 'social'
    
    return 'unknown'
```

## 2. web_fetch (Fallback)

When Tavily is unavailable or rate-limited.

### Usage

```bash
# Fetch a specific URL
curl -s "https://example.com/article" | head -100

# Or use in agent context
web_fetch(url="https://example.com/article")
```

### Limitations

- No search capability (must know the URL)
- No relevance scoring
- No content extraction optimization
- Manual source discovery required

### When to Use

- Verifying a specific URL exists
- Extracting content from known sources
- Cross-checking claims against primary sources

## 3. LLM Knowledge (Last Resort)

### When to Use

- Search tools are completely unavailable
- Topic is well-established historical fact (not recent events)
- Quick sanity check before deep research

### Staleness Handling

**ALWAYS include these warnings when using LLM knowledge:**

```markdown
> ⚠️ **Note:** This information is based on AI training data with a cutoff date of [DATE].
> It may be outdated or incomplete. Please verify with recent sources.
```

```json
{
  "claim": "...",
  "source": {
    "type": "llm_knowledge",
    "cutoff_date": "2026-01",
    "confidence_modifier": -0.3,
    "warning": "May be outdated, verify with search tools"
  }
}
```

### Confidence Adjustment

Apply confidence penalties to LLM knowledge:

| Information Age | Confidence Modifier |
|-----------------|---------------------|
| < 6 months | -0.1 |
| 6-12 months | -0.2 |
| 1-2 years | -0.3 |
| > 2 years | -0.5 or exclude |

### Cross-Verification Protocol

1. Make claim from LLM knowledge
2. Mark as "needs_verification"
3. If search tools available, immediately verify
4. Update confidence based on verification result

## Source Prioritization Rules

When multiple sources are available, prioritize in this order:

1. **Primary sources** — Official documentation, press releases, SEC filings
2. **Expert analysis** — Industry reports, academic papers
3. **Reputable media** — Established news outlets with editorial standards
4. **Community consensus** — Multiple independent community sources agreeing
5. **Single community source** — Use with caution, mark as unverified
6. **Social media** — Sentiment only, not factual evidence

## Search Query Best Practices

### Query Construction

- **Be specific:** "LangGraph multi-agent orchestration patterns" > "LangGraph"
- **Use quotes:** "exact phrase" for precise matches
- **Add context:** "AI agent finance {year}" not just "AI agents"
- **Multiple queries:** Search 2-3 variations per sub-question

### Query Examples

```
# Bad: Too broad
"AI agents"

# Good: Specific and contextualized
"LangGraph multi-agent supervisor pattern implementation {year}"

# Good: Multiple angles
"comparison LangGraph vs CrewAI vs AutoGen features"
"multi-agent framework benchmark performance"
"agent orchestration framework production usage"
```

## Rate Limiting & Fallbacks

### Tavily Rate Limits

If Tavily returns rate limit errors:
1. Wait 60 seconds
2. Retry with reduced `--max-results`
3. If still failing, switch to web_fetch for remaining queries
4. Log which queries used fallback

### Fallback Chain

```
Tavily search
  ↓ (if fails)
web_fetch on known URLs
  ↓ (if no URLs)
LLM knowledge (with staleness warning)
  ↓ (always)
Verify with at least one real source
```
