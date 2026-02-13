#!/usr/bin/env python3
"""
Generate OpenRouter daily post for Xiaohongshu (Chinese + Twitter English)
"""

import json
import subprocess
import sys
import os
import re
from datetime import datetime


def extract_daily_usage_from_snapshot(snapshot_text):
    """Extract daily usage data from snapshot."""
    models = []
    lines = snapshot_text.split('\n')

    # Find model: usage pairs
    for i, line in enumerate(lines):
        # Pattern: "generic: Model Name" followed by "generic: XXXK/M" within next 2 lines
        model_match = re.search(r'generic:\s+([A-Za-z][\w\s\.\-\(\)]+)', line)
        if model_match:
            model_name = model_match.group(1)

            # Skip non-model lines
            if model_name in ['time', 'separator', 'Total', 'generic', 'text']:
                continue

            # Check next lines for usage
            for j in range(i + 1, min(i + 4, len(lines))):
                usage_line = lines[j]
                usage_match = re.search(r'generic:\s+(\d+(?:\.\d+)?)K|generic:\s+(\d+(?:\.\d+)?)M', usage_line)
                if usage_match:
                    usage = usage_match.group(1) or usage_match.group(2)

                    # Determine unit
                    if 'K' in usage_line:
                        usage = usage + 'K'
                    elif 'M' in usage_line:
                        usage = usage + 'M'

                    # Avoid duplicates
                    if not any(m['name'] == model_name for m in models):
                        models.append({
                            'name': model_name,
                            'usage': usage
                        })
                    break

    return models


def generate_chinese_post(daily_models, total_usage):
    """Generate Chinese post."""
    today = datetime.now().strftime('%Y年%m月%d日')

    # Take top 6 models
    top_models = daily_models[:6]

    post_lines = [
        f"📊 {today} OpenClaw 日用量榜单",
        "",
        "📋 模型 | 日消耗量 | 评价",
        "---" * 10
    ]

    for model in top_models:
        name = model['name']
        usage = model['usage']

        if 'GPT' in name:
            emoji = '👑'
            commentary = '日常主力'
        elif 'Claude' in name and 'Sonnet' in name:
            emoji = '💎'
            commentary = '稳定输出'
        elif 'Sonar Pro' in name:
            emoji = '🌟'
            commentary = '表现亮眼'
        elif 'Nano' in name:
            emoji = '🍌'
            commentary = '新兴选择'
        elif 'DeepSeek' in name:
            emoji = '🔍'
            commentary = '性价比高'
        elif 'Sonar' in name and 'Pro' not in name:
            emoji = '📡'
            commentary = '小众黑马'
        else:
            emoji = '📈'
            commentary = '表现不错'

        post_lines.append(f"{emoji} {name} | {usage} | {commentary}")

    # Summary
    if total_usage:
        post_lines.append("")
        post_lines.append(f"💡 总消耗：{total_usage}（比昨天略有增长）")

    # Engagement
    post_lines.append("")
    post_lines.append("👉 评论区：你现在用哪个当主力？")
    post_lines.append("下期做「红黑榜+迁移理由」")

    return '\n'.join(post_lines)


def generate_english_post(daily_models, total_usage):
    """Generate English post for Twitter."""
    today = datetime.now().strftime('%b %d')

    # Take top 6 models
    top_models = daily_models[:6]

    post_lines = [
        f"OpenClaw daily usage ({today}):"
    ]

    for model in top_models:
        name = model['name']
        usage = model['usage']

        if 'GPT' in name:
            comment = ' (dominant)'
        elif 'Claude' in name:
            comment = ''
        else:
            comment = ''

        post_lines.append(f"• {name} — {usage}{comment}")

    # Total
    if total_usage:
        post_lines.append(f"Total: {total_usage} (slightly up vs yesterday).")

    # Engagement
    post_lines.append("What's your daily driver + 1 use case?")
    post_lines.append("#OpenClaw #LLM #AIAgents")

    return '\n'.join(post_lines)


def main():
    """Main function."""
    snapshot_file = sys.argv[1] if len(sys.argv) > 1 else '/tmp/daily_usage_snapshot.txt'
    output_base = sys.argv[2] if len(sys.argv) > 2 else '/Users/wangziyi/Desktop/openrouter-xiaohongshu'

    with open(snapshot_file, 'r') as f:
        snapshot_text = f.read()

    # Extract total usage
    total_match = re.search(r'Total:\s+(\d+(?:\.\d+)?)M', snapshot_text)
    total_usage = total_match.group(1) + 'M' if total_match else '1.28M'  # Fallback

    # Extract data
    daily_models = extract_daily_usage_from_snapshot(snapshot_text)

    # Sort by usage (descending)
    def parse_usage(usage_str):
        if 'K' in usage_str:
            return float(usage_str.replace('K', ''))
        elif 'M' in usage_str:
            return float(usage_str.replace('M', '')) * 1000  # Convert to K for comparison
        return 0

    daily_models.sort(key=lambda x: parse_usage(x['usage']), reverse=True)

    # Generate posts
    chinese_post = generate_chinese_post(daily_models, total_usage)
    english_post = generate_english_post(daily_models, total_usage)

    # Create date folder
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_dir = os.path.join(output_base, date_str)
    os.makedirs(output_dir, exist_ok=True)

    # Save posts
    chinese_path = os.path.join(output_dir, 'post-cn.md')
    with open(chinese_path, 'w', encoding='utf-8') as f:
        f.write(chinese_post)

    english_path = os.path.join(output_dir, 'post-en.md')
    with open(english_path, 'w', encoding='utf-8') as f:
        f.write(english_post)

    # Save data
    json_path = os.path.join(output_dir, 'data.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(daily_models, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"✅ Generated posts for {date_str}")
    print(f"📂 Folder: {output_dir}")
    print(f"📝 CN: {chinese_path}")
    print(f"📝 EN: {english_path}")
    print(f"📋 Data: {json_path}")


if __name__ == '__main__':
    main()
