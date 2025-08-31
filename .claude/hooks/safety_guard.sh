#!/bin/bash
# Safety Guard Hook - Blocks potentially dangerous commands

# Read input from stdin
INPUT=$(cat)

# Check if this is a Bash tool call
TOOL=$(echo "$INPUT" | jq -r '.tool // ""')
if [ "$TOOL" = "Bash" ]; then
    COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // ""')
    
    # Define dangerous patterns
    DANGEROUS_PATTERNS=(
        "rm -rf /"
        "rm -rf /*"
        "dd if=/dev/zero"
        "mkfs"
        "fdisk"
        "> /dev/sda"
        "chmod -R 777 /"
        "chown -R"
        ":(){:|:&};:"  # Fork bomb
    )
    
    # Check each pattern
    for pattern in "${DANGEROUS_PATTERNS[@]}"; do
        if [[ "$COMMAND" == *"$pattern"* ]]; then
            # Return JSON response blocking the command
            cat <<EOF
{
    "action": "block",
    "message": "🚫 Dangerous command blocked: This command contains the pattern '$pattern' which could be harmful to your system."
}
EOF
            exit 2
        fi
    done
    
    # Warn about sudo commands but don't block
    if [[ "$COMMAND" == sudo* ]]; then
        cat <<EOF
{
    "action": "continue",
    "message": "⚠️  Warning: Running command with sudo privileges. Please ensure this is intentional."
}
EOF
        exit 0
    fi
fi

# Allow all other commands
exit 0