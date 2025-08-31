#!/usr/bin/env python3
"""
Universal Event Logger for Claude Code
Logs all events to a single file with session ID in the filename
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

class ClaudeEventLogger:
    """Comprehensive logger for all Claude Code events - single file per session"""
    
    # Class variable to store the session logger across instances
    _session_logger = None
    _session_id = None
    _log_file_path = None
    
    def __init__(self):
        self.project_root = self.find_project_root()
        self.log_dir = self.project_root / '.claude_logs'
        self.log_dir.mkdir(exist_ok=True)
        
    def find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        
        # Look for common project markers
        markers = ['.git', '.claude', 'package.json', 'requirements.txt', 
                  'pyproject.toml', 'Cargo.toml', 'go.mod']
        
        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    return current
            current = current.parent
        
        # Default to current working directory
        return Path.cwd()
    
    def get_or_create_session_logger(self, session_id: str) -> logging.Logger:
        """Get existing session logger or create new one"""
        
        # If we already have a logger for this session, return it
        if ClaudeEventLogger._session_logger and ClaudeEventLogger._session_id == session_id:
            return ClaudeEventLogger._session_logger
        
        # Check if a log file already exists for this session
        existing_log = None
        for log_file in self.log_dir.glob(f'claude_session_{session_id[:8]}*.log'):
            if session_id[:8] in str(log_file):
                existing_log = log_file
                break
        
        # Create new session logger
        ClaudeEventLogger._session_id = session_id
        
        # Create logger with session-specific name
        logger_name = f'Claude.Session.{session_id}'
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()  # Clear any existing handlers
        
        # Use existing log file or create new one (no timestamp in filename)
        if existing_log:
            log_file_path = existing_log
            log_filename = existing_log.name
        else:
            log_filename = f'claude_session_{session_id[:8]}.log'
            log_file_path = self.log_dir / log_filename
        ClaudeEventLogger._log_file_path = log_file_path
        
        # Create rotating file handler for the session log
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=50*1024*1024,  # 50MB max per file
            backupCount=3,          # Keep 3 backups
            encoding='utf-8',
            mode='a'  # Append mode to continue existing sessions
        )
        
        # Create simplified formatter - event type first, no redundant timestamp
        formatter = logging.Formatter(
            fmt='%(message)s'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Add handler to logger
        logger.addHandler(file_handler)
        
        # Also create a JSON lines handler for structured data
        json_filename = f'claude_session_{session_id[:8]}.jsonl'
        json_file_path = self.log_dir / json_filename
        json_handler = logging.FileHandler(json_file_path, encoding='utf-8', mode='a')
        json_formatter = logging.Formatter('%(message)s')
        json_handler.setFormatter(json_formatter)
        json_handler.setLevel(logging.DEBUG)
        
        # Create a separate logger for JSON output
        json_logger_name = f'Claude.JSON.{session_id}'
        json_logger = logging.getLogger(json_logger_name)
        json_logger.setLevel(logging.DEBUG)
        json_logger.handlers.clear()
        json_logger.addHandler(json_handler)
        json_logger.propagate = False
        
        # Store both loggers
        ClaudeEventLogger._session_logger = logger
        ClaudeEventLogger._json_logger = json_logger
        
        return logger
    
    def log_event(self, event_data: Dict[str, Any], raw_json: Optional[str] = None) -> Dict[str, Any]:
        """Log event to session-specific file"""
        try:
            # Extract session ID from event data
            session_id = event_data.get('sessionId') or event_data.get('session_id', 'unknown')
            
            # Handle nested session_id in event_data
            if session_id == 'unknown' and 'event_data' in event_data:
                nested_data = event_data.get('event_data', {})
                session_id = nested_data.get('session_id', 'unknown')
            
            # Get or create session logger
            logger = self.get_or_create_session_logger(session_id)
            json_logger = getattr(ClaudeEventLogger, '_json_logger', None)
            
            # Extract event information - check multiple possible locations
            event_type = event_data.get('hook_event_name', 'Unknown')
            if event_type == 'Unknown':
                event_type = event_data.get('event', 'Unknown')
            if event_type == 'Unknown' and 'event_data' in event_data:
                nested_data = event_data.get('event_data', {})
                event_type = nested_data.get('hook_event_name', nested_data.get('event', 'Unknown'))
            
            timestamp = event_data.get('timestamp', datetime.now().timestamp())
            formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Use the original event_data as the log entry (flat structure from Claude)
            # Don't wrap it in another structure
            log_entry = event_data.copy()
            
            # Remove redundant fields that appear in every event
            filtered_data = {k: v for k, v in event_data.items() 
                           if k not in ['transcript_path', 'cwd']}
            
            # Use filtered JSON for logging
            json_str = json.dumps(filtered_data, ensure_ascii=False, separators=(',', ':'))
            
            # Log based on event type
            if event_type in ['PreToolUse', 'PostToolUse']:
                self._log_tool_event(logger, log_entry, event_data, event_type, json_str)
            elif event_type == 'UserPromptSubmit':
                self._log_prompt_event(logger, log_entry, event_data, json_str)
            elif event_type == 'Notification':
                self._log_notification_event(logger, log_entry, event_data, json_str)
            elif event_type in ['SessionStart', 'SessionEnd']:
                self._log_session_event(logger, log_entry, event_data, event_type, json_str)
            elif event_type in ['Stop', 'SubagentStop']:
                self._log_agent_event(logger, log_entry, event_data, event_type, json_str)
            elif event_type == 'PreCompact':
                self._log_compact_event(logger, log_entry, event_data, json_str)
            else:
                # Generic logging for unknown events
                logger.info(f"[{formatted_time}] [{event_type}] - Event logged | JSON: {json_str}")
                if event_type != 'Unknown':
                    # Log additional details for known but unhandled events
                    logger.debug(f"[{formatted_time}] [{event_type}] - Details: {json_str[:500]}")
            
            # Log to JSON file - use filtered JSON without redundant fields
            if json_logger:
                json_logger.info(json.dumps(filtered_data, ensure_ascii=False, default=str))
            
            # Update activity summary
            self.update_activity_summary(log_entry)
            
            return {
                "action": "continue",
                "message": f"✓ Logged {event_type} to session {session_id[:8]}"
            }
            
        except Exception as e:
            # Log error but don't block Claude's operation
            error_msg = f"Logging error in {event_type}: {str(e)}"
            if ClaudeEventLogger._session_logger:
                ClaudeEventLogger._session_logger.error(error_msg, exc_info=True)
            
            return {
                "action": "continue",
                "message": f"⚠️ Logging error (operation continued): {str(e)}"
            }
    
    def _log_tool_event(self, logger, log_entry, event_data, event_type, json_str):
        """Log tool-specific events"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Extract tool information - check multiple formats
        tool = event_data.get('tool_name', event_data.get('tool', 'Unknown'))
        parameters = event_data.get('tool_input', event_data.get('parameters', {}))
        
        # Check nested event_data for alternate format
        if tool == 'Unknown' and 'event_data' in event_data:
            nested = event_data['event_data']
            tool = nested.get('tool_name', nested.get('tool', 'Unknown'))
            parameters = nested.get('tool_input', nested.get('parameters', {}))
        
        # Don't add duplicate fields - they're already in event_data
        
        # Get response for PostToolUse
        response = None
        if event_type == 'PostToolUse':
            response = event_data.get('tool_response')
            if response is None and 'event_data' in event_data:
                response = event_data['event_data'].get('tool_response')
        
        # Create a summary for the human-readable part
        if event_type == 'PostToolUse' and response:
            if isinstance(response, list) and len(response) > 0:
                summary = f"Tool: {tool} (Response: {len(response)} items)"
            elif isinstance(response, dict):
                success = response.get('success', 'unknown')
                summary = f"Tool: {tool} (Success: {success})"
            else:
                summary = f"Tool: {tool} (Response type: {type(response).__name__})"
        else:
            summary = f"Tool: {tool}"
        
        logger.info(f"[{timestamp}] [{event_type}] - {summary} | JSON: {json_str}")
    
    def _log_prompt_event(self, logger, log_entry, event_data, json_str):
        """Log user prompt events"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        prompt = event_data.get('prompt', '')
        
        # Check nested format
        if not prompt and 'event_data' in event_data:
            prompt = event_data['event_data'].get('prompt', '')
        
        # Don't add duplicate fields - prompt is already in event_data
        
        # Single line with all information
        logger.info(f"[{timestamp}] [UserPromptSubmit] - Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''} | JSON: {json_str}")
    
    def _log_notification_event(self, logger, log_entry, event_data, json_str):
        """Log notification events"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        notification_type = event_data.get('type', 'info')
        message = event_data.get('message', '')
        
        logger.info(f"[{timestamp}] [Notification] - {message} | JSON: {json_str}")
    
    def _log_session_event(self, logger, log_entry, event_data, event_type, json_str):
        """Log session events"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session_id = log_entry.get('session_id', 'unknown')
        
        if event_type == 'SessionStart':
            logger.info(f"[{timestamp}] [SessionStart] - Session: {session_id} | JSON: {json_str}")
        else:  # SessionEnd
            reason = event_data.get('reason', event_data.get('event_data', {}).get('reason', 'unknown'))
            logger.info(f"[{timestamp}] [SessionEnd] - Reason: {reason} | JSON: {json_str}")
    
    def _log_agent_event(self, logger, log_entry, event_data, event_type, json_str):
        """Log agent stop events"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        agent_name = event_data.get('agent', 'main')
        
        if event_type == 'Stop':
            logger.info(f"[{timestamp}] [Stop] - Main agent stopped | JSON: {json_str}")
        else:
            logger.info(f"[{timestamp}] [SubagentStop] - Agent: {agent_name} | JSON: {json_str}")
    
    def _log_compact_event(self, logger, log_entry, event_data, json_str):
        """Log context compaction events"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        context_size = event_data.get('contextSize', 0)
        reason = event_data.get('reason', 'size_limit')
        
        logger.warning(f"[{timestamp}] [PreCompact] - Size: {context_size} | JSON: {json_str}")
    
    def update_activity_summary(self, log_entry: Dict[str, Any]):
        """Update activity summary file"""
        try:
            summary_file = self.log_dir / 'activity_summary.json'
            
            # Load existing summary
            if summary_file.exists():
                try:
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content and content != '{}':
                            summary = json.loads(content)
                        else:
                            summary = self._create_empty_summary()
                except (json.JSONDecodeError, IOError, ValueError):
                    summary = self._create_empty_summary()
            else:
                summary = self._create_empty_summary()
            
            # Update summary
            summary['total_events'] += 1
            event_type = log_entry.get('event_type', 'Unknown')
            summary['events_by_type'][event_type] = summary['events_by_type'].get(event_type, 0) + 1
            
            # Track session and its log file
            session_id = log_entry.get('session_id', 'unknown')
            if session_id not in summary['sessions']:
                summary['sessions'][session_id] = {
                    'start_time': log_entry.get('timestamp'),
                    'event_count': 0,
                    'log_file': str(ClaudeEventLogger._log_file_path) if ClaudeEventLogger._log_file_path else None
                }
            summary['sessions'][session_id]['event_count'] += 1
            summary['sessions'][session_id]['last_event'] = log_entry.get('timestamp')
            
            # Update other metrics
            if 'tool' in log_entry:
                tool = log_entry['tool']
                summary['tools_used'][tool] = summary['tools_used'].get(tool, 0) + 1
            
            summary['last_event'] = log_entry.get('timestamp')
            if not summary['first_event']:
                summary['first_event'] = log_entry.get('timestamp')
            
            # Write updated summary
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
                
        except Exception as e:
            if ClaudeEventLogger._session_logger:
                ClaudeEventLogger._session_logger.error(f"Failed to update activity summary: {e}")
    
    def _create_empty_summary(self):
        """Create empty summary structure"""
        return {
            'total_events': 0,
            'events_by_type': {},
            'tools_used': {},
            'sessions': {},
            'first_event': None,
            'last_event': None
        }


def main():
    """Main entry point for the logger hook"""
    try:
        # Configure basic logging for the script itself
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s | %(levelname)s | %(message)s'
        )
        
        # Read raw input from stdin as string to preserve exact format
        raw_input = sys.stdin.read()
        
        # Parse the JSON for processing
        input_data = json.loads(raw_input)
        
        # Create logger and log the event with both parsed and raw data
        logger = ClaudeEventLogger()
        result = logger.log_event(input_data, raw_json=raw_input)
        
        # Output result
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        # Don't block Claude's operation even if logging fails
        error_result = {
            "action": "continue",
            "message": f"⚠️ Logger error (operation continued): {str(e)}"
        }
        print(json.dumps(error_result))
        sys.exit(0)


if __name__ == "__main__":
    main()