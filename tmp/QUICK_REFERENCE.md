# Claude Code Logging - Quick Reference

## ✅ Setup Complete!

The logging system is now **ACTIVE** in this project. All Claude Code events are being logged automatically.

## 📁 File Locations

| File/Directory | Purpose |
|---------------|---------|
| `.claude/settings.json` | Hook configuration (✅ CREATED) |
| `.claude/hooks/*.py` | Python logging scripts |
| `.claude_logs/` | All log files (auto-created) |

## 🔍 Essential Commands

### View Summary
```bash
python3 .claude/hooks/log_viewer.py summary
```

### View Recent Events
```bash
python3 .claude/hooks/log_viewer.py recent
```

### Search Logs
```bash
python3 .claude/hooks/log_viewer.py search --query "keyword"
```

### Watch Real-time
```bash
tail -f .claude_logs/claude_events_$(date +%Y%m%d).log
```

### Test Setup
```bash
python3 .claude/hooks/test_python_hooks.py
```

## 📊 What's Being Logged

✅ **All 9 Event Types:**
- PreToolUse (before tools run)
- PostToolUse (after tools complete)
- UserPromptSubmit (your inputs)
- Notification (system messages)
- SessionStart/End (session lifecycle)
- Stop/SubagentStop (completion events)
- PreCompact (context compression)

✅ **Captured Information:**
- Every command executed
- All file operations
- User prompts
- Errors and warnings
- Performance metrics
- Session statistics

## 🗂️ Log Files

All in `.claude_logs/`:
- `claude_events_*.log` - Main comprehensive log
- `activity_summary.json` - Real-time statistics
- `commands_*.log` - All executed commands
- `errors_*.log` - Errors only
- `file_operations_*.log` - File access log

## 🔒 Privacy Note

⚠️ **Logs may contain:**
- Your prompts and conversations
- File contents
- Command outputs
- Working directory paths

**Remember to:**
- Add `.claude_logs/` to `.gitignore`
- Clean old logs periodically
- Review before sharing

## 🛠️ Disable/Enable

**To temporarily disable:**
Rename or remove `.claude/settings.json`

**To re-enable:**
Restore `.claude/settings.json`

## 📈 Current Status

```
✅ Hooks configured: 9/9 events
✅ Scripts executable: Yes
✅ Logging active: Yes
✅ Log directory: .claude_logs/
✅ Total events logged: Check with 'python3 .claude/hooks/log_viewer.py summary'
```

---
**The logging system is running automatically. No further action needed!**