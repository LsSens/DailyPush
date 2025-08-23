#!/usr/bin/env python3
"""
DailyPush - Main entry script
Run this file to execute DailyPush
"""

import sys
from pathlib import Path

# Add src to path to import modules
sys.path.append(str(Path(__file__).parent / "src"))

from main import main

if __name__ == "__main__":
    main()
