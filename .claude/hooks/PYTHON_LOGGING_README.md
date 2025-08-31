# Claude Code Python Logging System

## Overview
A comprehensive Python-based logging system using the Python `logging` module to track ALL Claude Code events. Features rotating log files, multiple log levels, specialized loggers for different aspects, and structured logging formats.

## Features

### 🐍 Pure Python Implementation
- All hooks written in Python 3
- Uses standard Python `logging` module
- No shell script dependencies
- Cross-platform compatible

### 📊 Comprehensive Logging with Python logging module
- **RotatingFileHandler**: Automatic log rotation when files exceed size limits
- **Multiple Formatters**: Detailed and JSON formatters
- **Log Levels**: DEBUG, INFO, WARNING, ERROR with appropriate filtering
- **Hierarchical Loggers**: Parent-child logger relationships for organized logging

### 📁 Specialized Loggers
```
Claude (root logger)
├── Claude.PreToolUse       # Before tool execution
├── Claude.PostToolUse      # After tool completion
├── Claude.UserPromptSubmit # User inputs
├── Claude.Notification     # System notifications
├── Claude.SessionStart     # Session beginning
├── Claude.SessionEnd       # Session completion
├── Claude.Stop            # Main agent completion
├── Claude.SubagentStop    # Subagent completion
├── Claude.PreCompact      # Context compression
├── Claude.Commands        # All executed commands
├── Claude.Files          # File operations
├── Claude.Errors         # Error tracking
├── Claude.Performance    # Performance metrics
└── Claude.Main          # General logging
```

### 📄 Log Files Generated
```
.claude_logs/
├── claude_events_YYYYMMDD.log       # Main log with rotation (10MB max, 5 backups)
├── claude_events_YYYYMMDD.jsonl     # Structured JSON logs
├── pretooluse_YYYYMMDD.log         # Event-specific logs (5MB max, 3 backups)
├── posttooluse_YYYYMMDD.log
├── userpromptsubmit_YYYYMMDD.log
├── notification_YYYYMMDD.log
├── sessionstart_YYYYMMDD.log
├── sessionend_YYYYMMDD.log
├── stop_YYYYMMDD.log
├── subagentstop_YYYYMMDD.log
├── precompact_YYYYMMDD.log
├── commands_YYYYMMDD.log           # All commands executed
├── file_operations_YYYYMMDD.log    # File read/write operations
├── errors_YYYYMMDD.log             # Error-only log
├── performance_YYYYMMDD.log        # Performance metrics
└── activity_summary.json           # Aggregated statistics
```

## Installation

### 1. Copy the hooks to your project
```bash
cp -r .claude/hooks /path/to/your/project/.claude/
```

### 2. Make Python scripts executable
```bash
cd /path/to/your/project
chmod +x .claude/hooks/*.py
```

### 3. Configure Claude Code settings

Add to `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_pretooluse.py"}]}
    ],
    "PostToolUse": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_posttooluse.py"}]}
    ],
    "UserPromptSubmit": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_userprompt.py"}]}
    ],
    "Notification": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_notification.py"}]}
    ],
    "SessionStart": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_sessionstart.py"}]}
    ],
    "SessionEnd": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_sessionend.py"}]}
    ],
    "Stop": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_stop.py"}]}
    ],
    "SubagentStop": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_subagentstop.py"}]}
    ],
    "PreCompact": [
      {"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_precompact.py"}]}
    ]
  }
}
```

Or use the provided configuration:
```bash
cp .claude/hooks/python_logging_settings.json .claude/settings.json
```

## Python Logging Module Features Used

### 1. Rotating File Handlers
```python
main_handler = logging.handlers.RotatingFileHandler(
    filename,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,          # Keep 5 backups
    encoding='utf-8'
)
```
- Automatically rotates logs when they exceed size limits
- Keeps specified number of backup files
- Prevents disk space issues

### 2. Custom Formatters
```python
detailed_formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d | %(name)-20s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```
- Consistent timestamp format with milliseconds
- Logger name for easy filtering
- Log level for severity identification

### 3. Hierarchical Logger Structure
```python
root_logger = logging.getLogger('Claude')
event_logger = logging.getLogger('Claude.PreToolUse')
```
- Parent loggers propagate to children
- Allows selective filtering by logger name
- Organized log output

### 4. Multiple Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages with stack traces

### 5. Specialized Handlers
- Different log files for different purposes
- Separate error log for quick issue identification
- Performance log for metrics tracking

## Log Format Examples

### Main Log Format
```
2025-08-31 16:02:07.569 | Claude.PreToolUse    | INFO     | PreToolUse | Tool: Bash | Command: ls -la /tmp
2025-08-31 16:02:07.600 | Claude.PostToolUse   | INFO     | PostToolUse | Tool: Write | File: /tmp/test.py
2025-08-31 16:02:07.630 | Claude.UserPromptSubmit | INFO     | UserPromptSubmit | Length: 62 chars
```

