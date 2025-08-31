#!/usr/bin/env python3
"""
Claude Event Log Viewer
Interactive tool to view and analyze Claude Code event logs
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import argparse
from collections import Counter

class LogViewer:
    """Interactive log viewer for Claude events"""
    
    def __init__(self, log_dir: Optional[Path] = None):
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            # Find project root and logs
            project_root = self.find_project_root()
            self.log_dir = project_root / '.claude_logs'
        
        if not self.log_dir.exists():
            print(f"⚠️  Log directory not found: {self.log_dir}")
            print("No logs have been generated yet.")
            sys.exit(1)
    
    def find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        
        # Look for .claude_logs directory
        while current != current.parent:
            if (current / '.claude_logs').exists():
                return current
            current = current.parent
        
        return Path.cwd()
    
    def get_today_logs(self) -> Optional[List[Dict]]:
        """Get today's JSON logs"""
        today = datetime.now().strftime("%Y%m%d")
        json_file = self.log_dir / f'claude_events_{today}.json'
        
        if not json_file.exists():
            return None
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def get_summary(self) -> Optional[Dict]:
        """Get activity summary"""
        summary_file = self.log_dir / 'activity_summary.json'
        
        if not summary_file.exists():
            return None
        
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def print_summary(self):
        """Print activity summary"""
        summary = self.get_summary()
        
        if not summary:
            print("No activity summary available.")
            return
        
        print("\n" + "="*60)
        print("📊 ACTIVITY SUMMARY")
        print("="*60)
        
        print(f"\n📈 Total Events: {summary.get('total_events', 0)}")
        print(f"📅 First Event: {summary.get('first_event', 'N/A')}")
        print(f"📅 Last Event: {summary.get('last_event', 'N/A')}")
        print(f"🔗 Unique Sessions: {len(summary.get('sessions', []))}")
        
        # Events by type
        print("\n📋 Events by Type:")
        for event_type, count in sorted(summary.get('events_by_type', {}).items()):
            print(f"  • {event_type}: {count}")
        
        # Tools used
        print("\n🔧 Tools Used:")
        for tool, count in sorted(summary.get('tools_used', {}).items(), 
                                 key=lambda x: x[1], reverse=True)[:10]:
            print(f"  • {tool}: {count} times")
        
        # Files accessed
        files = summary.get('files_accessed', [])
        if files:
            print(f"\n📁 Files Accessed: {len(files)} unique files")
            for file in files[:10]:
                print(f"  • {file}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
        
        # Recent commands
        commands = summary.get('commands_executed', [])
        if commands:
            print(f"\n💻 Recent Commands: (last 5)")
            for cmd in commands[-5:]:
                timestamp = cmd.get('timestamp', 'N/A')
                command = cmd.get('command', 'N/A')
                print(f"  [{timestamp}] {command}")
        
        # Errors
        errors = summary.get('errors', [])
        if errors:
            print(f"\n❌ Recent Errors: (last 3)")
            for error in errors[-3:]:
                timestamp = error.get('timestamp', 'N/A')
                event = error.get('event', 'N/A')
                error_msg = error.get('error', 'N/A')
                print(f"  [{timestamp}] {event}: {error_msg}")
    
    def print_recent_events(self, count: int = 20):
        """Print recent events"""
        logs = self.get_today_logs()
        
        if not logs:
            print("No logs for today.")
            return
        
        print("\n" + "="*60)
        print(f"📜 RECENT EVENTS (last {count})")
        print("="*60)
        
        for event in logs[-count:]:
            timestamp = event.get('timestamp', 'N/A')
            event_type = event.get('event_type', 'Unknown')
            tool = event.get('tool', '')
            
            print(f"\n[{timestamp}] {event_type}")
            
            if tool:
                print(f"  Tool: {tool}")
            
            if event_type == 'UserPromptSubmit':
                prompt_preview = event.get('prompt_preview', '')
                if prompt_preview:
                    print(f"  Prompt: {prompt_preview}")
            
            elif event_type in ['PreToolUse', 'PostToolUse']:
                if tool == 'Bash':
                    command = event.get('command', '')
                    if command:
                        print(f"  Command: {command}")
                elif tool in ['Write', 'Edit', 'Read']:
                    file_path = event.get('file_path', '')
                    if file_path:
                        print(f"  File: {file_path}")
                
                if event_type == 'PostToolUse':
                    success = event.get('success', 'N/A')
                    print(f"  Success: {success}")
                    if not success and 'error' in event:
                        print(f"  Error: {event['error']}")
    
    def search_logs(self, query: str):
        """Search logs for specific content"""
        logs = self.get_today_logs()
        
        if not logs:
            print("No logs for today.")
            return
        
        print(f"\n🔍 Searching for: '{query}'")
        print("="*60)
        
        matches = []
        for event in logs:
            # Search in JSON representation
            event_str = json.dumps(event, default=str).lower()
            if query.lower() in event_str:
                matches.append(event)
        
        print(f"Found {len(matches)} matching events:")
        
        for event in matches[:20]:  # Show first 20 matches
            timestamp = event.get('timestamp', 'N/A')
            event_type = event.get('event_type', 'Unknown')
            print(f"\n[{timestamp}] {event_type}")
            
            # Show relevant fields
            if 'tool' in event:
                print(f"  Tool: {event['tool']}")
            if 'command' in event:
                print(f"  Command: {event['command']}")
            if 'file_path' in event:
                print(f"  File: {event['file_path']}")
            if 'error' in event:
                print(f"  Error: {event['error']}")
    
    def analyze_performance(self):
        """Analyze performance metrics"""
        logs = self.get_today_logs()
        
        if not logs:
            print("No logs for today.")
            return
        
        print("\n" + "="*60)
        print("⚡ PERFORMANCE ANALYSIS")
        print("="*60)
        
        # Tool execution times (if available in future)
        tool_events = [e for e in logs if e.get('event_type') == 'PostToolUse']
        
        print(f"\n📊 Tool Executions: {len(tool_events)}")
        
        # Success rate
        successful = sum(1 for e in tool_events if e.get('success', True))
        if tool_events:
            success_rate = (successful / len(tool_events)) * 100
            print(f"✅ Success Rate: {success_rate:.1f}%")
        
        # Most used tools
        tool_counter = Counter(e.get('tool', 'Unknown') for e in tool_events)
        print("\n🔧 Most Used Tools:")
        for tool, count in tool_counter.most_common(5):
            print(f"  • {tool}: {count} executions")
        
        # Session analysis
        sessions = set(e.get('session_id', '') for e in logs if e.get('session_id'))
        print(f"\n🔗 Sessions: {len(sessions)}")
        
        # Event distribution
        event_counter = Counter(e.get('event_type', 'Unknown') for e in logs)
        print("\n📊 Event Distribution:")
        for event_type, count in event_counter.most_common():
            percentage = (count / len(logs)) * 100
            print(f"  • {event_type}: {count} ({percentage:.1f}%)")
    
    def export_logs(self, output_file: str, format: str = 'json'):
        """Export logs to file"""
        logs = self.get_today_logs()
        
        if not logs:
            print("No logs for today.")
            return
        
        output_path = Path(output_file)
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, default=str)
        elif format == 'csv':
            import csv
            
            # Flatten logs for CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if logs:
                    # Get all unique keys
                    all_keys = set()
                    for log in logs:
                        all_keys.update(log.keys())
                    
                    writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
                    writer.writeheader()
                    
                    for log in logs:
                        # Convert complex objects to strings
                        flat_log = {}
                        for key, value in log.items():
                            if isinstance(value, (dict, list)):
                                flat_log[key] = json.dumps(value)
                            else:
                                flat_log[key] = value
                        writer.writerow(flat_log)
        
        print(f"✅ Logs exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Claude Event Log Viewer')
    parser.add_argument('command', nargs='?', default='summary',
                       choices=['summary', 'recent', 'search', 'analyze', 'export'],
                       help='Command to execute')
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--count', '-c', type=int, default=20,
                       help='Number of recent events to show')
    parser.add_argument('--output', '-o', help='Output file for export')
    parser.add_argument('--format', '-f', choices=['json', 'csv'], default='json',
                       help='Export format')
    parser.add_argument('--log-dir', '-d', help='Custom log directory path')
    
    args = parser.parse_args()
    
    viewer = LogViewer(args.log_dir)
    
    if args.command == 'summary':
        viewer.print_summary()
    elif args.command == 'recent':
        viewer.print_recent_events(args.count)
    elif args.command == 'search':
        if not args.query:
            print("Error: --query required for search command")
            sys.exit(1)
        viewer.search_logs(args.query)
    elif args.command == 'analyze':
        viewer.analyze_performance()
    elif args.command == 'export':
        if not args.output:
            print("Error: --output required for export command")
            sys.exit(1)
        viewer.export_logs(args.output, args.format)


if __name__ == "__main__":
    main()