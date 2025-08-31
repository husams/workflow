#!/usr/bin/env python3
"""
Optimized Event Logger for Claude Code
Reduces redundancy by storing common session fields once
"""

import json
import sys
import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
import traceback
from typing import Dict, Any, Optional

class OptimizedClaudeLogger:
    """Optimized logger that reduces redundancy in logged JSON"""
    
    # Class variables to store session state
    _session_logger = None
    _session_id = None
    _log_file_path = None
    _session_common_fields = None  # Store common fields per session
    
    def __init__(self):
        self.project_root = self.find_project_root()
        self.log_dir = self.project_root / '.claude_logs'
        self.log_dir.mkdir(exist_ok=True)
        
    def find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        
        markers = ['.git', '.claude', 'package.json', 'requirements.txt', 
                  'pyproject.toml', 'Cargo.toml', 'go.mod']
        
        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    return current
            current = current.parent
        
        return Path.cwd()
    
    def extract_unique_fields(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract only fields that are unique to this event"""
        if not OptimizedClaudeLogger._session_common_fields:
            # First event in session - establish common fields
            OptimizedClaudeLogger._session_common_fields = {
                'session_id': event_data.get('session_id'),
                'transcript_path': event_data.get('transcript_path'),
                'cwd': event_data.get('cwd')
            }
            # Return full data for first event
            return event_data
        
        # Return only fields that differ from common fields
        unique = {}
        for key, value in event_data.items():
            if key not in OptimizedClaudeLogger._session_common_fields or \
               OptimizedClaudeLogger._session_common_fields[key] != value:
                unique[key] = value
        
        return unique
    
    def get_or_create_session_logger(self, session_id: str) -> logging.Logger:
        """Get existing session logger or create new one"""
        
        # If we already have a logger for this session, return it
        if OptimizedClaudeLogger._session_logger and OptimizedClaudeLogger._session_id == session_id:
            return OptimizedClaudeLogger._session_logger
        
        # Reset common fields for new session
        OptimizedClaudeLogger._session_common_fields = None
        
        # Check if a log file already exists for this session
        existing_log = None
        for log_file in self.log_dir.glob(f'claude_session_{session_id[:8]}*.log'):
            if session_id[:8] in str(log_file):
                existing_log = log_file
                break
        
        # Create new session logger
        OptimizedClaudeLogger._session_id = session_id
        
        logger_name = f'Claude.Session.{session_id}'
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        
        if existing_log:
            log_file_path = existing_log
        else:
            log_filename = f'claude_session_{session_id[:8]}.log'
            log_file_path = self.log_dir / log_filename
        OptimizedClaudeLogger._log_file_path = log_file_path
        
        # Create file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=50*1024*1024,  # 50MB max per file
            backupCount=3,
            encoding='utf-8',
            mode='a'
        )
        
        formatter = logging.Formatter(fmt='%(message)s')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        logger.addHandler(file_handler)
        
        # Also create a JSONL handler for full raw data
        json_filename = f'claude_session_{session_id[:8]}_raw.jsonl'
        json_file_path = self.log_dir / json_filename
        json_handler = logging.FileHandler(json_file_path, encoding='utf-8', mode='a')
        json_formatter = logging.Formatter('%(message)s')
        json_handler.setFormatter(json_formatter)
        
        json_logger_name = f'Claude.JSON.{session_id}'
        json_logger = logging.getLogger(json_logger_name)
        json_logger.setLevel(logging.DEBUG)
        json_logger.handlers.clear()
        json_logger.addHandler(json_handler)
        json_logger.propagate = False
        
        OptimizedClaudeLogger._session_logger = logger
        OptimizedClaudeLogger._json_logger = json_logger
        
        return logger
    
    def log_event(self, event_data: Dict[str, Any], raw_json: Optional[str] = None) -> Dict[str, Any]:
        """Log event with redundancy reduction"""
        try:
            # Extract session ID
            session_id = event_data.get('session_id', 'unknown')
            
            # Get or create session logger
            logger = self.get_or_create_session_logger(session_id)
            json_logger = getattr(OptimizedClaudeLogger, '_json_logger', None)
            
            # Log full raw data to JSONL file
            if json_logger and raw_json:
                json_logger.info(raw_json)
            
            # Extract event type
            event_type = event_data.get('hook_event_name', 'Unknown')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get unique fields only
            unique_fields = self.extract_unique_fields(event_data)
            
            # Log session header if this is the first event
            if len(unique_fields) == len(event_data):
                # First event - log session common fields
                logger.info(f"[{timestamp}] === NEW SESSION: {session_id[:8]} ===")
                logger.info(f"[{timestamp}] Session Fields: {{")
                if OptimizedClaudeLogger._session_common_fields:
                    for key, value in OptimizedClaudeLogger._session_common_fields.items():
                        if value:
                            logger.info(f"  {key}: {json.dumps(value)}")
                logger.info("}")
            
            # Create optimized JSON with only unique fields
            optimized_json = json.dumps(unique_fields, ensure_ascii=False, separators=(',', ':'))
            
            # Log based on event type with optimized JSON
            if event_type in ['PreToolUse', 'PostToolUse']:
                self._log_tool_event(logger, event_type, unique_fields, optimized_json, timestamp)
            elif event_type == 'UserPromptSubmit':
                prompt = unique_fields.get('prompt', '')
                logger.info(f"[{timestamp}] [{event_type}] - Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''} | JSON: {optimized_json}")
            elif event_type in ['SessionStart', 'SessionEnd']:
                if event_type == 'SessionEnd':
                    reason = unique_fields.get('reason', 'unknown')
                    logger.info(f"[{timestamp}] [{event_type}] - Reason: {reason} | JSON: {optimized_json}")
                else:
                    logger.info(f"[{timestamp}] [{event_type}] | JSON: {optimized_json}")
            else:
                logger.info(f"[{timestamp}] [{event_type}] | JSON: {optimized_json}")
            
            return {
                "action": "continue",
                "message": f"✓ Logged {event_type} (optimized)"
            }
            
        except Exception as e:
            return {
                "action": "continue",
                "message": f"⚠️ Logging error: {str(e)}"
            }
    
    def _log_tool_event(self, logger, event_type, unique_fields, json_str, timestamp):
        """Log tool events with optimization"""
        tool = unique_fields.get('tool_name', 'Unknown')
        
        if event_type == 'PostToolUse':
            response = unique_fields.get('tool_response')
            if isinstance(response, list) and len(response) > 0:
                # For long responses, just show count
                if len(str(response)) > 500:
                    summary = f"Tool: {tool} (Response: {len(response)} items, {len(str(response))} chars)"
                    # Don't include huge response in JSON
                    compact_fields = {k: v for k, v in unique_fields.items() if k != 'tool_response'}
                    compact_fields['tool_response'] = f"<{len(response)} items>"
                    json_str = json.dumps(compact_fields, ensure_ascii=False, separators=(',', ':'))
                else:
                    summary = f"Tool: {tool} (Response: {len(response)} items)"
            else:
                summary = f"Tool: {tool}"
        else:
            summary = f"Tool: {tool}"
        
        logger.info(f"[{timestamp}] [{event_type}] - {summary} | JSON: {json_str}")


def main():
    """Main entry point for the optimized logger hook"""
    try:
        # Read raw input from stdin
        raw_input = sys.stdin.read()
        
        # Parse the JSON
        input_data = json.loads(raw_input)
        
        # Create logger and log the event
        logger = OptimizedClaudeLogger()
        result = logger.log_event(input_data, raw_json=raw_input)
        
        # Output result
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        error_result = {
            "action": "continue",
            "message": f"⚠️ Logger error: {str(e)}"
        }
        print(json.dumps(error_result))
        sys.exit(0)


if __name__ == "__main__":
    main()