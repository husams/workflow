#!/usr/bin/env python3
"""
Notification Event Logger Hook
Logs all Notification events using Python logging module
"""

import sys
import os

# Add the hooks directory to Python path to import universal_logger
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from universal_logger import main

if __name__ == "__main__":
    main()