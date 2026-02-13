#!/bin/bash
# OpenClaw Update Checker Script
# This is a simple wrapper that delegates the actual work to the OpenClaw agent

OUTPUT_DIR="${1:-/Users/wangziyi/Desktop/openclaw-update}"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# The actual checking logic will be handled by the OpenClaw agent
# This script is primarily for environment setup if needed

echo "Checking OpenClaw updates..."
echo "Output directory: $OUTPUT_DIR"
