# Claude Code Hooks Collection

This directory contains example Claude Code hooks that demonstrate various capabilities and use cases.

## Available Hooks

### 🔍 command_logger.sh
**Purpose**: Logs all Bash commands executed by Claude to `~/.claude/logs/commands.log`
**Event**: PreToolUse
**Matcher**: Bash

### 🛡️ safety_guard.sh
**Purpose**: Blocks potentially dangerous commands that could harm your system
**Event**: PreToolUse
**Matcher**: Bash
**Features**:
- Blocks destructive commands (rm -rf /, mkfs, dd, etc.)
- Warns about sudo usage
- Returns clear error messages

### ✨ python_formatter.sh
**Purpose**: Automatically formats Python files with Black after editing
**Event**: PostToolUse
**Matcher**: Write|Edit|MultiEdit
**Requirements**: `pip install black`

### 📝 context_injector.py
**Purpose**: Adds project-specific context to user prompts
**Event**: UserPromptSubmit
**Matcher**: *
**Features**:
- Detects project type (Python, Node.js, Rust)
- Adds git branch information
- Includes working directory context

### 🧪 test_runner.sh
**Purpose**: Automatically runs tests after code changes
**Event**: PostToolUse
**Matcher**: Write|Edit|MultiEdit
**Features**:
- Detects Python and JavaScript test files
- Runs appropriate test framework
- Reports test results

## Installation

1. **Copy hooks to your Claude configuration directory:**
   ```bash
   cp -r .claude/hooks ~/.claude/
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x ~/.claude/hooks/*.sh ~/.claude/hooks/*.py
   ```

3. **Configure hooks in settings.json:**
   
   Copy relevant sections from `example-settings.json` to your `~/.claude/settings.json`:
   ```bash
   # View example configuration
   cat ~/.claude/hooks/example-settings.json
   
   # Edit your settings
   nano ~/.claude/settings.json
   ```

4. **Test hooks before enabling:**
   ```bash
   # Test a specific hook
   ~/.claude/hooks/test_hook.sh ~/.claude/hooks/safety_guard.sh dangerous_command
   ```

## Testing Hooks

Use the included test script to validate hooks before deployment:

```bash
# Basic test
./test_hook.sh <hook_script> basic

# Test specific scenarios
./test_hook.sh safety_guard.sh dangerous_command
./test_hook.sh command_logger.sh bash_command
./test_hook.sh python_formatter.sh python_edit
```

Available test cases:
- `basic` - Simple Read tool test
- `bash_command` - Bash command execution
- `dangerous_command` - Dangerous command blocking
- `python_edit` - Python file editing
- `user_prompt` - User prompt submission

## Creating Custom Hooks

### Basic Structure
```bash
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool // ""')

# Your logic here

exit 0  # Success
# exit 2  # Block operation
```

### JSON Response (Advanced)
```json
{
  "action": "continue|block|modify",
  "message": "Optional message",
  "modifiedInput": {
    "parameters": {}
  }
}
```

## Security Considerations

⚠️ **IMPORTANT**: Hooks run with your full system permissions!

- Always validate and sanitize inputs
- Use absolute paths for commands
- Add timeouts to prevent hanging
- Test thoroughly before enabling
- Review hook code before installation
- Be cautious with hooks that modify data

## Troubleshooting

### Hook not executing
- Check file permissions: `ls -la ~/.claude/hooks/`
- Verify path in settings.json
- Check matcher pattern matches tool name
- Look for syntax errors in JSON

### Hook blocking unexpectedly
- Test with test_hook.sh
- Check exit codes (only 2 blocks)
- Validate JSON output format
- Review conditional logic

### Performance issues
- Add timeouts to long-running commands
- Use background processing for heavy tasks
- Cache frequently accessed data
- Optimize script logic

## Examples in Production

### Enable logging and safety for all projects
Add to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "~/.claude/hooks/command_logger.sh"},
          {"type": "command", "command": "~/.claude/hooks/safety_guard.sh"}
        ]
      }
    ]
  }
}
```

### Enable Python formatting for specific project
Add to `.claude/settings.json` in project root:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "^(Write|Edit|MultiEdit)$",
        "hooks": [
          {"type": "command", "command": ".claude/hooks/python_formatter.sh"}
        ]
      }
    ]
  }
}
```

## Contributing

Feel free to submit additional hooks or improvements! Consider:
- Clear documentation
- Error handling
- Performance optimization
- Security validation
- Cross-platform compatibility

## License

These example hooks are provided as-is for educational purposes. Use at your own risk.