# OpenRouter Page Structure Reference

Last verified: 2026-02-12

## URL
```
https://openrouter.ai/apps?url=https%3A%2F%2Fopenclaw.ai%2F
```

## Page Layout

### Header
- Title: "OpenClaw"
- Subtitle: "The AI that actually does things"
- "Top models" label

### Usage Chart
- **Date range**: 1月30日 - 2月11日 (example dates, may vary)
- **Y-axis**: 65B - 260B tokens
- Visual trend line showing usage growth

### Leaderboard Section
Heading: "Leaderboard"
Subheading: "Monthly Usage"

#### Top 10 Models (structure)
```
<generic>[rank number]</generic>
  <link>Model Name</link>
    <text>by</text>
    <link>Provider</link>
  <generic>[token usage]</generic>
```

### Example Data (2026-02-12)
1. Kimi K2.5 by moonshotai: 334B tokens
2. Trinity Large Preview (free) by arcee-ai: 185B tokens
3. Gemini 3 Flash Preview by google: 173B tokens
4. Claude Sonnet 4.5 by anthropic: 71.2B tokens
5. Step 3.5 Flash by stepfun: 66.6B tokens
6. Claude Opus 4.6 by anthropic: 54.6B tokens
7. DeepSeek V3.2 by deepseek: 52.2B tokens
8. Claude Opus 4.5 by anthropic: 51.3B tokens
9. Grok 4.1 Fast by x-ai: 48.9B tokens
10. Pony Alpha by openrouter: 43.8B tokens

## Key Patterns for Data Extraction

- Free models: Include "(free)" in model name
- Family models: Same provider appearing multiple times (e.g., anthropic, google)
- Top 3: Always highlighted in posts
- Usage format: "XBtokens" (e.g., "334Btokens")

## Browser Requirements

- Must wait for full page load (Next.js SPA)
- Screenshot entire page for context
- Extract structured data from leaderboard section
