#!/usr/bin/env python3
"""
Test script for Python-based Claude Code hooks
"""

import json
import subprocess
import sys
from pathlib import Path

def test_hook(hook_script, test_data):
    """Test a hook with given data"""
    print(f"\n{'='*60}")
    print(f"Testing: {hook_script}")
    print(f"Event: {test_data.get('event', 'Unknown')}")
    print(f"{'='*60}")
    
    # Run the hook
    process = subprocess.Popen(
        ['python3', hook_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=json.dumps(test_data))
    
    print(f"Exit Code: {process.returncode}")
    
    if stdout:
        print(f"Output: {stdout}")
        try:
            result = json.loads(stdout)
            print(f"Parsed: {json.dumps(result, indent=2)}")
        except json.JSONDecodeError:
            print("(Output is not valid JSON)")
    
    if stderr:
        print(f"Errors: {stderr}")
    
    return process.returncode == 0

def main():
    # Test data for different events
    test_cases = [
        {
            "script": ".claude/hooks/log_pretooluse.py",
            "data": {
                "sessionId": "test-session-001",
                "timestamp": 1234567890,
                "event": "PreToolUse",
                "tool": "Bash",
                "parameters": {
                    "command": "ls -la /tmp",
                    "timeout": 30000
                }
            }
        },
        {
            "script": ".claude/hooks/log_posttooluse.py",
            "data": {
                "sessionId": "test-session-002",
                "timestamp": 1234567891,
                "event": "PostToolUse",
                "tool": "Write",
                "parameters": {
                    "file_path": "/tmp/test.py",
                    "content": "print('Hello, World!')"
                },
                "result": {
                    "success": True
                }
            }
        },
        {
            "script": ".claude/hooks/log_userprompt.py",
            "data": {
                "sessionId": "test-session-003",
                "timestamp": 1234567892,
                "event": "UserPromptSubmit",
                "prompt": "Help me write a Python function to calculate fibonacci numbers"
            }
        },
        {
            "script": ".claude/hooks/log_notification.py",
            "data": {
                "sessionId": "test-session-004",
                "timestamp": 1234567893,
                "event": "Notification",
                "type": "info",
                "message": "Task completed successfully"
            }
        },
        {
            "script": ".claude/hooks/log_sessionstart.py",
            "data": {
                "sessionId": "test-session-005",
                "timestamp": 1234567894,
                "event": "SessionStart"
            }
        },
        {
            "script": ".claude/hooks/log_posttooluse.py",
            "data": {
                "sessionId": "test-session-006",
                "timestamp": 1234567895,
                "event": "PostToolUse",
                "tool": "Read",
                "parameters": {
                    "file_path": "/tmp/test.py",
                    "limit": 100,
                    "offset": 0
                },
                "result": {
                    "success": False,
                    "error": "File not found"
                }
            }
        }
    ]
    
    print("🧪 Testing Python-based Claude Code Hooks")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        if test_hook(test_case["script"], test_case["data"]):
            passed += 1
            print("✅ Test passed")
        else:
            failed += 1
            print("❌ Test failed")
    
    print("\n" + "="*60)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    # Check if logs were created
    log_dir = Path(".claude_logs")
    if log_dir.exists():
        print(f"\n📁 Log directory created: {log_dir}")
        log_files = list(log_dir.glob("*.log")) + list(log_dir.glob("*.jsonl"))
        print(f"📄 Log files created: {len(log_files)}")
        for log_file in log_files[:10]:  # Show first 10
            print(f"  - {log_file.name}")
        
        # Check activity summary
        summary_file = log_dir / "activity_summary.json"
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
            print(f"\n📊 Activity Summary:")
            print(f"  Total Events: {summary.get('total_events', 0)}")
            print(f"  Event Types: {summary.get('events_by_type', {})}")
            print(f"  Tools Used: {summary.get('tools_used', {})}")
    else:
        print("\n⚠️  Log directory not created")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())