# OpenRouter Daily Post Template

## Variables
- {{date_range}}: Date range from chart
- {{trend_keyword}}: 爬坡/震荡/回落/突破
- {{trend_summary}}: One-sentence trend summary
- {{top3}}: Array of top 3 models with commentary
- {{free_models}}: Free model analysis
- {{family_analysis}}: Family model positioning
- {{model_suggestions}}: Model selection suggestions
- {{next_topic}}: Next topic teaser

---

## Post Content

{{trend_emoji}} OpenClaw {{version}} 榜：{{trend_keyword}}

📈 {{date_range}} 用量变化：{{trend_summary}}

🏆 月榜前三：

{{#each top3}}
{{this.rank}}️⃣ {{this.name}}：{{this.usage}}
{{this.commentary}}
{{/each}}

{{free_models}}

{{family_analysis}}

💡 模型选择建议：
{{model_suggestions}}

👉 {{engagement_prompt}}

---

## Commentary Templates

### Kimi Models
- 断层第一
- 成了全村希望
- 用量碾压，口碑在线

### Free Models
- 免费也能当主力
- 0成本，性能在线
- 免费阵营太猛，吸量惊人

### Claude Models
- 稳定输出
- 质量天花板
- 按任务选，追质量用 Claude

### Gemini Models
- 谷歌一家多位
- 家族式占位
- 谷歌生态整合强

### Other Models
- 社区口碑型黑马
- 性价比之选
- 潜力股

## Trend Keywords
- 爬坡：usage increasing steadily
- 震荡：usage fluctuating
- 回落：usage decreasing
- 突破：usage hitting new highs

## Engagement Prompts
- 评论区告诉我：你现在用哪个当主力？
- 评论区蹲一个：你现在的主力模型是？
- 用过这些模型吗？评论区聊聊体验
- 你的主力模型换了吗？为啥换的？
