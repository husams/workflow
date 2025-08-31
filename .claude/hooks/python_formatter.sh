#!/bin/bash
# Python Auto-Formatter Hook - Automatically formats Python files after editing

# Read input from stdin
INPUT=$(cat)

# Check if this is a file editing tool
TOOL=$(echo "$INPUT" | jq -r '.tool // ""')
EVENT=$(echo "$INPUT" | jq -r '.event // ""')

# Only run on PostToolUse events for file editing tools
if [ "$EVENT" = "PostToolUse" ] && [[ "$TOOL" =~ ^(Write|Edit|MultiEdit)$ ]]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // ""')
    
    # Check if it's a Python file
    if [[ "$FILE_PATH" == *.py ]]; then
        # Check if black is installed
        if command -v black &> /dev/null; then
            # Format the file
            black "$FILE_PATH" --quiet 2>/dev/null
            
            if [ $? -eq 0 ]; then
                cat <<EOF
{
    "action": "continue",
    "message": "✨ Python file auto-formatted with Black: $(basename "$FILE_PATH")"
}
EOF
            else
                cat <<EOF
{
    "action": "continue",
    "message": "⚠️  Black formatting failed for: $(basename "$FILE_PATH")"
}
EOF
            fi
        else
            # Black not installed, just continue
            cat <<EOF
{
    "action": "continue",
    "message": "ℹ️  Black formatter not installed. Install with: pip install black"
}
EOF
        fi
        exit 0
    fi
fi

# For non-Python files or other tools, just continue
exit 0