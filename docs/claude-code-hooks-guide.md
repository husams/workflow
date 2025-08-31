# Claude Code Hooks - Complete Implementation Guide

## Overview
Claude Code hooks are shell commands that execute automatically at specific points during Claude's interaction workflow. They provide deterministic control over Claude's behavior, enabling validation, logging, context injection, and custom workflows.

## Hook Events

### 1. PreToolUse
Executes before any tool is called.
- **Use cases**: Validate commands, log operations, block dangerous actions
- **Input**: Tool name, parameters, session context
- **Can block**: Yes (exit code 2)

### 2. PostToolUse
Executes after a tool completes.
- **Use cases**: Process results, trigger follow-up actions, log outputs
- **Input**: Tool name, parameters, result, session context
- **Can block**: No

### 3. UserPromptSubmit
Executes when user submits a prompt.
- **Use cases**: Add context, validate inputs, inject instructions
- **Input**: User prompt, session context
- **Can modify prompt**: Yes (via JSON output)

### 4. Notification
Triggered by system notifications.
- **Use cases**: Custom alerts, desktop notifications, logging
- **Input**: Notification content, type
- **Can block**: No

### 5. SessionStart
Executes when Claude session begins.
- **Use cases**: Initialize environment, load context, set variables
- **Input**: Session ID, timestamp
- **Can block**: No

### 6. SessionEnd
Executes when Claude session ends.
- **Use cases**: Cleanup, save state, generate reports
- **Input**: Session ID, duration, summary
- **Can block**: No

### 7. Stop
Executes when main agent finishes task.
- **Use cases**: Final validation, summary generation
- **Input**: Task result, metrics
- **Can block**: No

### 8. SubagentStop
Executes when a subagent completes.
- **Use cases**: Validate subagent output, chain workflows
- **Input**: Subagent name, result
- **Can block**: No

### 9. PreCompact
Executes before context compaction.
- **Use cases**: Save important context, optimize memory
- **Input**: Current context size
- **Can block**: No

## Configuration Structure

### Basic Hook Configuration
Location: `~/.claude/settings.json`

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "path/to/your/script.sh"
          }
        ]
      }
    ]
  }
}
```

### Matcher Patterns
- **Exact match**: `"Bash"` - matches only Bash tool
- **Wildcard**: `"*"` - matches all tools
- **Regex**: `"^(Read|Write)$"` - matches Read or Write tools
- **Glob**: `"mcp__*"` - matches all MCP tools

## Hook Input/Output

### Input Format (via stdin)
```json
{
  "sessionId": "unique-session-id",
  "timestamp": 1234567890,
  "event": "PreToolUse",
  "tool": "Bash",
  "parameters": {
    "command": "ls -la"
  },
  "context": {
    "workingDirectory": "/path/to/project",
    "user": "username"
  }
}
```

### Output Options

#### 1. Simple Exit Code
- `0`: Success, continue normally
- `2`: Block operation with error
- Other: Treated as success

#### 2. JSON Output (Advanced)
```json
{
  "action": "continue|block|modify",
  "message": "Optional feedback message",
  "modifiedInput": {
    "parameters": {
      "command": "modified command"
    }
  },
  "additionalContext": "Extra information to add"
}
```

## Practical Examples

### Example 1: Command Logger
**Purpose**: Log all Bash commands to a file

**Hook Script** (`~/.claude/hooks/log_commands.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // ""')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Command: $COMMAND" >> ~/.claude/command_log.txt
exit 0
```

**Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/log_commands.sh"
          }
        ]
      }
    ]
  }
}
```

### Example 2: Dangerous Command Blocker
**Purpose**: Block potentially dangerous commands

**Hook Script** (`~/.claude/hooks/safety_check.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // ""')

# Check for dangerous patterns
if echo "$COMMAND" | grep -qE '(rm -rf /|dd if=|mkfs|fdisk)'; then
    echo '{"action": "block", "message": "Dangerous command blocked for safety"}'
    exit 2
fi

exit 0
```

### Example 3: Auto-formatter
**Purpose**: Automatically format Python files after editing

**Hook Script** (`~/.claude/hooks/auto_format.py`):
```python
#!/usr/bin/env python3
import json
import sys
import subprocess
import os

def main():
    input_data = json.load(sys.stdin)
    
    if input_data.get('tool') in ['Write', 'Edit', 'MultiEdit']:
        file_path = input_data.get('parameters', {}).get('file_path', '')
        
        if file_path.endswith('.py'):
            # Run black formatter
            subprocess.run(['black', file_path], capture_output=True)
            print(json.dumps({
                "action": "continue",
                "message": f"Auto-formatted {os.path.basename(file_path)} with Black"
            }))
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Configuration**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "^(Write|Edit|MultiEdit)$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/auto_format.py"
          }
        ]
      }
    ]
  }
}
```

### Example 4: Context Injector
**Purpose**: Add project-specific context to every prompt

**Hook Script** (`~/.claude/hooks/inject_context.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // ""')

# Add project context
CONTEXT="Remember: Follow our coding standards - use 4 spaces for indentation, include type hints, and write tests for all new functions."

OUTPUT=$(jq -n \
  --arg prompt "$PROMPT" \
  --arg context "$CONTEXT" \
  '{
    "action": "modify",
    "modifiedInput": {
      "prompt": ($context + "\n\n" + $prompt)
    }
  }')

echo "$OUTPUT"
exit 0
```

### Example 5: Test Runner
**Purpose**: Automatically run tests after code changes

**Hook Script** (`~/.claude/hooks/run_tests.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool // ""')
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // ""')

if [[ "$TOOL" =~ ^(Write|Edit|MultiEdit)$ ]] && [[ "$FILE_PATH" =~ \.py$ ]]; then
    # Extract module name from file path
    MODULE=$(basename "$FILE_PATH" .py)
    
    # Run tests for the module
    if [ -f "tests/test_$MODULE.py" ]; then
        pytest "tests/test_$MODULE.py" -q
        if [ $? -ne 0 ]; then
            echo '{"action": "continue", "message": "Warning: Tests failed after edit"}'
        fi
    fi
fi

exit 0
```

## Advanced Hook Patterns

### Chain Multiple Hooks
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/log_commands.sh"
          },
          {
            "type": "command",
            "command": "~/.claude/hooks/safety_check.sh"
          }
        ]
      }
    ]
  }
}
```

### Conditional Hooks Based on Environment
```bash
#!/bin/bash
INPUT=$(cat)

