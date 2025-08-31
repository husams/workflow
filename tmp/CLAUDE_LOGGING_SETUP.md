# Claude Code Universal Logging System - Complete Setup Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Verify Files
Ensure you have the following structure in your project:
```
your-project/
├── .claude/
│   ├── settings.json              # ✅ Hook configuration (CREATED)
│   └── hooks/
│       ├── universal_logger.py    # Main logging engine
│       ├── log_pretooluse.py     # Event hooks (9 files)
│       ├── log_posttooluse.py
│       ├── log_userprompt.py
│       ├── log_notification.py
│       ├── log_sessionstart.py
│       ├── log_sessionend.py
│       ├── log_stop.py
│       ├── log_subagentstop.py
│       ├── log_precompact.py
│       ├── log_viewer.py         # Log viewing utility
│       └── test_python_hooks.py  # Testing script
└── .claude_logs/                  # Will be created automatically
```

### Step 2: Make Scripts Executable
```bash
chmod +x .claude/hooks/*.py
```

### Step 3: Test the Setup
```bash
python3 .claude/hooks/test_python_hooks.py
```

✅ **That's it! Logging is now active for all Claude Code events in this project.**

## 📋 What Gets Logged

### Every Event Captures:
- **Timestamp**: ISO format with milliseconds
- **Session ID**: Unique identifier for each Claude session
- **Event Type**: PreToolUse, PostToolUse, UserPromptSubmit, etc.
- **Working Directory**: Current directory when event occurred
- **User**: System username
- **Full Event Data**: Complete JSON payload

### Tool-Specific Information:
- **Bash Commands**: Full command, timeout settings
- **File Operations**: File paths, existence checks, content previews
- **Read Operations**: Offset, limit parameters
- **Errors**: Complete error messages and stack traces

## 📁 Log Files Location

All logs are stored in `.claude_logs/` in your project root:

```
.claude_logs/
├── claude_events_20250831.log       # Main comprehensive log
├── claude_events_20250831.jsonl     # Structured JSON logs
├── activity_summary.json            # Real-time statistics
├── commands_20250831.log           # All executed commands
├── file_operations_20250831.log    # File read/write operations
├── errors_20250831.log             # Errors only
├── performance_20250831.log        # Performance metrics
└── [event_type]_20250831.log      # Event-specific logs
```

## 🔍 Viewing Your Logs

### Quick Summary
```bash
python3 .claude/hooks/log_viewer.py summary
```

Shows:
- Total events count
- Event distribution
- Most used tools
- Files accessed
- Recent commands
- Error summary

### Recent Activity
```bash
# Last 20 events (default)
python3 .claude/hooks/log_viewer.py recent

# Last 100 events
python3 .claude/hooks/log_viewer.py recent --count 100
```

### Search Logs
```bash
# Search for errors
python3 .claude/hooks/log_viewer.py search --query "error"

# Search for specific file
python3 .claude/hooks/log_viewer.py search --query "main.py"

# Search for git commands
python3 .claude/hooks/log_viewer.py search --query "git"
```

### Real-time Monitoring
```bash
# Watch logs in real-time
tail -f .claude_logs/claude_events_$(date +%Y%m%d).log

# Watch commands only
tail -f .claude_logs/commands_$(date +%Y%m%d).log

# Watch errors only
tail -f .claude_logs/errors_$(date +%Y%m%d).log
```

### Export Logs
```bash
# Export to JSON
python3 .claude/hooks/log_viewer.py export --output my_session.json

# Export to CSV
python3 .claude/hooks/log_viewer.py export --output my_session.csv --format csv
```

## 📊 Understanding the Logs

### Main Log Format
```
2025-08-31 16:02:07.569 | Claude.PreToolUse    | INFO     | PreToolUse | Tool: Bash | Command: ls -la
```

Components:
- **Timestamp**: Date and time with milliseconds
- **Logger Name**: Hierarchical logger (Claude.EventType)
- **Level**: DEBUG, INFO, WARNING, ERROR
- **Message**: Human-readable event description

