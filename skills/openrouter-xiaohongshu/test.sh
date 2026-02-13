#!/bin/bash
# Test script for openrouter-xiaohongshu skill

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$BASE_DIR/scripts"

echo "=== OpenRouter Xiaohongshu Skill Test ==="
echo "Base directory: $BASE_DIR"
echo ""

# Test fetch_data.py with sample snapshot
echo "Test 1: Testing fetch_data.py..."
cat > /tmp/test_snapshot.txt << 'EOF'
- generic [ref=e482]:
  - generic [ref=e483]:
    - generic [ref=e484]: "1."
    - generic [ref=e486]:
      - link "Kimi K2.5" [ref=e487] [cursor=pointer]:
        - /url: /moonshotai/kimi-k2.5
      - generic [ref=e488]:
        - text: by
        - link "moonshotai" [ref=e489] [cursor=pointer]:
          - /url: /moonshotai
    - generic [ref=e490]: 334Btokens
  - generic [ref=e491]:
    - generic [ref=e492]: "2."
    - generic [ref=e494]:
      - link "Trinity Large Preview (free)" [ref=e495] [cursor=pointer]:
        - /url: /arcee-ai/trinity-large-preview
      - generic [ref=e496]:
        - text: by
        - link "arcee-ai" [ref=e497] [cursor=pointer]:
          - /url: /arcee-ai
    - generic [ref=e498]: 185Btokens
  - generic [ref=e499]:
    - generic [ref=e500]: "3."
    - generic [ref=e502]:
      - link "Gemini 3 Flash Preview" [ref=e503] [cursor=pointer]:
        - /url: /google/gemini-3-flash-preview
      - generic [ref=e504]:
        - text: by
        - link "google" [ref=e505] [cursor=pointer]:
          - /url: /google
    - generic [ref=e506]: 173Btokens
  - generic [ref=e507]:
    - generic [ref=e508]: "4."
    - generic [ref=e510]:
      - link "Claude Sonnet 4.5" [ref=e511] [cursor=pointer]:
        - /url: /anthropic/claude-sonnet-4.5
      - generic [ref=e512]:
        - text: by
        - link "anthropic" [ref=e513] [cursor=pointer]:
          - /url: /anthropic
    - generic [ref=e514]: 71.2Btokens
  - generic [ref=e515]:
    - generic [ref=e516]: "5."
    - generic [ref=e518]:
      - link "Step 3.5 Flash" [ref=e519] [cursor=pointer]:
        - /url: /stepfun/step-3.5-flash
      - generic [ref=e520]:
        - text: by
        - link "stepfun" [ref=e521] [cursor=pointer]:
          - /url: /stepfun
    - generic [ref=e522]: 66.6Btokens
EOF

python3 "$SCRIPTS_DIR/fetch_data.py" --snapshot /tmp/test_snapshot.txt --format json

echo ""
echo "Test 2: Testing generate_post.py..."
python3 "$SCRIPTS_DIR/generate_post.py" --snapshot /tmp/test_snapshot.txt --output /tmp/test-output

echo ""
echo "=== Test Complete ==="
echo "Check output in /tmp/test-output/"