# Only run in production environment
if [ "$ENVIRONMENT" = "production" ]; then
    # Strict validation
    exit 2
fi

exit 0
```

### Hook with External API Integration
```python
#!/usr/bin/env python3
import json
import sys
import requests

def main():
    input_data = json.load(sys.stdin)
    
    # Send notification to Slack
    if input_data.get('event') == 'SessionEnd':
        webhook_url = os.environ.get('SLACK_WEBHOOK')
        if webhook_url:
            requests.post(webhook_url, json={
                "text": f"Claude session completed: {input_data.get('sessionId')}"
            })
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Testing Hooks

### Test Script Template
```bash
#!/bin/bash
# test_hook.sh - Test your hook with sample input

HOOK_SCRIPT="$1"
TEST_INPUT='{
  "sessionId": "test-123",
  "event": "PreToolUse",
  "tool": "Bash",
  "parameters": {
    "command": "ls -la"
  }
}'

echo "Testing hook: $HOOK_SCRIPT"
echo "$TEST_INPUT" | $HOOK_SCRIPT
echo "Exit code: $?"
```

### Debugging Tips
1. **Log everything**: Add logging to understand hook behavior
2. **Test independently**: Run hooks manually before configuring
3. **Use verbose output**: Include detailed messages in responses
4. **Check permissions**: Ensure scripts are executable (`chmod +x`)
5. **Validate JSON**: Use `jq` to validate input/output JSON

## Security Best Practices

### 1. Input Validation
```bash
#!/bin/bash
INPUT=$(cat)

# Validate JSON structure
if ! echo "$INPUT" | jq empty 2>/dev/null; then
    exit 1
fi

# Sanitize inputs
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // ""' | sed 's/[;&|]//g')
```

### 2. Use Absolute Paths
```bash
# Good
/usr/local/bin/black "$FILE_PATH"

# Bad - vulnerable to PATH manipulation
black "$FILE_PATH"
```

### 3. Limit Permissions
```bash
# Run hooks with restricted permissions
sudo -u limited_user /path/to/hook.sh
```

### 4. Timeout Protection
```bash
#!/bin/bash
timeout 5s /path/to/actual_hook.sh
if [ $? -eq 124 ]; then
    echo "Hook timed out" >&2
    exit 1
fi
```

### 5. Audit and Monitoring
```bash
# Log all hook executions
echo "$(date): Hook executed by $(whoami)" >> /var/log/claude_hooks.log
```

## Common Use Cases

1. **Development Workflow**
   - Auto-format code
   - Run linters
   - Execute tests
   - Update documentation

2. **Security & Compliance**
   - Block sensitive file access
   - Audit command execution
   - Enforce coding standards
   - Validate credentials

3. **Team Collaboration**
   - Send notifications
   - Update task tracking
   - Generate reports
   - Sync with CI/CD

4. **Learning & Improvement**
   - Log common patterns
   - Track error frequencies
   - Measure performance
   - Gather metrics

## Troubleshooting

### Hook Not Executing
- Check configuration syntax in `settings.json`
- Verify script permissions (`chmod +x`)
- Ensure correct path to script
- Check matcher pattern matches tool name

### Hook Blocking Unexpectedly
- Review exit codes (only 2 blocks)
- Check JSON output format
- Validate conditional logic
- Test with simpler input

### Performance Issues
- Add timeouts to prevent hanging
- Optimize script execution
- Use async processing for heavy tasks
- Cache frequently accessed data

## Summary

Claude Code hooks provide powerful customization capabilities:
- **Control**: Validate and modify Claude's actions
- **Automation**: Trigger workflows automatically
- **Integration**: Connect with external systems
- **Security**: Enforce policies and restrictions
- **Monitoring**: Track and audit all operations

Remember: **USE AT YOUR OWN RISK** - Always test hooks thoroughly in a safe environment before production use.