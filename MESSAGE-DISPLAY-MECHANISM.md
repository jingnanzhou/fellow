# Message Display Mechanism in Claude Code

## Understanding How Messages Appear in Chat

This document explains how hooks and commands communicate with users in Claude Code's chat interface.

## The Key Distinction

| Output Stream | Where It Goes | Visible in Chat? |
|---------------|---------------|------------------|
| **stdout** | Becomes part of the conversation | ✅ Yes - appears in chat |
| **stderr** | Goes to logs/terminal | ❌ No - only in logs |

## How Hooks Work

### Hook Execution Flow

```
User types: "Add authentication"
      ↓
Hook intercepts prompt
      ↓
Hook processes (enrich-context.py)
      ↓
Hook outputs to stdout → This becomes Claude's input
      ↓
Claude sees modified prompt
      ↓
Claude responds in chat
```

### Critical Rule for Hooks

**To display a message in chat, you MUST include it in stdout (the modified prompt)**

#### ❌ Wrong Way (Messages Don't Appear in Chat)

```python
# This goes to logs only - user won't see it!
print("⚠️ KB not found", file=sys.stderr)
print("Please run /build-kb", file=sys.stderr)

# Only the original prompt goes to Claude
print(user_prompt)
```

**Result:** User sees no warning, just their original request without enrichment

#### ✅ Right Way (Messages Appear in Chat)

```python
# Prepend warning to the prompt
warning = """⚠️ **Fellow Knowledge Base Not Found**

Please run `/build-kb` first.

---

**Original Request:**
"""

# Output warning + prompt to stdout
print(warning + user_prompt)
```

**Result:** User sees the warning in chat, followed by their request

### How It Appears in Chat

When hook outputs to stdout:

```
User: "Add authentication"

[Hook modifies prompt to include warning]

Claude sees and displays:
⚠️ **Fellow Knowledge Base Not Found**

Fellow detected a coding request but couldn't find a knowledge base.

To enable context enrichment:
1. Build the knowledge base: `/build-kb`

Or continue without enrichment.

---

**Original Request:**
Add authentication

[Claude then responds to this combined message]
```

## How Commands Work

### Command Execution Flow

```
User types: /fellow Add authentication
      ↓
Claude Code executes fellow.md agent
      ↓
Agent runs and outputs to conversation
      ↓
Everything agent says appears in chat
      ↓
User sees agent's full conversation
```

### Critical Rule for Commands

**All agent output automatically appears in chat**

#### Example: /fellow Command

**Agent's Response (All Visible in Chat):**

```markdown
⚠️  **Fellow Knowledge Base Not Found**

This appears to be the first time using Fellow on this project.

**This will take 2-5 minutes** (one-time process).

I can build the knowledge base now and then proceed with your request.

Would you like me to build it?
```

**User Response:** "Yes"

**Agent Continues:**

```markdown
🔨 Building Knowledge Base

[Executing /build-kb command...]

✓ Knowledge base built successfully!

Now proceeding with your original request: "Add authentication"

[Continues with enriched context...]
```

**Everything above appears in the chat interface**

## Implementation: Fellow's Message Strategy

### Hook Implementation (enrich-context.py)

**Current Implementation:**

```python
def main():
    user_prompt = get_user_prompt()

    # Detect coding request
    is_coding, intent, confidence = detect_coding_request(user_prompt)

    if not is_coding:
        # Not coding - pass through
        print(user_prompt)
        return

    # Find KB
    kb_dir = find_knowledge_base()

    if not kb_dir:
        # KB NOT FOUND - Show warning IN CHAT
        warning = """⚠️  **Fellow Knowledge Base Not Found**

Fellow detected a coding request but couldn't find a knowledge base.

**To enable context enrichment:**
1. Build the knowledge base: `/build-kb`
   (Takes 2-5 minutes)

**Or continue without enrichment:**
Your request will proceed without Fellow's context.

---

**Original Request:**
"""
        # Output to STDOUT (appears in chat)
        print(warning + user_prompt)
        return

    # KB found - proceed with enrichment
    enriched = enrich_with_context(user_prompt, kb_dir)
    print(enriched)  # Output enriched prompt to STDOUT
```

**Key Points:**
- Warning message prepended to user's prompt
- Goes to stdout → Claude sees it → Appears in chat
- User understands what happened and what to do

### Command Implementation (fellow.md)

**Phase 1: KB Detection and Auto-Build**

