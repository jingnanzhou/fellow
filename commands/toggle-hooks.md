# Toggle Fellow Hooks

Enable or disable automatic context enrichment hooks.

## Usage

```bash
# Check current status
/toggle-hooks status

# Enable automatic enrichment
/toggle-hooks on

# Disable automatic enrichment
/toggle-hooks off
```

## What It Does

This command controls whether Fellow automatically intercepts and enriches coding requests.

- **When enabled**: Coding requests are automatically enriched with semantic knowledge from the knowledge base
- **When disabled**: All requests pass through unchanged (use `/fellow` command for explicit enrichment)

## Implementation

```bash
# Get the directory where Fellow plugin is installed
# This needs to work regardless of where Claude Code is run from

find_plugin_dir() {
  # Method 1: Check if we're in the plugin development directory
  if [ -f ".claude-plugin/plugin.json" ]; then
    local plugin_name=$(grep -o '"name":\s*"[^"]*"' .claude-plugin/plugin.json | head -1 | cut -d'"' -f4)
    if [ "$plugin_name" = "fellow" ]; then
      echo "$(pwd)"
      return 0
    fi
  fi

  # Method 2: Search Claude Code's plugin installation directories
  local installed_plugins="$HOME/.claude/plugins/installed_plugins.json"
  if [ -f "$installed_plugins" ]; then
    # Extract Fellow's install path from installed_plugins.json
    local install_path=$(grep -A 2 '"fellow@' "$installed_plugins" | grep '"installPath"' | cut -d'"' -f4)
    if [ -n "$install_path" ] && [ -d "$install_path" ]; then
      echo "$install_path"
      return 0
    fi
  fi

  # Method 3: Search common plugin cache locations
  for cache_dir in "$HOME/.claude/plugins/cache"/*; do
    if [ -d "$cache_dir/fellow" ]; then
      # Find the latest version
      local latest_version=$(ls -1 "$cache_dir/fellow" | sort -V | tail -1)
      if [ -n "$latest_version" ]; then
        echo "$cache_dir/fellow/$latest_version"
        return 0
      fi
    fi
  done

  return 1
}

# Find the plugin directory
PLUGIN_DIR=$(find_plugin_dir)
if [ -z "$PLUGIN_DIR" ]; then
  echo "⚠️  Could not locate Fellow plugin directory"
  echo "   Searched in:"
  echo "   - Current directory (development mode)"
  echo "   - ~/.claude/plugins/installed_plugins.json"
  echo "   - ~/.claude/plugins/cache/*"
  exit 1
fi

# Get the hook configuration file from Fellow plugin directory
HOOKS_FILE="$PLUGIN_DIR/.claude-plugin/hooks.json"

# Parse the command
case "$1" in
  status)
    # Show current status
    if [ -f "$HOOKS_FILE" ]; then
      ENABLED=$(grep -o '"enabled":\s*\(true\|false\)' "$HOOKS_FILE" | head -1)
      if [[ "$ENABLED" == *"true"* ]]; then
        echo "✅ Fellow hooks are ENABLED"
        echo "   Coding requests will be automatically enriched with context"
        echo ""
        echo "To disable: /toggle-hooks off"
      else
        echo "❌ Fellow hooks are DISABLED"
        echo "   Use /fellow command for explicit enrichment"
        echo ""
        echo "To enable: /toggle-hooks on"
      fi
    else
      echo "⚠️  Hook configuration not found at: $HOOKS_FILE"
    fi
    ;;

  on|enable)
    # Enable hooks
    if [ -f "$HOOKS_FILE" ]; then
      # Use sed to replace enabled: false with enabled: true
      sed -i.bak 's/"enabled":\s*false/"enabled": true/' "$HOOKS_FILE"
      echo "✅ Fellow hooks ENABLED"
      echo "   Coding requests will now be automatically enriched with context"
    else
      echo "⚠️  Hook configuration not found at: $HOOKS_FILE"
      exit 1
    fi
    ;;

  off|disable)
    # Disable hooks
    if [ -f "$HOOKS_FILE" ]; then
      # Use sed to replace enabled: true with enabled: false
      sed -i.bak 's/"enabled":\s*true/"enabled": false/' "$HOOKS_FILE"
      echo "❌ Fellow hooks DISABLED"
      echo "   Automatic enrichment is now off"
      echo "   Use /fellow command for explicit enrichment when needed"
    else
      echo "⚠️  Hook configuration not found at: $HOOKS_FILE"
      exit 1
    fi
    ;;

  *)
    echo "Usage: /toggle-hooks [status|on|off]"
    echo ""
    echo "Commands:"
    echo "  status  - Show current hook status"
    echo "  on      - Enable automatic context enrichment"
    echo "  off     - Disable automatic context enrichment"
    exit 1
    ;;
esac
```

## Examples

### Check Status
```bash
/toggle-hooks status
```

Output:
```
✅ Fellow hooks are ENABLED
   Coding requests will be automatically enriched with context

To disable: /toggle-hooks off
```

### Disable Hooks Temporarily
```bash
/toggle-hooks off
```

Output:
```
❌ Fellow hooks DISABLED
   Automatic enrichment is now off
   Use /fellow command for explicit enrichment when needed
```

### Re-enable Hooks
```bash
/toggle-hooks on
```

Output:
```
✅ Fellow hooks ENABLED
   Coding requests will now be automatically enriched with context
```

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

## Manual Alternative

You can also manually edit `.claude-plugin/hooks.json`:

```json
{
  "hooks": [
    {
      "name": "fellow-context-enrichment",
      "enabled": false,  // Change to true/false
      ...
    }
  ]
}
```

## Notes

- Changes take effect immediately (no restart needed in most cases)
- When disabled, you can still use `/fellow` command for explicit enrichment
- Status is persisted across Claude Code sessions
- Hook configuration is specific to Fellow plugin directory
