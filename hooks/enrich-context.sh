#!/bin/bash
#
# Fellow Context Enrichment Hook
#
# This hook automatically intercepts coding requests and enriches them with
# semantic knowledge from the knowledge base.
#
# Hook Type: user-prompt-submit
# Trigger: Before user prompt is processed by Claude
# Purpose: Add architectural context, constraints, and guardrails

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# User's prompt is passed as argument or via stdin
USER_PROMPT="${1:-$(cat)}"

# Check if Python enrichment script exists
ENRICH_SCRIPT="$SCRIPT_DIR/enrich-context.py"
if [ ! -f "$ENRICH_SCRIPT" ]; then
    echo "Error: Enrichment script not found at $ENRICH_SCRIPT" >&2
    exit 1
fi

# Run the Python enrichment script
# It will:
# 1. Analyze the user's prompt
# 2. Check for knowledge base
# 3. Load relevant knowledge
# 4. Generate enriched context
# 5. Output enriched prompt or original if no KB

python3 "$ENRICH_SCRIPT" "$USER_PROMPT"
