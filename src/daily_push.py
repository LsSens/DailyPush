#!/usr/bin/env python3
"""
DailyPush - Main class for managing automated commits
"""

import os
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import git

from git_manager import GitManager
from commit_manager import CommitManager
from file_manager import FileManager

logger = logging.getLogger(__name__)

class DailyPush:
    def __init__(self, repo_path: str = "."):
        """
        Initialize DailyPush
        
        Args:
            repo_path: Path to Git repository
        """
        self.repo_path = Path(repo_path).resolve()
        
        # Initialize managers
        self.git_manager = GitManager(self.repo_path)
        self.commit_manager = CommitManager(self.git_manager)
        self.file_manager = FileManager(self.repo_path)
        
        # Initialize repository
        self.initialize_repo()
        
    def initialize_repo(self):
        """Initialize Git repository or create new one if needed"""
        try:
            self.git_manager.initialize_repo()
            logger.info(f"Repository initialized: {self.repo_path}")
        except Exception as e:
            logger.error(f"Error initializing repository: {e}")
            raise
    
    def daily_routine(self):
        """Complete daily routine: multiple commits + push"""
        logger.info("Starting daily routine...")
        
        # Define how many commits to make (configurable via .env)
        commits_min = int(os.getenv('COMMITS_MIN', 25))
        commits_max = int(os.getenv('COMMITS_MAX', 30))
        commits_to_make = random.randint(commits_min, commits_max)
        logger.info(f"🎯 Making {commits_to_make} commits before push...")
        
        # Make multiple commits
        for i in range(commits_to_make):
            logger.info(f"📝 Commit {i+1}/{commits_to_make}...")
            
            if self.commit_manager.make_commit():
                logger.info(f"✅ Commit {i+1} completed successfully!")
            else:
                logger.error(f"❌ Failed on commit {i+1}")
                return False
        
        # After all commits, do the push
        total_commits = len(list(self.git_manager.repo.iter_commits()))
        logger.info(f"🎉 All {commits_to_make} commits completed!")
        logger.info(f"📤 Pushing {total_commits} commits to GitHub...")
        
        try:
            if self.git_manager.push_to_remote():
                logger.info("🎉 Daily routine completed successfully!")
                logger.info(f"✅ {total_commits} commits sent to GitHub!")
                logger.info("📊 Your GitHub statistics are updated!")
            else:
                logger.warning("⚠️ All commits completed, but push failed")
                logger.info("💡 Run again to retry push")
        except Exception as e:
            logger.warning(f"⚠️ All commits completed, but push failed: {e}")
            logger.info("💡 Run again to retry push")
        
        return True
