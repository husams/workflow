# Claude Code Universal Logging System

## Overview
A comprehensive Python-based logging system that tracks ALL Claude Code events with detailed information. Logs are stored in the project root directory under `.claude_logs/` with timestamps and full event details.

## Features

### 📊 Complete Event Coverage
- **PreToolUse** - Before any tool execution
- **PostToolUse** - After tool completion
- **UserPromptSubmit** - User input tracking
- **Notification** - System notifications
- **SessionStart/End** - Session lifecycle
- **Stop** - Main agent completion
- **SubagentStop** - Subagent completion
- **PreCompact** - Context compression events

### 📁 Log Files Structure
```
.claude_logs/
├── claude_events_YYYYMMDD.json      # Structured JSON logs
├── claude_events_YYYYMMDD.log       # Text format logs
├── activity_summary.json            # Aggregated statistics
├── pretooluse_YYYYMMDD.log         # Event-specific logs
├── posttooluse_YYYYMMDD.log
├── userpromptsubmit_YYYYMMDD.log
├── notification_YYYYMMDD.log
├── sessionstart_YYYYMMDD.log
├── sessionend_YYYYMMDD.log
├── stop_YYYYMMDD.log
├── subagentstop_YYYYMMDD.log
└── precompact_YYYYMMDD.log
```

### 📝 Logged Information

#### For All Events:
- Timestamp (ISO format and Unix)
- Event type
- Session ID
- Working directory
- User
- Python version
- Full event data

#### Tool-Specific Details:
- **Bash**: Commands executed, timeouts
- **File Operations**: File paths, existence checks
- **Read**: Offset and limit parameters
- **Edit/Write**: File modifications

#### Event-Specific Details:
- **UserPromptSubmit**: Prompt content and length
- **PostToolUse**: Success/failure, error messages
- **Session Events**: Duration, statistics
- **Agent Events**: Completion status, output preview

## Installation

### 1. Copy hooks to your project
```bash
# Copy the hooks directory to your project
cp -r .claude/hooks /path/to/your/project/.claude/
```

### 2. Make scripts executable
```bash
cd /path/to/your/project
chmod +x .claude/hooks/*.sh .claude/hooks/*.py
```

### 3. Configure Claude Code settings

Add to your `.claude/settings.json` in the project root:

```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_pretooluse.sh"}]}
    ],
    "PostToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_posttooluse.sh"}]}
    ],
    "UserPromptSubmit": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_userprompt.sh"}]}
    ],
    "Notification": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_notification.sh"}]}
    ],
    "SessionStart": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_sessionstart.sh"}]}
    ],
    "SessionEnd": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_sessionend.sh"}]}
    ],
    "Stop": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_stop.sh"}]}
    ],
    "SubagentStop": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_subagentstop.sh"}]}
    ],
    "PreCompact": [
      {"matcher": "*", "hooks": [{"type": "command", "command": ".claude/hooks/log_precompact.sh"}]}
    ]
  }
}
```

Or use the provided configuration:
```bash
# Copy the complete configuration
cp .claude/hooks/full_logging_settings.json .claude/settings.json
```

## Usage

### Viewing Logs

#### 1. Activity Summary
```bash
python3 .claude/hooks/log_viewer.py summary
```
Shows:
- Total events count
- Event type distribution
- Most used tools
- Files accessed
- Recent commands
- Error summary

#### 2. Recent Events
```bash
# Show last 20 events (default)
python3 .claude/hooks/log_viewer.py recent

# Show last 50 events
python3 .claude/hooks/log_viewer.py recent --count 50
```

#### 3. Search Logs
```bash
# Search for specific content
python3 .claude/hooks/log_viewer.py search --query "error"
python3 .claude/hooks/log_viewer.py search --query "file.py"
python3 .claude/hooks/log_viewer.py search --query "git commit"
```

#### 4. Performance Analysis
```bash
python3 .claude/hooks/log_viewer.py analyze
```
Shows:
- Tool execution statistics
- Success rates
- Event distribution
- Session analysis

#### 5. Export Logs
```bash
# Export to JSON
python3 .claude/hooks/log_viewer.py export --output my_logs.json

# Export to CSV
python3 .claude/hooks/log_viewer.py export --output my_logs.csv --format csv
```

### Direct Log Access

#### View today's JSON logs
```bash
cat .claude_logs/claude_events_$(date +%Y%m%d).json | jq .
```

#### View activity summary
```bash
cat .claude_logs/activity_summary.json | jq .
```

#### Tail real-time logs
```bash
tail -f .claude_logs/claude_events_$(date +%Y%m%d).log
```

#### View specific event type logs
```bash
# View all Bash commands executed today
cat .claude_logs/pretooluse_$(date +%Y%m%d).log | grep "Bash"

# View all file edits
cat .claude_logs/posttooluse_$(date +%Y%m%d).log | grep -E "Write|Edit"
```

