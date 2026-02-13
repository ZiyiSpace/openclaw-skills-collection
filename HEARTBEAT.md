# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

## Daily Tasks

每天早上 10:30 抓取 OpenRouter 月度排行榜数据：

**执行流程：**
1. 访问 https://openrouter.ai/apps?url=https%3A%2F%2Fopenclaw.ai%2F
2. 获取 Monthly Usage（月度排行榜）数据
3. 截图保存到：`~/Desktop/openrouter-xiaohongshu/YYYY-MM-DD/screenshot.jpg`
4. 生成中文和英文文案（简洁爆款风格）
5. 保存到：`~/Desktop/openrouter-xiaohongshu/YYYY-MM-DD/`

**文案风格：**
- 简洁有力（不要太长）
- 一句话钩子 + Top 3 + 关键洞察 + 互动问题
- 参考："国产三强争霸，Kimi断层第一"
- 中文版：231B、英文版：294B（精简版）

**重要提醒：**
- ✅ 抓取的是 **Monthly Usage（月度排行榜）**，不是 Daily Usage（日用量）
- ✅ 单位是 **B（billion tokens）**，不是 K（thousand tokens）
- ✅ Top 数据：Kimi K2.5 (390B)、Trinity (211B)、Gemini (153B)...
- ❌ 不要再用 GPT-4o-mini 551K 这类日用量数据写月榜文案！

---

## Skills Update Check

**检查频率：** 每天一次

每次心跳时检查 OpenClaw Skills 索引是否有更新：

1. 读取 `memory/skills-state.json` 获取当前 commit SHA
2. 调用 GitHub API 检查最新 commit：
   - URL: https://api.github.com/repos/VoltAgent/awesome-openclaw-skills/commits
3. 如果 SHA 不同：
   - 重新解析 README.md
   - 更新 `skills-index.md`
   - 更新 `skills-state.json`
   - **在当前会话直接提醒：** "检测到 X 个新技能，已更新索引"

**更新状态文件位置：** `memory/skills-state.json`
**索引文件位置：** `workspace/skills-index.md`
