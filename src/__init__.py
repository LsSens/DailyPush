#!/usr/bin/env python3
"""
DailyPush - Main package for automated GitHub commits
"""

__version__ = "1.0.0"
__author__ = "DailyPush Bot"
__description__ = "Keeps GitHub statistics always active with regular commits"

from .daily_push import DailyPush
from .git_manager import GitManager
from .commit_manager import CommitManager
from .file_manager import FileManager

__all__ = [
    'DailyPush',
    'GitManager', 
    'CommitManager',
    'FileManager'
]
