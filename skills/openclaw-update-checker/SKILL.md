---
name: openclaw-update-checker
description: Check GitHub for OpenClaw releases and save update notes when new versions are available. Use when you need to: (1) Periodically check for OpenClaw updates, (2) Save changelog and user-focused highlights to a specified directory, (3) Track version history in markdown files.
---

# OpenClaw Update Checker

## Purpose

Periodically checks GitHub releases for OpenClaw and generates structured markdown files when new versions are released.

## Workflow

### Step 1: Check Current Version

Read the last checked version from the state file:
- Path: `{OUTPUT_DIR}/last-checked-version.json`
- Format: `{"lastVersion": "2026.2.9"}`

If the file doesn't exist, assume no prior checks have been made.

### Step 2: Fetch Latest Release

Use `web_fetch` to get the GitHub releases page:
- URL: `https://github.com/openclaw/openclaw/releases`

Extract the latest version number from the page (e.g., "openclaw 2026.2.9" → "2026.2.9").

### Step 3: Compare Versions

If the latest version matches `lastVersion`, no action needed.

If there's a new version, proceed to generate the update file.

### Step 4: Generate Update File

Create a markdown file named `{VERSION}.md` in `{OUTPUT_DIR}` (default: `/Users/wangziyi/Desktop/openclaw-update/`).

File structure:
```markdown
# OpenClaw 更新：{VERSION}

## 版本号
{VERSION}

## 详细内容
{FULL_CHANGELOG}

## 对大众用户的重点信息
{USER_FOCUSED_HIGHLIGHTS}

---
生成时间：{TIMESTAMP}
```

### Step 5: Extract Highlights

Analyze the changelog to identify user-focused information:

**Include:**
- New features that affect end users
- Important fixes for user-facing issues
- Breaking changes that impact usage
- Security improvements

**Exclude:**
- Internal refactoring
- Technical debt cleanup
- Build system changes
- Documentation-only updates
- Test/CI improvements

### Step 6: Update State

Update `last-checked-version.json` with the new version.

## Configuration

- **Output directory**: `/Users/wangziyi/Desktop/openclaw-update/` (unless specified otherwise)
- **State file**: `{OUTPUT_DIR}/last-checked-version.json`
- **File naming**: `{VERSION}.md`

## Execution

This skill is typically run via a cron job scheduled for daily execution (e.g., 9:00 AM).
