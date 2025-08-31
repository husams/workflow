#!/bin/bash
# Command Logger Hook - Logs all Bash commands executed by Claude

# Read input from stdin
INPUT=$(cat)

# Extract command if this is a Bash tool call
TOOL=$(echo "$INPUT" | jq -r '.tool // ""')
if [ "$TOOL" = "Bash" ]; then
    COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // ""')
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // "unknown"')
    
    # Create log directory if it doesn't exist
    LOG_DIR="$HOME/.claude/logs"
    mkdir -p "$LOG_DIR"
    
    # Log the command
    echo "[$TIMESTAMP] Session: $SESSION_ID | Command: $COMMAND" >> "$LOG_DIR/commands.log"
fi

# Always exit 0 to allow command to proceed
exit 0