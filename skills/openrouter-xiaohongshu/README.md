# OpenRouter Xiaohongshu Daily Post Skill

自动抓取 OpenRouter 榜单数据，生成小红书日更文案（中文 + 英文 Twitter）。

## 功能

- 📊 自动抓取 OpenRouter Apps 页面日用量数据
- 🖼️ 截取完整榜单截图
- 📝 生成中英文文案（简短版）
- 📁 按日期归档（YYYY-MM-DD 文件夹）
- ⏰ 支持定时自动执行（每天 10:00）

## 使用方法

### 手动执行

在 OpenClaw 会话中：

```bash
# 1. 打开浏览器并导航到页面
browser: navigate(targetUrl="https://openrouter.ai/apps?url=https%3A%2F%2Fopenclaw.ai%2F", profile="openclaw")

# 2. 点击最后一个柱状条显示日用量
browser: act(targetId="...", ref="e86")

# 3. 截取快照并保存
browser: snapshot(targetId="...", refs="role") > /tmp/daily_usage_snapshot.txt

# 4. 运行生成脚本
exec: python3 workspace/skills/openrouter-xiaohongshu/scripts/generate_post_final.py /tmp/daily_usage_snapshot.txt ~/Desktop/openrouter-xiaohongshu
```

### 自动执行（Cron）

使用 OpenClaw cron 配置每日自动执行：

```json
{
  "name": "openrouter-daily-post",
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "执行 openrouter 每日榜单抓取和文案生成。使用 browser 工具访问 https://openrouter.ai/apps?url=https%3A%2F%2Fopenclaw.ai%2F 并运行 workspace/skills/openrouter-xiaohongshu/scripts/generate_post_final.py 脚本。"
  }
}
```

每天上午 10:00 自动运行。

## 输出格式

生成的文件夹结构：
```
openrouter-xiaohongshu/
└── 2026-02-12/
    ├── post-cn.md        # 中文文案（小红书）
    ├── post-en.md        # 英文文案（Twitter）
    ├── screenshot.jpg    # 榜单截图
    └── data.json         # 原始数据
```

## 文案格式

### 中文版（小红书）
```
📊 2026年02月12日 OpenClaw 日用量榜单

📋 模型 | 日消耗量 | 评价
------------------------------
👑 GPT-4o-mini | 551K | 日常主力
💎 Claude 3.5 Sonnet | 277K | 稳定输出
🌟 Sonar Pro | 220K | 表现亮眼
🍌 Nano Banana Pro | 62K | 新兴选择
🔍 DeepSeek V3 | 45K | 性价比高
📡 Sonar | 33K | 小众黑马

💡 总消耗：1.28M（比昨天略有增长）

👉 评论区：你现在用哪个当主力？
下期做「红黑榜+迁移理由」
```

### 英文版（Twitter）
```
OpenClaw daily usage (Feb 12):
• GPT-4o-mini — 551K (dominant)
• Claude 3.5 Sonnet — 277K
• Sonar Pro — 220K
• Nano Banana Pro (Gemini 3 Pro Image Preview) — 62K
• DeepSeek V3 — 45K
• Sonar — 33K
Total: 1.28M (slightly up vs yesterday).
What's your daily driver + 1 use case?
#OpenClaw #LLM #AIAgents
```

## 依赖要求

- Python 3.6+
- OpenClaw browser 工具
- 网络连接（访问 OpenRouter）

## 注意事项

1. **日用量获取**：需要点击最后一个柱状条（ref="e86"）才能显示日用量数据
2. **文案合规**：避免使用"推荐""必用"等绝对化词汇
3. **手动发布**：文案生成后需要手动复制到小红书发布（避免自动化风险）

## 故障排查

### 数据提取失败
检查页面快照格式是否正确，确保日用量弹窗已打开

### 截图不完整
使用 `fullPage=true` 参数获取完整页面截图

### Cron 未触发
检查时区设置（应设置为 Asia/Shanghai），确认 Gateway 正在运行

## 扩展内容方向

基于数据可生成的扩展内容：

1. **红黑榜系列** - 本期主力 vs 避坑模型
2. **迁移理由** - 从 Claude 换到 GPT 的理由
3. **家族分析** - Sonar 系列占位说明什么
4. **趋势预测** - 下周谁会掉出前10