### JSON Log Format
```json
{
  "timestamp": "2025-08-31T16:02:07.569561",
  "event_type": "PreToolUse",
  "session_id": "abc-123",
  "tool": "Bash",
  "parameters": {
    "command": "ls -la"
  }
}
```

### Activity Summary
```json
{
  "total_events": 150,
  "events_by_type": {
    "PreToolUse": 50,
    "PostToolUse": 50,
    "UserPromptSubmit": 20
  },
  "tools_used": {
    "Bash": 30,
    "Write": 15,
    "Read": 25
  },
  "files_accessed": ["file1.py", "file2.js"],
  "commands_executed": [...]
}
```

## ⚙️ Configuration Details

### The `.claude/settings.json` File

This file configures which hooks run for which events:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",           // Matches all tools
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/log_pretooluse.py"
          }
        ]
      }
    ],
    // ... similar for other events
  }
}
```

### Matcher Patterns
- `"*"` - Matches all tools (current configuration)
- `"Bash"` - Matches only Bash tool
- `"^(Read|Write)$"` - Regex for Read or Write
- `"mcp__*"` - Glob pattern for MCP tools

### Disabling Specific Events
To disable logging for an event, remove its section from settings.json:
```json
{
  "hooks": {
    // Remove or comment out events you don't want to log
    // "UserPromptSubmit": [ ... ]
  }
}
```

## 🛠️ Advanced Configuration

### Adjust Log Rotation
Edit `.claude/hooks/universal_logger.py`:
```python
# Main log (line ~62)
main_handler = logging.handlers.RotatingFileHandler(
    main_log_file,
    maxBytes=10*1024*1024,  # Change to 50MB: 50*1024*1024
    backupCount=5,          # Change to keep 10 backups: 10
    encoding='utf-8'
)

# Event logs (line ~94)
event_handler = logging.handlers.RotatingFileHandler(
    event_log,
    maxBytes=5*1024*1024,   # Change to 20MB: 20*1024*1024
    backupCount=3,          # Change to keep 5 backups: 5
    encoding='utf-8'
)
```

### Change Log Levels
To reduce verbosity, edit `.claude/hooks/universal_logger.py`:
```python
# Change from DEBUG to INFO to reduce log volume
root_logger.setLevel(logging.INFO)  # Line ~58
```

### Custom Log Directory
To change log location, edit `.claude/hooks/universal_logger.py`:
```python
# Line ~22-23
self.log_dir = self.project_root / 'my_custom_logs'  # Change directory name
```

## 🔒 Security & Privacy

### Important Considerations
⚠️ **Logs may contain sensitive information:**
- User prompts and conversations
- File contents and paths
- Command outputs
- API keys or credentials in commands

### Best Practices

1. **Add to .gitignore**
```bash
echo ".claude_logs/" >> .gitignore
```

2. **Set Permissions**
```bash
chmod 700 .claude_logs/
```

3. **Regular Cleanup**
```bash
# Delete logs older than 7 days
find .claude_logs -name "*.log" -mtime +7 -delete
find .claude_logs -name "*.jsonl" -mtime +7 -delete
```

4. **Sensitive Projects**
For sensitive projects, consider:
- Encrypting log files
- Disabling UserPromptSubmit logging
- Filtering sensitive commands

## 🧹 Maintenance

### Check Log Size
```bash
du -sh .claude_logs/
```

### Clean Old Logs
```bash
# Remove all logs
rm -rf .claude_logs/

# Remove logs older than N days
find .claude_logs -type f -mtime +30 -delete
```

### Backup Logs
```bash
# Create backup archive
tar -czf claude_logs_backup_$(date +%Y%m%d).tar.gz .claude_logs/