```markdown
### Phase 1: Knowledge Base Loading

1. Check if KB exists

2. If NOT found:
   - Say to user in chat:
     "⚠️ Knowledge base not found. I can build it now (takes 2-5 min).
      Would you like me to build it?"

3. If user says yes:
   - Say: "🔨 Building knowledge base..."
   - Execute /build-kb command
   - Say: "✓ KB built! Proceeding with your request..."
   - Continue with enrichment

4. If user says no:
   - Say: "Understood. To use Fellow later, run /build-kb.
      Proceeding without enrichment."
   - Continue without enrichment
```

**All of this conversation appears in the chat interface**

## Comparison: Before vs After Fix

### Before Fix (stderr)

**What happened:**
```python
# Hook code
print("⚠️ KB not found", file=sys.stderr)  # Goes to logs
print(user_prompt)  # Goes to Claude
```

**User experience:**
```
User: "Add authentication"

[No warning visible in chat]

Claude: [Generates code without Fellow's context]

User: "Why didn't Fellow help?" 🤔
```

**Logs showed:**
```
⚠️ KB not found
Please run /build-kb
```

But user never saw these messages!

### After Fix (stdout)

**What happens:**
```python
# Hook code
warning = "⚠️ KB not found. Run /build-kb first.\n\n"
print(warning + user_prompt)  # Goes to Claude
```

**User experience:**
```
User: "Add authentication"

[Warning appears in chat]
⚠️ Fellow Knowledge Base Not Found
Run /build-kb first.

Original Request: Add authentication

Claude: I understand. It looks like Fellow needs a knowledge base
        to provide context. As the message says, you should run
        /build-kb first. Would you like me to help with that?

User: [Now knows exactly what to do] ✅
```

## Best Practices

### For Hooks

1. **Always output to stdout for user-facing messages**
   ```python
   # User should see this
   print(message + user_prompt)  # stdout
   ```

2. **Use stderr only for debugging/logging**
   ```python
   # Debugging info
   print(f"Debug: confidence={conf}", file=sys.stderr)
   ```

3. **Format messages for chat display**
   ```python
   # Use markdown formatting
   message = "⚠️ **Warning**\n\nSomething happened.\n\n---\n\n"
   ```

### For Commands

1. **All agent output goes to chat automatically**
   - No need for special handling
   - Just write messages in the agent's response

2. **Format for readability**
   - Use headings, bullets, emoji
   - Break up long text
   - Use markdown formatting

3. **Make messages actionable**
   - Tell user what to do
   - Provide clear next steps
   - Ask for confirmation when needed

## Testing Message Display

### Test Hook Messages

```bash
# Test if messages appear in chat

# 1. Remove KB
rm -rf .fellow-data/

# 2. Make a coding request
claude

You: "Add authentication"

# Expected in chat:
# ⚠️ Fellow Knowledge Base Not Found
# [Full warning message]
# Original Request: Add authentication

# If you only see "Add authentication", messages went to logs (wrong!)
```

### Test Command Messages

```bash
# 1. Remove KB
rm -rf .fellow-data/

# 2. Use /fellow command
claude

You: /fellow Add authentication

# Expected in chat:
# ⚠️ Fellow Knowledge Base Not Found
# [Agent asks if you want to build]

# All agent conversation should be visible
```

## Debugging

### If Messages Don't Appear

**Check 1: Are you using stdout?**
```python
# Wrong
print("message", file=sys.stderr)

# Right
print("message")  # defaults to stdout
```

**Check 2: For hooks, is message part of output?**
```python
# The entire stdout becomes Claude's input
# Make sure warning is included
output = warning + user_prompt
print(output)
```

**Check 3: Test output directly**
```bash
# Run hook directly and check output
cd hooks
echo "Add auth" | python3 enrich-context.py

# You should see the warning in stdout, not stderr
```

## Summary

| Goal | Method | Stream | Visible in Chat? |
|------|--------|--------|------------------|
| **Show warning to user** | Include in prompt | stdout | ✅ Yes |
| **Debug/log info** | Log message | stderr | ❌ No |
| **Command conversation** | Agent output | (automatic) | ✅ Yes |
| **Hook enrichment** | Modified prompt | stdout | ✅ Yes |

**Key Takeaway:**

> **If you want users to see a message in the chat interface,
> it MUST go to stdout (or be part of the agent's conversation for commands)**

**stderr is only for logs!**

---

**Implementation Status: Fixed to use stdout for user-facing messages**
