#!/usr/bin/env python3
"""Test hook to capture raw input from Claude"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Read raw input from stdin
raw_input = sys.stdin.read()

# Write raw input to test file
test_file = Path.cwd() / '.claude_logs' / 'raw_hook_input_test.json'
test_file.parent.mkdir(exist_ok=True)

with open(test_file, 'a') as f:
    f.write(f"\n=== {datetime.now().isoformat()} ===\n")
    f.write(raw_input)
    f.write("\n")

# Parse and return continue response
try:
    data = json.loads(raw_input)
    print(json.dumps({"action": "continue"}))
except:
    print(json.dumps({"action": "continue"}))