# Move to backup location
mv claude_logs_backup_*.tar.gz ~/backups/
```

## 🐛 Troubleshooting

### Logs Not Appearing

1. **Check settings.json exists and is valid JSON:**
```bash
cat .claude/settings.json | python3 -m json.tool
```

2. **Verify Python is available:**
```bash
which python3
python3 --version
```

3. **Check script permissions:**
```bash
ls -la .claude/hooks/*.py
# All should be executable (-rwxr-xr-x)
```

4. **Test a hook manually:**
```bash
echo '{"event": "PreToolUse", "tool": "Bash", "parameters": {"command": "ls"}}' | python3 .claude/hooks/log_pretooluse.py
```

### Permission Errors
```bash
# Fix permissions
chmod +x .claude/hooks/*.py
chmod 755 .claude/hooks/
```

### Python Module Errors
```bash
# Ensure Python 3.6+ is installed
python3 --version

# If using virtual environment, activate it first
source venv/bin/activate
```

### Disk Space Issues
```bash
# Check available space
df -h .

# Clean up logs
rm -rf .claude_logs/*.log.*  # Remove rotated backups
```

## 📈 Performance Impact

The logging system is designed to be lightweight:
- **Asynchronous writing**: Doesn't block Claude's operations
- **Rotation prevents growth**: Automatic file rotation
- **Efficient formatting**: Lazy string evaluation
- **Buffered I/O**: Reduces disk operations

Typical overhead: < 5ms per event

## 🎯 Use Cases

### 1. Debugging Sessions
- Track exact sequence of operations
- Identify where errors occurred
- Reproduce issues

### 2. Audit Trail
- Complete record of all actions
- Compliance and security auditing
- Change tracking

### 3. Performance Analysis
- Identify slow operations
- Track resource usage
- Optimize workflows

### 4. Learning & Improvement
- Understand Claude's behavior
- Identify patterns
- Improve prompts based on logs

### 5. Team Collaboration
- Share session logs
- Review code changes
- Track progress

## 📝 Example Workflows

### Investigating an Error
```bash
# 1. Search for errors
python3 .claude/hooks/log_viewer.py search --query "error"

# 2. View error log
cat .claude_logs/errors_$(date +%Y%m%d).log

# 3. Get context around error
grep -B5 -A5 "error" .claude_logs/claude_events_$(date +%Y%m%d).log
```

### Reviewing a Session
```bash
# 1. Get session summary
python3 .claude/hooks/log_viewer.py summary

# 2. View recent activity
python3 .claude/hooks/log_viewer.py recent --count 50

# 3. Export for analysis
python3 .claude/hooks/log_viewer.py export --output session.json
```

### Monitoring Real-time
```bash
# Terminal 1: Watch all events
tail -f .claude_logs/claude_events_$(date +%Y%m%d).log

# Terminal 2: Watch commands only
tail -f .claude_logs/commands_$(date +%Y%m%d).log | grep -v "^$"

# Terminal 3: Watch for errors
tail -f .claude_logs/errors_$(date +%Y%m%d).log
```

## ✅ Verification Checklist

After setup, verify everything is working:

- [ ] `.claude/settings.json` exists
- [ ] All `.py` files in `.claude/hooks/` are executable
- [ ] Test script runs successfully: `python3 .claude/hooks/test_python_hooks.py`
- [ ] `.claude_logs/` directory is created after testing
- [ ] Log files are being written
- [ ] `activity_summary.json` is being updated
- [ ] Log viewer works: `python3 .claude/hooks/log_viewer.py summary`

## 🆘 Getting Help

If you encounter issues:

1. **Check this documentation first**
2. **Run the test script** to identify specific problems
3. **Review the error logs** in `.claude_logs/errors_*.log`
4. **Verify Python version** (requires 3.6+)
5. **Check file permissions** on hooks and log directory

## 📄 License & Credits

This logging system was created for comprehensive Claude Code activity tracking.
Feel free to modify and extend based on your needs.

---

**Remember**: The logging system runs automatically once configured. You don't need to manually invoke anything - just use Claude Code normally and all events will be logged!