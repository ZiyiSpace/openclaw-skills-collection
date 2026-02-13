#!/usr/bin/env python3
"""
Main script to generate OpenRouter daily post for Xiaohongshu.
Usage: Called from OpenClaw session or cron.
"""

import json
import subprocess
import sys
import os
from datetime import datetime


def get_base_dir():
    """Get skill base directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_fetch_data(snapshot_text, output_dir=None):
    """
    Run fetch_data.py to extract leaderboard data.

    Args:
        snapshot_text: Browser snapshot text
        output_dir: Output directory for results

    Returns:
        dict: Extracted data and generated post
    """
    base_dir = get_base_dir()
    script_path = os.path.join(base_dir, 'scripts', 'fetch_data.py')

    # Run the fetch script with snapshot data
    cmd = [sys.executable, script_path, '--format', 'json']

    if output_dir:
        cmd.extend(['--output', output_dir])

    result = subprocess.run(
        cmd,
        input=snapshot_text,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"fetch_data.py failed: {result.stderr}")

    return json.loads(result.stdout)


def generate_post_content(leaderboard_data):
    """
    Generate complete post content with enhanced analysis.

    Args:
        leaderboard_data: Extracted leaderboard data

    Returns:
        str: Formatted post content
    """
    if not leaderboard_data or not leaderboard_data.get('leaderboard'):
        return None

    all_models = leaderboard_data['leaderboard']
    top5 = all_models[:5]
    free_models = [m for m in all_models if m['is_free']]

    # Get date
    today = datetime.now().strftime('%Y年%m月%d日')

    # Generate post
    post_lines = [
        f"📊 {today} OpenClaw 模型排行榜",
        "",
        "📋 排名 | 模型 | 消耗量 | 评价",
        "---" * 15
    ]

    # Generate commentary for top 5
    for model in top5:
        name = model['name']
        usage = model['usage']

        # Generate emoji and commentary
        if model['rank'] == 1:
            emoji = '👑'
            if 'Kimi' in name:
                commentary = '断层王者，绝对主力'
            else:
                commentary = '榜首霸主'
        elif model['rank'] == 2:
            emoji = '🥈'
            commentary = '强力亚军'
        elif model['rank'] == 3:
            emoji = '🥉'
            commentary = '稳居三甲'
        elif model['is_free']:
            emoji = '🔥'
            commentary = '免费黑马，吸量惊人'
        elif 'Kimi' in name:
            emoji = '🌟'
            commentary = '稳定输出'
        elif 'Claude' in name:
            emoji = '💎'
            commentary = '质量天花板'
        elif 'Gemini' in name:
            emoji = '🌈'
            commentary = '谷歌生态强'
        elif 'Step' in name:
            emoji = '⚡'
            commentary = '推理速度快'
        elif 'Pony' in name:
            emoji = '🐴'
            commentary = '社区口碑黑马'
        elif 'DeepSeek' in name:
            emoji = '🔍'
            commentary = '性价比之选'
        elif 'Grok' in name:
            emoji = '🐦'
            commentary = '马斯克出品'
        else:
            emoji = '📈'
            commentary = '表现亮眼'

        post_lines.append(f"{emoji} 第{model['rank']}名 | {name} | {usage} | {commentary}")

    # Free models section
    if free_models:
        post_lines.append("")
        post_lines.append("🔥 免费阵营太猛：")
        for fm in free_models[:3]:
            post_lines.append(f"• {fm['name']}：{fm['usage']}（第{fm['rank']}位）")

    # Deep analysis report
    post_lines.append("")
    post_lines.append("📝 深度分析报告：")

    # Analysis 1: Top model analysis
    top_model = all_models[0]
    post_lines.append("")
    post_lines.append("1️⃣ 稳坐钓鱼台的王者")
    post_lines.append(f"👑 {top_model['name']}：{top_model['usage']}")
    if 'Kimi' in top_model['name']:
        post_lines.append("背景：Moonshot AI（月之暗面）的旗舰模型。")
        post_lines.append("分析：当其他模型还在争夺「老二老三」时，Kimi K2.5 依然占据榜首，比第二名高出一倍多。说明它已经成为了大多数用户的「日用主力（Daily Driver）」，不仅是尝鲜，而是真正融入了工作流。")
    elif 'Trinity' in top_model['name']:
        post_lines.append("背景：Arcee AI 的免费预览模型。")
        post_lines.append("分析：免费模型登顶，说明用户对「0 成本且强」的需求强烈。用户忠诚度极低，一旦有更好的免费替代品，会立即迁移。")
    else:
        post_lines.append(f"背景：{top_model['name']} 是本期榜单的榜首。")
        post_lines.append("分析：凭借出色的性能和用户体验，获得了用户的广泛认可，成为当前的主力选择。")

    # Analysis 2: Free models phenomenon
    if free_models:
        post_lines.append("")
        post_lines.append("2️⃣ 免费阵营的内卷")
        post_lines.append(f"🔥 本期有 {len(free_models)} 个免费模型上榜：")
        for fm in free_models:
            post_lines.append(f"• {fm['name']}（第{fm['rank']}位）")
        post_lines.append("分析：2026 年初的一个核心现象 ——「免费且强」的模型正在疯狂内卷。用户正在大量测试这些免费模型的边界，它们的流量增长速度远超付费模型。")

    # Analysis 3: Family model positioning
    provider_counts = {}
    for m in all_models[:10]:
        # Extract provider from model name or use default
        if 'Kimi' in m['name']:
            provider = 'Moonshot AI'
        elif 'Claude' in m['name']:
            provider = 'Anthropic'
        elif 'Gemini' in m['name']:
            provider = 'Google'
        elif 'Step' in m['name']:
            provider = 'StepFun'
        elif 'Pony' in m['name']:
            provider = 'OpenRouter'
        elif 'DeepSeek' in m['name']:
            provider = 'DeepSeek'
        elif 'Grok' in m['name']:
            provider = 'xAI'
        elif 'Trinity' in m['name']:
            provider = 'Arcee AI'
        else:
            provider = m.get('provider', 'Unknown')

        provider_counts[provider] = provider_counts.get(provider, 0) + 1

    family_models = {k: v for k, v in provider_counts.items() if v > 1}
    if family_models:
        post_lines.append("")
        post_lines.append("3️⃣ 家族式占位分析")
        post_lines.append("🤖 多个模型来自同一厂商：")
        for provider, count in family_models.items():
            post_lines.append(f"• {provider}：{count} 个模型")
        post_lines.append("分析：这说明大家在「按任务选模型」，不是只追最强。不同的模型针对不同的场景（Claude Sonnet 追稳定、Claude Opus 追性能、Gemini 追速度），用户会根据具体需求切换。")

    # Analysis 4: Emerging trends
    post_lines.append("")
    post_lines.append("4️⃣ 新兴趋势")
    step_models = [m for m in all_models if 'Step' in m['name']]
    if step_models:
        post_lines.append("⚡ StepFun 系列崛起：")
        for sm in step_models[:2]:
            post_lines.append(f"• {sm['name']}（第{sm['rank']}位）")
        post_lines.append("分析：主打「智能体优先」和超快推理速度，正在吸引用户关注。")

    pony_models = [m for m in all_models if 'Pony' in m['name']]
    if pony_models:
        post_lines.append("")
        post_lines.append("🐴 Pony Alpha 的崛起：")
        for pm in pony_models:
            post_lines.append(f"• {pm['name']}（第{pm['rank']}位）")
        post_lines.append("分析：社区口碑型黑马，擅长角色扮演和代码。用户正在疯狂测试它的边界，是目前的流量明星。")

    # Engagement
    post_lines.append("")
    post_lines.append("👉 评论区告诉我：你现在用哪个当主力？")
    post_lines.append("我下期做「红黑榜+迁移理由」。")

    return '\n'.join(post_lines)


def save_results(output_dir, screenshot_path, post_content, leaderboard_data):
    """
    Save screenshot and post content.

    Args:
        output_dir: Output directory
        screenshot_path: Path to screenshot
        post_content: Generated post text
        leaderboard_data: Extracted data

    Returns:
        dict: Paths to saved files
    """
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.now().strftime('%Y-%m-%d')

    # Save post content
    post_path = os.path.join(output_dir, f'{date_str}-openrouter-post.md')
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(post_content)

    # Save screenshot if path provided
    screenshot_dest = None
    if screenshot_path and os.path.exists(screenshot_path):
        screenshot_dest = os.path.join(output_dir, f'{date_str}-openrouter-rankings.jpg')
        # Copy screenshot to output directory
        import shutil
        shutil.copy(screenshot_path, screenshot_dest)

    # Save JSON data
    json_path = os.path.join(output_dir, f'{date_str}-openrouter-data.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(leaderboard_data, f, indent=2, ensure_ascii=False)

    return {
        'post_path': post_path,
        'screenshot_path': screenshot_dest,
        'json_path': json_path
    }


def main():
    """Main function to orchestrate workflow."""
    import argparse
    parser = argparse.ArgumentParser(description='Generate OpenRouter daily post')
    parser.add_argument('--snapshot', help='Browser snapshot text')
    parser.add_argument('--screenshot', help='Screenshot file path')
    parser.add_argument('--output', default='/tmp/openrouter-xiaohongshu', help='Output directory')
    args = parser.parse_args()

    if not args.snapshot:
        print("Error: --snapshot is required", file=sys.stderr)
        sys.exit(1)

    # Read snapshot file
    with open(args.snapshot, 'r', encoding='utf-8') as f:
        snapshot_text = f.read()

    # Extract data
    data = run_fetch_data(snapshot_text)

    # Generate post
    post_content = generate_post_content(data)

    if not post_content:
        print("Error: Failed to generate post content", file=sys.stderr)
        sys.exit(1)

    # Save results
    saved_paths = save_results(args.output, args.screenshot, post_content, data)

    # Print summary
    print(f"✅ Generated post for {datetime.now().strftime('%Y-%m-%d')}")
    print(f"📊 Extracted {len(data['leaderboard'])} models")
    print(f"📝 Post: {saved_paths['post_path']}")
    if saved_paths['screenshot_path']:
        print(f"🖼️  Screenshot: {saved_paths['screenshot_path']}")
    print(f"📋 Data: {saved_paths['json_path']}")

    # Print post preview
    print("\n--- Post Preview ---")
    print(post_content[:800] + "..." if len(post_content) > 800 else post_content)


if __name__ == '__main__':
    main()
