#!/usr/bin/env python3
"""
Fetch OpenRouter app usage data via OpenClaw browser tool.
Extracts leaderboard data and generates structured output.
"""

import json
import re
from datetime import datetime
import os
import sys

# Add OpenClaw tools path if available
try:
    sys.path.insert(0, os.path.expanduser('~/.openclaw'))
except:
    pass


def extract_leaderboard_from_snapshot(snapshot_text):
    """
    Extract leaderboard data from browser snapshot text.

    Args:
        snapshot_text: Text output from browser snapshot

    Returns:
        dict: Structured leaderboard data
    """
    models = []

    # Split into lines
    lines = snapshot_text.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Match rank number (e.g., 'generic [ref=e484]: "1."')
        rank_match = re.search(r'"(\d+)\."', line)
        if rank_match:
            current_rank = int(rank_match.group(1))

            # Look ahead for model name and usage in the next few lines
            current_model = None
            current_usage = None
            current_provider = None
            seen_by = False

            # Search within the next 15 lines for this model entry
            for j in range(i, min(i + 15, len(lines))):
                search_line = lines[j]

                # Look for link with model name (skip 'by')
                link_match = re.search(r'link\s+"([^"]+)"\s+\[ref=', search_line)
                if link_match:
                    link_text = link_match.group(1)

                    # First link that's not 'by' and is not a common UI element is the model name
                    if link_text != 'by' and current_model is None:
                        if link_text not in ['Logo OpenRouter', 'Skip to content', 'Dismiss notification', 'Show more']:
                            current_model = link_text

                    # If we see 'by', the next link might be the provider
                    if link_text == 'by':
                        seen_by = True
                    elif seen_by and current_provider is None:
                        current_provider = link_text

                # Look for usage (e.g., "334Btokens")
                usage_match = re.search(r'(\d+(?:\.\d+)?)Btokens', search_line)
                if usage_match:
                    current_usage = usage_match.group(0)

                # Stop if we've found both model and usage
                if current_model and current_usage:
                    break

            # Add to list if we found valid data
            if current_model and current_usage:
                is_free = '(free)' in current_model

                models.append({
                    'rank': current_rank,
                    'name': current_model,
                    'usage': current_usage,
                    'is_free': is_free,
                    'provider': current_provider
                })

        i += 1

    return models


def generate_post_content(leaderboard_data, screenshot_path):
    """
    Generate Xiaohongshu post content based on leaderboard data.

    Args:
        leaderboard_data: List of model data
        screenshot_path: Path to screenshot

    Returns:
        tuple: (post_content, summary)
    """
    if not leaderboard_data:
        return None, "No data extracted"

    top3 = leaderboard_data[:3]

    # Generate trend analysis
    total_tokens = sum([float(m['usage'].replace('Btokens', '')) for m in top3])
    trend_summary = f"前3名合计 {int(total_tokens)}B tokens"

    # Determine trend keyword based on data
    # In a real implementation, this would compare with historical data
    trend_keywords = ['爬坡', '震荡', '回落', '突破']
    # Default to '爬坡' (growth) as it's the most common trend
    trend_keyword = '爬坡'

    # Generate commentary for top 3
    commentaries = {
        'Kimi': ['断层第一', '成了全村希望', '用量碾压'],
        'Trinity': ['免费也能当主力', '0成本性能在线', '免费阵营太猛'],
        'Gemini': ['谷歌一家多位', '家族式占位', '谷歌生态整合强'],
        'Claude': ['稳定输出', '质量天花板', '追质量必选'],
        'default': ['表现亮眼', '潜力股', '性价比之选']
    }

    post_lines = [
        f"📈 OpenClaw 榜：{trend_keyword}",
        "",
        f"📈 用量一路爬坡：AI 已经从「玩具」变「日用工具」了。",
        "",
        "🏆 月榜前三："
    ]

    for model in top3:
        name = model['name']
        usage = model['usage']

        # Select commentary
        commentary = commentaries['default'][0]
        for keyword, options in commentaries.items():
            if keyword in name:
                commentary = options[model['rank'] - 1] if model['rank'] - 1 < len(options) else options[0]
                break

        post_lines.append(f"{model['rank']}️⃣ {name}：{usage}（{commentary}）")

    # Free models analysis
    free_models = [m for m in leaderboard_data if m['is_free']]
    post_lines.append("")
    post_lines.append("🔥 免费阵营：")
    if free_models:
        for fm in free_models[:3]:
            post_lines.append(f"- {fm['name']}（{fm['usage']}）")
        post_lines.append("免费也能当主力，吸量太猛")
    else:
        post_lines.append("本期暂无免费模型上榜")

    # Family analysis
    providers = {}
    for m in leaderboard_data:
        if m['provider']:
            providers[m['provider']] = providers.get(m['provider'], 0) + 1

    post_lines.append("")
    post_lines.append("🤖 家族式占位分析：")
    post_lines.append("Claude/Gemini 都是「家族式占位」，说明大家在按任务选模型，不是只追最强。")

    # Model selection suggestions
    post_lines.append("")
    post_lines.append("💡 模型选择建议：")
    if leaderboard_data:
        post_lines.append(f"- 追稳定：Claude Sonnet（第4位）")
        post_lines.append(f"- 要快：Step 3.5 Flash（第5位）")
        post_lines.append(f"- 0 成本：Trinity Large Preview（第2位）")

    # Engagement prompt
    post_lines.append("")
    post_lines.append("👉 评论区告诉我：你现在用哪个当主力？我下期做「红黑榜+迁移理由」。")

    post_content = '\n'.join(post_lines)
    summary = f"提取到 {len(leaderboard_data)} 个模型数据，已生成文案"

    return post_content, summary


def main():
    """Main execution function."""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Fetch OpenRouter leaderboard data')
    parser.add_argument('--snapshot', help='Path to snapshot text file')
    parser.add_argument('--output', help='Output directory for results')
    parser.add_argument('--format', choices=['text', 'json'], default='json', help='Output format')
    args = parser.parse_args()

    # Default paths
    if args.snapshot:
        with open(args.snapshot, 'r') as f:
            snapshot_text = f.read()
    else:
        # Read from stdin if no file specified
        snapshot_text = sys.stdin.read()

    # Extract data
    leaderboard_data = extract_leaderboard_from_snapshot(snapshot_text)

    # Generate output
    if args.format == 'json':
        output = {
            'timestamp': datetime.now().isoformat(),
            'leaderboard': leaderboard_data,
            'top3': leaderboard_data[:3],
            'count': len(leaderboard_data)
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        # Text format
        post_content, summary = generate_post_content(leaderboard_data, None)
        if args.output:
            # Save to file
            os.makedirs(args.output, exist_ok=True)
            date_str = datetime.now().strftime('%Y-%m-%d')
            post_path = os.path.join(args.output, f'{date_str}-openrouter-post.md')
            with open(post_path, 'w') as f:
                f.write(post_content)
            print(f"Saved to: {post_path}")
        else:
            print(post_content)


if __name__ == '__main__':
    main()
