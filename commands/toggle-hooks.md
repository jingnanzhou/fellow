---
description: Toggle Fellow hooks on/off for automatic context enrichment
argument-hint: "[status|on|off]"
---

# Toggle Fellow Hooks

Enable or disable automatic context enrichment hooks.

## Objective

Control whether Fellow automatically intercepts and enriches coding requests:
- **When enabled**: Coding requests are automatically enriched with semantic knowledge from the knowledge base
- **When disabled**: All requests pass through unchanged (use `/fellow` command for explicit enrichment)

---

## Arguments

- **$ARGUMENTS** (optional): The action to perform
  - `status` - Show current hook status (default if no argument provided)
  - `on` or `enable` - Enable automatic context enrichment
  - `off` or `disable` - Disable automatic context enrichment

---

## Implementation

**CRITICAL**: This is an EXECUTABLE command, not documentation. You MUST execute the Python tool, not display its contents.

### Step 1: Execute the toggle_hooks.py tool

Run the following command to toggle the hooks:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/toggle_hooks.py $ARGUMENTS
```

**Important**:
- Replace `$ARGUMENTS` with the actual argument provided by the user (status/on/off)
- If no argument provided, use "status" as default
- The script will output status messages directly - do NOT add additional commentary
- Simply show the output from the script to the user

### Step 2: Display Output

The script will output appropriate messages:
- For `status`: Shows whether hooks are enabled or disabled
- For `on`: Confirms hooks have been enabled
- For `off`: Confirms hooks have been disabled

**Do NOT**:
- Display the Python script contents
- Display bash script alternatives
- Add extra explanations beyond the script output
- Show implementation details

---

## Examples

### Check Status
```
/fellow:toggle-hooks status
```

Expected behavior: Execute `python3 ${CLAUDE_PLUGIN_ROOT}/tools/toggle_hooks.py status` and show its output

### Enable Hooks
```
/fellow:toggle-hooks on
```

Expected behavior: Execute `python3 ${CLAUDE_PLUGIN_ROOT}/tools/toggle_hooks.py on` and show its output

### Disable Hooks
```
/fellow:toggle-hooks off
```

Expected behavior: Execute `python3 ${CLAUDE_PLUGIN_ROOT}/tools/toggle_hooks.py off` and show its output

---

## Use Cases

**Disable hooks when:**
- Working on non-Fellow projects (no KB available)
- Testing code without architectural constraints
- Pair programming and want explicit control
- Debugging hook behavior

**Enable hooks when:**
- Working on projects with established knowledge base
- Want automatic architectural guardrails
- Need consistent pattern enforcement
- Active development on familiar codebase

---

## Notes

- Changes take effect immediately (no restart needed)
- When disabled, you can still use `/fellow` command for explicit enrichment
- Status is persisted across Claude Code sessions
- Configuration is stored in `.claude-plugin/hooks.json`
