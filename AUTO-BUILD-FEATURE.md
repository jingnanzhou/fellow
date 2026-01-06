# Auto-Build Knowledge Base Feature

Fellow now includes automatic knowledge base building for a seamless first-time experience.

## What Is Auto-Build?

When you try to use Fellow's context enrichment without having built a knowledge base first, Fellow will:

1. **Detect the missing knowledge base**
2. **Inform you it will take 2-5 minutes**
3. **Offer to build it automatically**
4. **Build the KB and then proceed** with your original request

## How It Works

### Scenario 1: Using Automatic Enrichment (Hooks)

When hooks are enabled and you make a coding request:

```
You: "Add authentication to the user endpoint"

Fellow (detecting no KB):
⚠️  Fellow Knowledge Base Not Found

Fellow detected a coding request but couldn't find a knowledge base for this project.

To enable context enrichment:
1. Build the knowledge base: `/build-kb`
   (Takes 2-5 minutes for first extraction)

Or continue without enrichment:
Your request will proceed without Fellow's architectural context.
```

The request proceeds without enrichment, but you know what to do.

### Scenario 2: Using Manual Command

When you explicitly use `/fellow` command:

```
You: /fellow Add authentication to the user endpoint

Fellow:
⚠️  Fellow Knowledge Base Not Found

This appears to be the first time using Fellow on this project.
To enable context enrichment, Fellow needs to extract semantic knowledge
from your codebase.

Project directory: /path/to/your/project
Time required: 2-5 minutes (one-time process)

Would you like to build the knowledge base now?

Options:
1. Build now (recommended) - Fellow will extract knowledge automatically
2. Cancel and build later - Run `/build-kb` manually when ready

Build knowledge base now? (y/n):
```

**If you choose "yes":**

```
🔨 Building Knowledge Base

Project: /path/to/your/project
This will take 2-5 minutes...

[/build-kb executes automatically]

✓ Knowledge base built successfully!

Proceeding with your original request: "Add authentication to the user endpoint"

[Fellow now enriches and proceeds with your request]
```

**If you choose "no":**

```
ℹ️  Knowledge base build cancelled.

To use Fellow later:
1. Run `/build-kb` to extract knowledge (2-5 minutes)
2. Then use `/fellow` or enable automatic enrichment

Your request will proceed without enrichment.
```

## Benefits

### 1. No Confusing Errors

**Before:**
```
Error: Knowledge base not found at .fellow-data/semantic/
```

**After:**
```
⚠️  Fellow Knowledge Base Not Found

Fellow detected a coding request but couldn't find a knowledge base...
[Helpful instructions provided]
```

### 2. Smooth Onboarding

New users don't need to know about `/build-kb` upfront. They can:
1. Install Fellow
2. Start coding
3. Fellow guides them through KB creation when needed

### 3. Context-Aware Guidance

Fellow explains:
- **Why** KB is needed (enable context enrichment)
- **How long** it takes (2-5 minutes)
- **What to do** (build now or later)
- **What happens** (request proceeds with or without enrichment)

## Implementation Details

### Components

**1. Hook Detection** (`hooks/enrich-context.py`):
- Detects missing KB when intercepting requests
- Displays helpful message to stderr
- Allows request to proceed without enrichment

**2. Command Auto-Build** (`commands/fellow.md`):
- Enhanced Phase 1 to check for KB
- Prompts user to build if missing
- Automatically triggers `/build-kb` if user agrees
- Proceeds with enrichment after build completes

**3. Auto-Build Helper** (`hooks/auto_build_kb.py`):
- Shared utility for KB detection
- Displays consistent messages
- Handles user prompting
- Triggers KB build

### Configuration

**Enable/Disable Auto-Build**

Auto-build can be controlled via configuration:

**In `.claude-plugin/hooks.json`:**
```json
{
  "hooks": [{
    "config": {
      "auto_build_kb": true,    // Enable auto-build prompts
      "auto_build_on_command": true,  // Auto-build for /fellow
      "auto_build_on_hook": false     // Don't auto-build for hooks (just notify)
    }
  }]
}
```

**Default behavior:**
- `/fellow` command: Prompts and auto-builds
- Hooks: Notifies but doesn't interrupt (avoids breaking user flow)

## User Experience Examples

### Example 1: First-Time User

