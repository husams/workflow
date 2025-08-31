# Claude Code Session Logging - Updated Format

## ✅ Changes Implemented

### 1. Single File Per Session (No Timestamp in Filename)
**Old format**: `claude_session_20250831_161539_615a8a64.log`  
**New format**: `claude_session_615a8a64.log`

- Each session gets ONE log file that persists across all events
- No timestamp in filename to ensure same file is used throughout session
- Session ID (first 8 chars) uniquely identifies the log file

### 2. Event Type First Format
**Old format**: `2025-08-31 16:15:39.808 | INFO | [Claude.Session.id] | Event details`  
**New format**: `EventType | Key: Value | Key: Value`

Examples:
```
SessionStart | ID: test-updated-format | User: husam | Directory: /Users/husam/workspace/workflow
UserPromptSubmit | Length: 46 | Prompt: This is a test prompt to verify the new format
PreToolUse | Tool: Bash | Command: ls -la
PostToolUse | Tool: Write | File: /path/to/file.py
PostToolUse | Output: command output here...
PostToolUse | Error: error message if any
Notification | Type: info | Message: Task completed
SessionEnd | Reason: user_exit
Stop | Main agent stopped
SubagentStop | Agent: code-reviewer
PreCompact | Size: 150000 | Reason: size_limit
```

### 3. Session Persistence
- Logger instances are cached at class level
- Same session ID always appends to same file
- File handles are kept open with append mode ('a')
- Automatic detection of existing session files

### 4. JSON Analytics Format
Each event is also logged to `claude_session_SESSIONID.jsonl` with full structured data:
```json
{
    "timestamp": "2025-08-31T16:45:59.091273",
    "unix_timestamp": 1693584000,
    "event_type": "SessionStart",
    "session_id": "test-updated-format",
    "working_directory": "/Users/husam/workspace/workflow",
    "user": "husam",
    "event_data": {
        "event": "SessionStart",
        "sessionId": "test-updated-format",
        "timestamp": 1693584000
    }
}
```

## 📊 Benefits of New Format

### Cleaner Logs
- Event type immediately visible at start of each line
- No redundant timestamps (they're in JSON if needed)
- Consistent pipe-delimited format for easy parsing
- Less visual clutter

### Better Session Tracking
- All events for a session in ONE file
- No file proliferation with timestamps
- Easy to follow complete session history
- Simpler file management

### Analytics Ready
- JSON lines format for structured analytics
- Complete event data preserved
- Easy to parse and analyze programmatically
- Supports real-time streaming analytics

## 🔍 Usage Examples

### Find Session Log
```bash
# By session ID (first 8 chars)
ls .claude_logs/claude_session_3b63a99c*

# Most recent session
ls -t .claude_logs/claude_session_*.log | head -1
```

### Follow Live Session
```bash
# Follow current session
tail -f .claude_logs/claude_session_SESSIONID.log

# Follow with filtering
tail -f .claude_logs/claude_session_*.log | grep "PreToolUse"
```

### Analyze Events
```bash
# Count event types
grep -o "^[^|]*" .claude_logs/claude_session_*.log | sort | uniq -c

# Find all tool uses
grep "Tool:" .claude_logs/claude_session_*.log

# Extract all prompts
grep "UserPromptSubmit" .claude_logs/claude_session_*.log
```

### Parse JSON for Analytics
```python
import json

# Read all events for a session
with open('.claude_logs/claude_session_SESSIONID.jsonl', 'r') as f:
    events = [json.loads(line) for line in f]

# Analyze tool usage
tools_used = {}
for event in events:
    if event['event_type'] in ['PreToolUse', 'PostToolUse']:
        tool = event.get('tool', 'Unknown')
        tools_used[tool] = tools_used.get(tool, 0) + 1
```

## 📁 File Structure

```
.claude_logs/
├── claude_session_3b63a99c.log      # Human-readable session log
├── claude_session_3b63a99c.jsonl    # Structured JSON analytics
├── claude_session_test-upd.log      # Another session
├── claude_session_test-upd.jsonl    
└── activity_summary.json            # Overall statistics
```

## 🚀 Implementation Details

### Key Changes in universal_logger.py

1. **Session File Detection**:
```python
# Check if a log file already exists for this session
existing_log = None
for log_file in self.log_dir.glob(f'claude_session_{session_id[:8]}*.log'):
    if session_id[:8] in str(log_file):
        existing_log = log_file
        break
```

2. **Simplified Formatter**:
```python
# Event type first, no timestamp in main log
formatter = logging.Formatter(fmt='%(message)s')
```

3. **Append Mode**:
```python
# Always append to existing session files
file_handler = logging.handlers.RotatingFileHandler(
    log_file_path,
    maxBytes=50*1024*1024,
    backupCount=3,
    encoding='utf-8',
    mode='a'  # Append mode
)
```

4. **Event Formatting**:
```python
# Consistent format: EventType | Key: Value | Key: Value
logger.info(f"{event_type} | Tool: {tool} | Command: {command}")
logger.info(f"UserPromptSubmit | Length: {len(prompt)} | Prompt: {prompt[:200]}")
logger.info(f"SessionEnd | Reason: {reason}")
```

## ✅ Requirements Met

| Requirement | Implementation |
|------------|----------------|
| Same session in same file | ✅ Class-level logger caching |
| No timestamp in filename | ✅ Format: `claude_session_SESSIONID.log` |
| Event type first | ✅ Format: `EventType \| Details` |
| Capture for analytics | ✅ JSON lines format (.jsonl files) |
| All events tracked | ✅ All 9 event types implemented |

## 📈 Activity Summary

The `activity_summary.json` continues to track:
- Total events across all sessions
- Event type distribution
- Tool usage statistics
- Session metadata with log file paths
- First and last event timestamps

## 🎉 System Status

The updated logging system is now:
- **Cleaner**: Event-first format without redundant timestamps
- **Simpler**: One file per session without timestamp proliferation
- **Persistent**: Same session always uses same file
- **Analytics-Ready**: Full JSON capture for data analysis
- **Production-Ready**: Tested and verified with multiple event types

---
**Update Date**: August 31, 2025
**Version**: 2.0.0 (Simplified Single-File Format)
**Status**: ✅ FULLY OPERATIONAL