### Command Log Format
```
2025-08-31 16:02:07 | [PreToolUse] git status
2025-08-31 16:02:08 | [PostToolUse] git commit -m "Update"
```

### Error Log Format
```
2025-08-31 16:02:07.716 | Claude.Errors        | ERROR    | Tool failure - Read: File not found
```

### JSON Log Format (structured data)
```json
{
  "timestamp": "2025-08-31T16:02:07.569561",
  "unix_timestamp": 1234567890,
  "event_type": "PreToolUse",
  "session_id": "test-session-001",
  "working_directory": "/Users/user/project",
  "user": "username",
  "tool": "Bash",
  "parameters": {
    "command": "ls -la /tmp",
    "timeout": 30000
  },
  "command": "ls -la /tmp"
}
```

## Testing

### Run the test suite
```bash
python3 .claude/hooks/test_python_hooks.py
```

### Test individual hooks
```bash
echo '{"event": "PreToolUse", "tool": "Bash", "parameters": {"command": "ls"}}' | python3 .claude/hooks/log_pretooluse.py
```

## Viewing Logs

### Using the log viewer utility
```bash
# View summary
python3 .claude/hooks/log_viewer.py summary

# View recent events
python3 .claude/hooks/log_viewer.py recent --count 50

# Search logs
python3 .claude/hooks/log_viewer.py search --query "error"

# Analyze performance
python3 .claude/hooks/log_viewer.py analyze

# Export logs
python3 .claude/hooks/log_viewer.py export --output logs.json
```

### Direct file access
```bash
# Tail main log
tail -f .claude_logs/claude_events_$(date +%Y%m%d).log

# View errors only
cat .claude_logs/errors_$(date +%Y%m%d).log

# View commands
cat .claude_logs/commands_$(date +%Y%m%d).log

# Parse JSON logs
cat .claude_logs/claude_events_$(date +%Y%m%d).jsonl | jq .
```

## Configuration Options

### Adjust log rotation settings
In `universal_logger.py`, modify:
```python
# Main log rotation
maxBytes=10*1024*1024,  # Change max file size
backupCount=5,          # Change number of backups

# Event log rotation
maxBytes=5*1024*1024,   # Per-event file size
backupCount=3,          # Per-event backups
```

### Change log levels
```python
logger.setLevel(logging.DEBUG)  # Set to INFO, WARNING, ERROR as needed
```

### Modify formatters
```python
detailed_formatter = logging.Formatter(
    fmt='your_custom_format',
    datefmt='your_date_format'
)
```

## Benefits of Python Implementation

1. **Native logging module**: Leverages Python's robust logging framework
2. **Automatic rotation**: Prevents disk space issues with RotatingFileHandler
3. **Performance**: Efficient buffered writing and lazy evaluation
4. **Flexibility**: Easy to extend with custom handlers and formatters
5. **Error handling**: Proper exception handling with stack traces
6. **Thread-safe**: Python logging module is thread-safe by design
7. **Filtering**: Built-in filtering by logger name and level
8. **Propagation**: Hierarchical logger structure with propagation control

## Troubleshooting

### Python not found
```bash
# Check Python installation
which python3

# Update shebang if needed
#!/usr/bin/env python3  # or specific path like #!/usr/bin/python3
```

### Permission denied
```bash
chmod +x .claude/hooks/*.py
```

### Logs not appearing
- Check settings.json configuration
- Verify Python scripts are executable
- Test hooks individually
- Check .claude_logs/ directory permissions

### Disk space issues
- Adjust maxBytes and backupCount in universal_logger.py
- Implement log cleanup cron job
- Monitor .claude_logs/ directory size

## Security Notes

- Logs may contain sensitive information
- Add `.claude_logs/` to `.gitignore`
- Set appropriate file permissions
- Consider encryption for sensitive environments
- Implement log retention policies

## Performance Considerations

- Rotating handlers prevent unlimited growth
- JSON logs use line-delimited format for efficient parsing
- Separate loggers reduce I/O contention
- Buffered writing improves performance
- Lazy formatting with % style reduces overhead

## Extending the System

### Add custom loggers
```python
custom_logger = logging.getLogger('Claude.Custom')
custom_logger.setLevel(logging.INFO)
# Add handlers as needed
```

### Add custom handlers
```python
# Email handler for critical errors
email_handler = logging.handlers.SMTPHandler(...)
error_logger.addHandler(email_handler)
```

### Add filters
```python
class CustomFilter(logging.Filter):
    def filter(self, record):
        # Custom filtering logic
        return True

logger.addFilter(CustomFilter())
```

This Python-based logging system provides enterprise-grade logging capabilities with the reliability and features of Python's built-in logging module.