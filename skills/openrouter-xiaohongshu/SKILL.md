---
name: openrouter-xiaohongshu
description: Fetch OpenRouter app usage data, generate daily leaderboard posts for Xiaohongshu (小红书). Screenshots the page, extracts model rankings, and generates engaging posts with trend analysis.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "os": ["darwin", "linux"],
        "requires": {},
      },
  }
---

# OpenRouter Xiaohongshu Daily Post

## Overview

Automatically fetch OpenRouter app usage data (https://openrouter.ai/apps), generate structured posts for Xiaohongshu with trend analysis, model rankings, and selection suggestions. Runs daily at 9:00 AM (Asia/Shanghai) via cron.

## Usage

### Manual trigger

```bash
# In OpenClaw session
Run the skill manually to fetch and generate today's post.
```

### Automatic trigger

Cron job configured to run daily at 9:00 AM.

## Workflow

1. **Fetch data** - Open browser, navigate to OpenRouter apps page, screenshot and extract data
2. **Generate post** - Create structured post with:
   - Trend analysis (usage patterns, keywords)
   - Top 3 models with commentary
   - Free tier analysis
   - Family model positioning (Claude/Gemini)
   - Model selection suggestions
   - Engagement prompts
3. **Save output** - Screenshot + post content saved to workspace
4. **Notify** - Send notification to current session for manual posting

## Output

- **Screenshot**: `output/YYYY-MM-DD-openrouter-rankings.jpg`
- **Post content**: `output/YYYY-MM-DD-openrouter-post.md`

## Data Structure

Extracted from OpenRouter leaderboard:
- Model name, provider, token usage
- Date range and usage trend
- Free model positions
- Family model clusters

## References

- See `references/openrouter-page-structure.md` for page DOM structure
- See `templates/post_template.md` for post format
