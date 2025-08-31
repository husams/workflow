#!/bin/bash
# Test Runner Hook - Automatically runs tests after code changes

# Read input from stdin
INPUT=$(cat)

# Only run on PostToolUse events
EVENT=$(echo "$INPUT" | jq -r '.event // ""')
if [ "$EVENT" != "PostToolUse" ]; then
    exit 0
fi

# Check if this is a file editing tool
TOOL=$(echo "$INPUT" | jq -r '.tool // ""')
if [[ ! "$TOOL" =~ ^(Write|Edit|MultiEdit)$ ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // ""')
FILE_NAME=$(basename "$FILE_PATH")
FILE_DIR=$(dirname "$FILE_PATH")

# Function to run Python tests
run_python_tests() {
    local file_path="$1"
    local module_name="${file_path%.py}"
    module_name="${module_name##*/}"
    
    # Look for corresponding test file
    local test_patterns=(
        "tests/test_${module_name}.py"
        "test/test_${module_name}.py"
        "tests/${module_name}_test.py"
        "test_${module_name}.py"
    )
    
    for test_file in "${test_patterns[@]}"; do
        if [ -f "$test_file" ]; then
            echo "Running tests for $module_name..." >&2
            
            # Try pytest first, then unittest
            if command -v pytest &> /dev/null; then
                pytest "$test_file" -q
                local result=$?
            elif command -v python3 &> /dev/null; then
                python3 -m unittest "$test_file" 2>&1
                local result=$?
            else
                return 1
            fi
            
            if [ $result -eq 0 ]; then
                cat <<EOF
{
    "action": "continue",
    "message": "✅ Tests passed for ${module_name}"
}
EOF
            else
                cat <<EOF
{
    "action": "continue",
    "message": "❌ Tests failed for ${module_name}. Please review and fix."
}
EOF
            fi
            return 0
        fi
    done
    
    return 1
}

# Function to run JavaScript/TypeScript tests
run_javascript_tests() {
    local file_path="$1"
    
    # Check if package.json exists and has test script
    if [ -f "package.json" ]; then
        if grep -q '"test"' package.json; then
            # Check for test file
            local test_patterns=(
                "${file_path%.js}.test.js"
                "${file_path%.js}.spec.js"
                "${file_path%.ts}.test.ts"
                "${file_path%.ts}.spec.ts"
            )
            
            for test_file in "${test_patterns[@]}"; do
                if [ -f "$test_file" ]; then
                    echo "Running JavaScript tests..." >&2
                    npm test -- "$test_file" 2>&1
                    local result=$?
                    
                    if [ $result -eq 0 ]; then
                        cat <<EOF
{
    "action": "continue",
    "message": "✅ JavaScript tests passed"
}
EOF
                    else
                        cat <<EOF
{
    "action": "continue",
    "message": "❌ JavaScript tests failed. Please review and fix."
}
EOF
                    fi
                    return 0
                fi
            done
        fi
    fi
    
    return 1
}

# Determine file type and run appropriate tests
case "$FILE_PATH" in
    *.py)
        run_python_tests "$FILE_PATH"
        ;;
    *.js|*.jsx|*.ts|*.tsx)
        run_javascript_tests "$FILE_PATH"
        ;;
    *)
        # No tests to run for this file type
        exit 0
        ;;
esac

exit 0