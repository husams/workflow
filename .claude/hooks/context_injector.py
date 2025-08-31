#!/usr/bin/env python3
"""
Context Injector Hook - Adds project-specific context to user prompts
"""

import json
import sys
import os
from datetime import datetime

def get_project_context():
    """Get project-specific context based on current directory"""
    cwd = os.getcwd()
    project_name = os.path.basename(cwd)
    
    # Default context
    context_lines = [
        f"Project: {project_name}",
        f"Working Directory: {cwd}",
    ]
    
    # Add git branch if in a git repo
    if os.path.exists('.git'):
        try:
            import subprocess
            branch = subprocess.check_output(['git', 'branch', '--show-current'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
            if branch:
                context_lines.append(f"Git Branch: {branch}")
        except:
            pass
    
    # Check for specific project files and add relevant context
    if os.path.exists('package.json'):
        context_lines.append("Type: Node.js/JavaScript project")
        context_lines.append("Remember: Use npm/yarn commands, follow JavaScript conventions")
    elif os.path.exists('requirements.txt') or os.path.exists('pyproject.toml'):
        context_lines.append("Type: Python project")
        context_lines.append("Remember: Follow PEP 8, use type hints, write docstrings")
    elif os.path.exists('Cargo.toml'):
        context_lines.append("Type: Rust project")
        context_lines.append("Remember: Follow Rust conventions, handle Results properly")
    
    # Add any project-specific instructions from .claude/project.md
    project_instructions_path = '.claude/project.md'
    if os.path.exists(project_instructions_path):
        context_lines.append(f"Project instructions available in {project_instructions_path}")
    
    return "\n".join(context_lines)

def main():
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    
    # Only process UserPromptSubmit events
    if input_data.get('event') != 'UserPromptSubmit':
        sys.exit(0)
    
    user_prompt = input_data.get('prompt', '')
    
    # Don't inject context for very short prompts (likely commands)
    if len(user_prompt) < 10:
        sys.exit(0)
    
    # Get project context
    context = get_project_context()
    
    # Create modified prompt with context
    modified_prompt = f"""[Project Context]
{context}

[User Request]
{user_prompt}"""
    
    # Output JSON response
    output = {
        "action": "modify",
        "modifiedInput": {
            "prompt": modified_prompt
        },
        "message": "📁 Added project context to prompt"
    }
    
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()