```bash
# User installs Fellow
cd fellow
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace

# User starts coding without building KB
claude

You: "Add rate limiting to the API endpoint"

Fellow:
⚠️  Fellow Knowledge Base Not Found

Fellow detected a coding request but couldn't find a knowledge base for this project.

To enable context enrichment:
1. Build the knowledge base: `/build-kb`
   (Takes 2-5 minutes for first extraction)

Or continue without enrichment:
Your request will proceed without Fellow's architectural context.

# User now knows to run /build-kb
You: /build-kb

[KB builds in 3 minutes]

✓ Knowledge base built successfully!

# Now automatic enrichment works
You: "Add rate limiting to the API endpoint"

📋 Context from Knowledge Base

Relevant Entities:
- RateLimiter (class): Redis-based rate limiting
...
```

### Example 2: Experienced User with Manual Command

```bash
# User knows about Fellow and uses /fellow directly
You: /fellow Refactor the authentication service

Fellow:
⚠️  Fellow Knowledge Base Not Found

This appears to be the first time using Fellow on this project.
...

Would you like to build the knowledge base now? (y/n): y

🔨 Building Knowledge Base

Project: /path/to/your/project
This will take 2-5 minutes...

[Automatic extraction runs]

✓ Knowledge base built successfully!

Proceeding with your original request: "Refactor the authentication service"

📋 Context from Knowledge Base
...
```

### Example 3: User Who Wants to Wait

```bash
You: /fellow Add caching layer

Fellow:
Would you like to build the knowledge base now? (y/n): n

ℹ️  Knowledge base build cancelled.

To use Fellow later:
1. Run `/build-kb` to extract knowledge (2-5 minutes)
2. Then use `/fellow` or enable automatic enrichment

Your request will proceed without enrichment.

# Request proceeds without Fellow's context
# User can build KB later when convenient
```

## Best Practices

### For Plugin Developers

1. **Always check for KB** before attempting enrichment
2. **Provide clear guidance** when KB is missing
3. **Don't interrupt user flow** unnecessarily (hooks should notify, not block)
4. **Make building easy** - one command, clear instructions

### For Users

1. **Build KB upfront** for best experience:
   ```bash
   cd /path/to/your/project
   /build-kb
   ```

2. **Use auto-build** for convenience:
   ```bash
   /fellow <your request>
   # Accept auto-build when prompted
   ```

3. **Update KB after changes**:
   ```bash
   /build-kb --update  # Fast incremental update
   ```

## Technical Details

### KB Detection Logic

```python
def find_knowledge_base(start_dir: Optional[Path] = None) -> Optional[Path]:
    """Search upward for .fellow-data/semantic/"""
    current = start_dir or Path.cwd()
    for _ in range(10):  # Up to 10 levels
        kb_dir = current / '.fellow-data' / 'semantic'
        if kb_dir.exists() and has_kb_files(kb_dir):
            return kb_dir
        if current.parent == current:  # Root
            break
        current = current.parent
    return None
```

### Auto-Build Trigger

When user agrees to build:

1. **Display progress message**
2. **Execute `/build-kb` command** internally
3. **Wait for completion**
4. **Verify KB was created**
5. **Proceed with original request**

### Error Handling

- **Build fails**: Display error, offer to retry or continue without enrichment
- **User cancels**: Proceed without enrichment, show how to build later
- **KB corrupted**: Offer to rebuild completely

## Configuration Options

```json
{
  "hooks": [{
    "config": {
      // Auto-build settings
      "auto_build_kb": true,              // Enable auto-build feature
      "auto_build_on_command": true,      // Auto-build for /fellow command
      "auto_build_on_hook": false,        // Auto-build for hooks (not recommended)
      "auto_build_timeout": 600,          // Max seconds for build (10 minutes)

      // Notification settings
      "notify_on_missing_kb": true,       // Show message when KB missing
      "notify_only_once_per_session": true // Avoid spam for hooks
    }
  }]
}
```

## Migration from Previous Versions

Previous versions required users to:
1. Learn about `/build-kb`
2. Manually run it before using Fellow
3. Remember to update it

New auto-build feature:
1. Automatically detects first use
2. Offers to build when needed
3. Guides user through process

**No breaking changes** - existing workflows still work!

## Future Enhancements

Potential improvements:

1. **Background building**: Start KB build in background while user continues working
2. **Smart rebuilding**: Auto-detect when KB is outdated and offer to update
3. **Progressive loading**: Load partial KB while building continues
4. **Multi-project awareness**: Detect related projects and share knowledge

## Summary

The auto-build feature makes Fellow:
- ✅ **Easier to use** - No need to read docs before starting
- ✅ **Self-documenting** - Explains itself when needed
- ✅ **Fail-safe** - Gracefully handles missing KB
- ✅ **Flexible** - User can build now or later
- ✅ **Non-intrusive** - Doesn't block user flow unnecessarily

**Result**: Better first-time user experience and higher adoption rate!

---

**Auto-build makes Fellow accessible to everyone, from first-time users to power users.**
