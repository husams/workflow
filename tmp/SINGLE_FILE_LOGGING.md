# Claude Code Single-File Session Logging

## ✅ System Updated: Single File Per Session

The logging system has been updated to write **all events to a single file per session** with the session ID included in the filename.

## 📁 New Log File Structure

### File Naming Convention
```
claude_session_YYYYMMDD_HHMMSS_SESSIONID.log
claude_session_YYYYMMDD_HHMMSS_SESSIONID.jsonl
```

Example:
```
claude_session_20250831_161539_615a8a64.log   # Human-readable log
claude_session_20250831_161539_615a8a64.jsonl # Structured JSON data
```

### Directory Structure
```
.claude_logs/
├── claude_session_20250831_161539_615a8a64.log    # Session 1
├── claude_session_20250831_161539_615a8a64.jsonl
├── claude_session_20250831_162245_7b2c9d8e.log    # Session 2
├── claude_session_20250831_162245_7b2c9d8e.jsonl
├── claude_session_20250831_163012_9f3e4a5b.log    # Session 3
├── claude_session_20250831_163012_9f3e4a5b.jsonl
└── activity_summary.json                          # Overall statistics
```

## 🎯 Key Features

### 1. Single File Per Session
- **All events** for a session go to one file
- No more scattered logs across multiple files
- Easy to follow a complete session from start to finish

### 2. Session ID in Filename
- Quickly identify which log belongs to which session
- First 8 characters of session ID used for brevity
- Timestamp shows when session started

### 3. Automatic Session Detection
- Logger automatically detects session ID from events
- Creates new log file for each unique session
- Reuses existing logger for same session

### 4. Rotating File Handler
- Each session log can grow up to 50MB
- Automatically rotates with .1, .2, .3 backups
- Prevents disk space issues

## 📊 Log Format Example

```
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | ================================================================================
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | SESSION STARTED - ID: 615a8a64-90f6-477f-a1c8-6c4c32b670e4
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | Log File: /Users/user/project/.claude_logs/claude_session_20250831_161539_615a8a64.log
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | Project Root: /Users/user/project
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | Working Directory: /Users/user/project
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | User: username
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | Timestamp: 2025-08-31T16:15:39.808241
2025-08-31 16:15:39.808 | INFO     | [Claude.Session.615a8a64] | ================================================================================
2025-08-31 16:15:39.866 | INFO     | [Claude.Session.615a8a64] | ============================================================
2025-08-31 16:15:39.866 | INFO     | [Claude.Session.615a8a64] | 📝 USER PROMPT
2025-08-31 16:15:39.866 | INFO     | [Claude.Session.615a8a64] | Length: 25 characters
2025-08-31 16:15:39.866 | INFO     | [Claude.Session.615a8a64] | Prompt: Help me write a function
2025-08-31 16:15:39.866 | INFO     | [Claude.Session.615a8a64] | ============================================================
2025-08-31 16:15:40.123 | INFO     | [Claude.Session.615a8a64] | ▶ PreToolUse | Tool: Bash
2025-08-31 16:15:40.123 | INFO     | [Claude.Session.615a8a64] |   Command: ls -la
2025-08-31 16:15:40.234 | INFO     | [Claude.Session.615a8a64] | ✓ PostToolUse | Tool: Bash
2025-08-31 16:15:40.234 | DEBUG    | [Claude.Session.615a8a64] |   Output: total 88...
2025-08-31 16:15:45.567 | INFO     | [Claude.Session.615a8a64] | ⏹️  MAIN AGENT STOPPED
2025-08-31 16:15:45.678 | INFO     | [Claude.Session.615a8a64] | 🏁 SESSION ENDED
2025-08-31 16:15:45.678 | INFO     | [Claude.Session.615a8a64] |   Reason: user_exit
2025-08-31 16:15:45.678 | INFO     | [Claude.Session.615a8a64] | ================================================================================
```

## 🔍 Finding Your Session Log

