#!/bin/bash
# Test Script for Claude Code Hooks
# Usage: ./test_hook.sh <hook_script> [test_case]

HOOK_SCRIPT="$1"
TEST_CASE="${2:-basic}"

if [ -z "$HOOK_SCRIPT" ]; then
    echo "Usage: $0 <hook_script> [test_case]"
    echo "Available test cases: basic, bash_command, dangerous_command, python_edit"
    exit 1
fi

if [ ! -f "$HOOK_SCRIPT" ]; then
    echo "Error: Hook script not found: $HOOK_SCRIPT"
    exit 1
fi

echo "Testing hook: $HOOK_SCRIPT"
echo "Test case: $TEST_CASE"
echo "---"

case "$TEST_CASE" in
    "basic")
        TEST_INPUT='{
            "sessionId": "test-session-123",
            "timestamp": 1234567890,
            "event": "PreToolUse",
            "tool": "Read",
            "parameters": {
                "file_path": "/tmp/test.txt"
            }
        }'
        ;;
    
    "bash_command")
        TEST_INPUT='{
            "sessionId": "test-session-456",
            "timestamp": 1234567890,
            "event": "PreToolUse",
            "tool": "Bash",
            "parameters": {
                "command": "ls -la /tmp"
            }
        }'
        ;;
    
    "dangerous_command")
        TEST_INPUT='{
            "sessionId": "test-session-789",
            "timestamp": 1234567890,
            "event": "PreToolUse",
            "tool": "Bash",
            "parameters": {
                "command": "rm -rf /"
            }
        }'
        ;;
    
    "python_edit")
        TEST_INPUT='{
            "sessionId": "test-session-abc",
            "timestamp": 1234567890,
            "event": "PostToolUse",
            "tool": "Edit",
            "parameters": {
                "file_path": "/tmp/test.py",
                "old_string": "def foo():",
                "new_string": "def bar():"
            },
            "result": {
                "success": true
            }
        }'
        ;;
    
    "user_prompt")
        TEST_INPUT='{
            "sessionId": "test-session-def",
            "timestamp": 1234567890,
            "event": "UserPromptSubmit",
            "prompt": "Help me write a Python function"
        }'
        ;;
    
    *)
        echo "Unknown test case: $TEST_CASE"
        exit 1
        ;;
esac

echo "Input JSON:"
echo "$TEST_INPUT" | jq .
echo "---"

echo "Hook Output:"
OUTPUT=$(echo "$TEST_INPUT" | "$HOOK_SCRIPT" 2>&1)
EXIT_CODE=$?

echo "$OUTPUT"
echo "---"
echo "Exit Code: $EXIT_CODE"

# Try to parse as JSON if output exists
if [ -n "$OUTPUT" ]; then
    echo "---"
    echo "Parsed Output (if JSON):"
    echo "$OUTPUT" | jq . 2>/dev/null || echo "(Not valid JSON)"
fi

# Interpret exit code
echo "---"
case $EXIT_CODE in
    0)
        echo "✅ Result: Success - Operation will continue"
        ;;
    2)
        echo "🚫 Result: Blocked - Operation will be prevented"
        ;;
    *)
        echo "⚠️  Result: Non-standard exit code ($EXIT_CODE)"
        ;;
esac