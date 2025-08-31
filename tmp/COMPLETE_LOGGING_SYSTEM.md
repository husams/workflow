# Claude Code Session Logging - Complete Implementation

## ✅ Final Format with Full JSON Data

### Log Format
```
[Timestamp] [EventType] - Summary | JSON: {complete_data}
```

### Real Examples

```
[2025-08-31 17:03:13] [SessionStart] - New Session: mcp-test-session | JSON: {"session_id":"mcp-test-session","user":"husam","cwd":"/Users/husam/workspace/workflow","log_file":"/Users/husam/workspace/workflow/.claude_logs/claude_session_mcp-test.log"}

[2025-08-31 17:03:13] [UserPromptSubmit] - Prompt: List all files in the current directory | JSON: {"prompt":"List all files in the current directory","length":39,"session_id":"complete-test"}

[2025-08-31 17:03:13] [PreToolUse] - Tool: Bash | JSON: {"tool":"Bash","input":{"command":"ls -la","description":"List files"}}

[2025-08-31 17:03:13] [PostToolUse] - Tool: Bash | JSON: {"tool":"Bash","input":{"command":"ls -la"},"response":{"stdout":"file1.txt\nfile2.py\nfile3.md","stderr":"","success":true}}

[2025-08-31 17:03:13] [PreToolUse] - Tool: mcp__backlog__get_task_instructions | JSON: {"tool":"mcp__backlog__get_task_instructions","input":{"task_id":123}}

[2025-08-31 17:03:13] [PostToolUse] - Tool: mcp__backlog__get_task_instructions | JSON: {"tool":"mcp__backlog__get_task_instructions","input":{"task_id":123},"response":{"stdout":"Task instructions: Implement user authentication with OAuth2","stderr":"","success":true}}

[2025-08-31 17:03:13] [Stop] - Main agent stopped | JSON: {"agent":"main","session_id":"complete-test"}

[2025-08-31 17:03:13] [SessionEnd] - Reason: user_exit | JSON: {"session_id":"complete-test","reason":"user_exit"}
```

## 📊 Key Features

### 1. Complete Information in Single Line
- Each log entry contains ALL relevant information
- No need to look at multiple lines to understand an event
- JSON data provides complete context

### 2. Clear Event Type Identification
- **PreToolUse** vs **PostToolUse** clearly distinguished
- No more "Unknown" events
- Properly extracts `hook_event_name` from Claude events

### 3. JSON Data Included
Each log line includes compact JSON with:
- Tool name and inputs
- Response data (for PostToolUse)
- Session information
- Success/failure status

### 4. Single File Per Session
- Filename: `claude_session_SESSIONID.log`
- No timestamp in filename
- All events append to same file

## 🔍 Event Types and Formats

| Event Type | Format | JSON Fields |
|------------|--------|-------------|
| **SessionStart** | `[Time] [SessionStart] - Session: ID` | session_id, user, cwd, source |
| **UserPromptSubmit** | `[Time] [UserPromptSubmit] - Prompt: text` | prompt, length, session_id |
| **PreToolUse** | `[Time] [PreToolUse] - Tool: name` | tool, input |
| **PostToolUse** | `[Time] [PostToolUse] - Tool: name` | tool, input, response |
| **Notification** | `[Time] [Notification] - message` | type, message |
| **Stop** | `[Time] [Stop] - Main agent stopped` | agent, session_id |
| **SubagentStop** | `[Time] [SubagentStop] - Agent: name` | agent, session_id |
| **PreCompact** | `[Time] [PreCompact] - Size: N` | size, reason |
| **SessionEnd** | `[Time] [SessionEnd] - Reason: reason` | session_id, reason |

## 📁 File Structure

```
.claude_logs/
├── claude_session_17222ae6.log     # Real Claude session
├── claude_session_17222ae6.jsonl   # JSON analytics
├── claude_session_complete.log     # Test session
├── claude_session_mcp-test.log     # MCP tool test
└── activity_summary.json           # Overall statistics
```

## 📈 Activity Summary

The `activity_summary.json` tracks:
```json
{
  "total_events": 34,
  "events_by_type": {
    "SessionStart": 20,
    "UserPromptSubmit": 2,
    "PreToolUse": 4,    // Clearly counted
    "PostToolUse": 4,   // Separately tracked
    "Stop": 2,
    "SessionEnd": 2
  },
  "tools_used": {
    "mcp__backlog__get_task_instructions": 4,
    "Bash": 2,
    "Read": 2
  },
  "sessions": {
    "session-id": {
      "start_time": "2025-08-31T17:03:13",
      "event_count": 6,
      "log_file": "/path/to/log",
      "last_event": "2025-08-31T17:03:13"
    }
  }
}
```

## 🔧 Usage Examples

### Search for Tool Usage
```bash
# Find all PreToolUse events
grep "\[PreToolUse\]" .claude_logs/claude_session_*.log

# Find all PostToolUse events
grep "\[PostToolUse\]" .claude_logs/claude_session_*.log

# Find specific tool usage
grep "mcp__backlog" .claude_logs/claude_session_*.log
```

### Extract JSON Data
```bash
# Extract just the JSON from a line
grep "\[PreToolUse\]" session.log | sed 's/.*JSON: //'

# Parse with jq
grep "\[PostToolUse\]" session.log | sed 's/.*JSON: //' | jq '.response'
```

### Analyze with Python
```python
import json
import re

with open('.claude_logs/claude_session_xxx.log', 'r') as f:
    for line in f:
        # Extract JSON from log line
        match = re.search(r'JSON: (.+)$', line)
        if match:
            data = json.loads(match.group(1))
            
            # Analyze based on event type
            if '[PreToolUse]' in line:
                print(f"Tool started: {data['tool']}")
            elif '[PostToolUse]' in line:
                if data['response'].get('success'):
                    print(f"Tool succeeded: {data['tool']}")
                else:
                    print(f"Tool failed: {data['tool']}")
```

## ✅ All Requirements Satisfied

| Requirement | Implementation |
|------------|----------------|
| PreToolUse/PostToolUse distinction | ✅ Clearly shown in event type |
| All info in single line | ✅ Complete data per line |
| JSON data included | ✅ Full JSON in each log entry |
| No "Unknown" events | ✅ Proper event extraction |
| Clean format | ✅ `[Time] [Type] - Summary \| JSON: {...}` |
| Single file per session | ✅ Session-based files |

## 🚀 System Benefits

1. **Complete Visibility**: Every event has full context in one line
2. **Easy Parsing**: Consistent format for automated analysis
3. **Debug Friendly**: JSON data helps troubleshooting
4. **Analytics Ready**: Structured data for metrics
5. **Performance**: Single file per session reduces I/O

## 📝 Configuration

The system is configured via `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_pretooluse.py"}]}],
    "PostToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": "python3 .claude/hooks/log_posttooluse.py"}]}],
    // ... other events
  }
}
```

## 🎉 Status

The Claude Code logging system is now:
- **Fully Operational**: All events captured correctly
- **Information Rich**: Complete data in every log line
- **Tool Aware**: PreToolUse/PostToolUse properly distinguished
- **JSON Enhanced**: Full context available for analysis
- **Production Ready**: Tested with real Claude sessions

---
**Implementation Complete**: August 31, 2025
**Version**: 4.0.0 (Complete with JSON)
**Status**: ✅ FULLY OPERATIONAL