## Log Structure Examples

### PreToolUse Event
```json
{
  "timestamp": "2025-08-31T15:53:50.790304",
  "unix_timestamp": 1234567890,
  "event_type": "PreToolUse",
  "session_id": "test-session-456",
  "working_directory": "/Users/user/project",
  "user": "username",
  "tool": "Bash",
  "parameters": {
    "command": "ls -la /tmp"
  },
  "command": "ls -la /tmp"
}
```

### PostToolUse Event
```json
{
  "timestamp": "2025-08-31T15:54:10.123456",
  "event_type": "PostToolUse",
  "tool": "Write",
  "parameters": {
    "file_path": "/path/to/file.py"
  },
  "file_path": "/path/to/file.py",
  "file_exists": false,
  "result": {
    "success": true
  },
  "success": true
}
```

### UserPromptSubmit Event
```json
{
  "timestamp": "2025-08-31T15:52:30.456789",
  "event_type": "UserPromptSubmit",
  "prompt": "Help me write a Python function",
  "prompt_length": 30,
  "prompt_preview": "Help me write a Python function"
}
```

## Activity Summary Structure

```json
{
  "total_events": 150,
  "events_by_type": {
    "PreToolUse": 50,
    "PostToolUse": 50,
    "UserPromptSubmit": 20,
    "SessionStart": 5,
    "SessionEnd": 5,
    "Stop": 10,
    "SubagentStop": 10
  },
  "tools_used": {
    "Bash": 30,
    "Write": 15,
    "Read": 25,
    "Edit": 10
  },
  "files_accessed": [
    "/path/to/file1.py",
    "/path/to/file2.js"
  ],
  "commands_executed": [
    {
      "timestamp": "2025-08-31T15:53:50",
      "command": "ls -la"
    }
  ],
  "errors": [],
  "sessions": ["session-123", "session-456"],
  "first_event": "2025-08-31T10:00:00",
  "last_event": "2025-08-31T16:00:00"
}
```

## Privacy & Security

### ⚠️ Important Considerations

1. **Sensitive Information**: Logs may contain:
   - File contents
   - Command outputs
   - User prompts
   - File paths
   - Error messages

2. **Storage Location**: Logs are stored in project root
   - Add `.claude_logs/` to `.gitignore`
   - Don't commit logs to version control

3. **Log Rotation**: Logs are created daily
   - Implement cleanup for old logs
   - Monitor disk space usage

### Add to .gitignore
```bash
echo ".claude_logs/" >> .gitignore
```

## Troubleshooting

### Logs not appearing
1. Check hook configuration in settings.json
2. Verify script permissions: `ls -la .claude/hooks/`
3. Test hooks manually: `.claude/hooks/test_hook.sh`

### Permission errors
```bash
# Fix permissions
chmod +x .claude/hooks/*.sh .claude/hooks/*.py
```

### Python not found
```bash
# Update shebang in scripts if needed
# Change #!/usr/bin/env python3 to specific path
which python3  # Find your Python path
```

### Disk space issues
```bash
# Check log size
du -sh .claude_logs/

# Clean old logs (older than 7 days)
find .claude_logs -name "*.log" -mtime +7 -delete
find .claude_logs -name "*.json" -mtime +7 -delete
```

## Advanced Usage

### Custom Analysis
```python
import json
from pathlib import Path

# Load logs
log_file = Path('.claude_logs') / f'claude_events_{datetime.now().strftime("%Y%m%d")}.json'
with open(log_file) as f:
    logs = json.load(f)

# Analyze specific patterns
bash_commands = [
    log for log in logs 
    if log.get('tool') == 'Bash'
]

# Count errors
errors = [
    log for log in logs 
    if not log.get('success', True)
]
```

### Integration with Monitoring
```bash
# Send logs to external service
python3 -c "
import json
import requests
from pathlib import Path

log_file = Path('.claude_logs/activity_summary.json')
with open(log_file) as f:
    summary = json.load(f)

# Send to monitoring service
requests.post('https://your-monitoring.com/api', json=summary)
"
```

## Benefits

1. **Complete Audit Trail**: Every action is logged
2. **Performance Analysis**: Identify bottlenecks
3. **Error Tracking**: Catch and analyze failures
4. **Usage Patterns**: Understand Claude's behavior
5. **Security Monitoring**: Track file access and commands
6. **Session Replay**: Reconstruct entire sessions
7. **Debugging**: Detailed context for issues

## Notes

- Logs don't block Claude's operations
- Failed logging doesn't interrupt workflow
- Logs are human-readable and machine-parseable
- Daily rotation prevents excessive file sizes
- Summary provides quick insights without parsing all logs