### Method 1: Check Activity Summary
```bash
cat .claude_logs/activity_summary.json | python3 -m json.tool
```

Look for your session ID and its log file:
```json
"sessions": {
    "615a8a64-90f6-477f-a1c8-6c4c32b670e4": {
        "start_time": "2025-08-31T16:15:39.808271",
        "event_count": 42,
        "log_file": "/path/to/.claude_logs/claude_session_20250831_161539_615a8a64.log",
        "last_event": "2025-08-31T16:15:45.678"
    }
}
```

### Method 2: List Recent Session Logs
```bash
# List all session logs sorted by time (newest first)
ls -lt .claude_logs/claude_session_*.log | head -10

# Show the most recent session log
ls -t .claude_logs/claude_session_*.log | head -1
```

### Method 3: Follow Current Session
```bash
# Follow the most recent log file
tail -f $(ls -t .claude_logs/claude_session_*.log | head -1)
```

## 📈 Benefits

### 1. Easier Session Analysis
- Complete session history in one file
- No need to correlate multiple log files
- Clear session boundaries

### 2. Better Debugging
- Follow exact sequence of events
- See full context in one place
- Easy to share specific session logs

### 3. Cleaner Log Directory
- Fewer files (one per session instead of 10+)
- Clear file naming with session ID
- Easy to identify and manage sessions

### 4. Improved Performance
- Single logger instance per session
- Reduced file handle overhead
- More efficient disk I/O

## 🛠️ Configuration

### Log Rotation Settings
In `universal_logger.py`:
```python
file_handler = logging.handlers.RotatingFileHandler(
    log_file_path,
    maxBytes=50*1024*1024,  # 50MB max per file
    backupCount=3,          # Keep 3 backups
    encoding='utf-8'
)
```

### Session ID Extraction
The logger automatically extracts session ID from:
1. `event_data.sessionId`
2. `event_data.session_id`
3. Nested `event_data.event_data.session_id`
4. Falls back to 'unknown' if not found

## 📝 Usage Examples

### View Specific Session
```bash
# If you know the session ID
SESSION_ID="615a8a64"
cat .claude_logs/claude_session_*_${SESSION_ID}*.log
```

### Search Across All Sessions
```bash
# Search for errors across all sessions
grep -h "ERROR" .claude_logs/claude_session_*.log

# Find all commands executed
grep -h "Command:" .claude_logs/claude_session_*.log

# Find specific file access
grep -h "File: /path/to/file.py" .claude_logs/claude_session_*.log
```

### Export Session
```bash
# Copy a specific session log
cp .claude_logs/claude_session_20250831_161539_615a8a64.log ~/Desktop/session_export.log

# Create archive of a session
tar -czf session_615a8a64.tar.gz .claude_logs/claude_session_*_615a8a64.*
```

### Clean Old Sessions
```bash
# Remove session logs older than 7 days
find .claude_logs -name "claude_session_*.log" -mtime +7 -delete
find .claude_logs -name "claude_session_*.jsonl" -mtime +7 -delete

# Keep only last 10 sessions
ls -t .claude_logs/claude_session_*.log | tail -n +11 | xargs rm -f
```

## 🔄 Migration from Old System

If you had logs from the previous multi-file system:
1. Old logs remain in `.claude_logs/` with their original names
2. New sessions will use the single-file format
3. Activity summary tracks both old and new sessions
4. You can safely delete old log files if not needed

## 📊 Session Metrics

The activity summary now tracks:
- Session ID
- Start time
- Event count per session
- Log file path
- Last event time

This makes it easy to:
- Identify long-running sessions
- Find high-activity sessions
- Track session patterns
- Analyze usage over time

## ✅ Summary

The logging system now provides:
- **One log file per session** with session ID in filename
- **Complete session history** in a single, easy-to-read file
- **Automatic session detection** and logger reuse
- **50MB rotating logs** with automatic backups
- **Clean, organized log directory** with clear file naming

All events for a Claude Code session are now captured in a single file, making it much easier to follow, analyze, and share session logs!