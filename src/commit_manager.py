#!/usr/bin/env python3
"""
CommitManager - Manages commits for DailyPush
"""

import logging
from datetime import datetime

from file_manager import FileManager

logger = logging.getLogger(__name__)

class CommitManager:
    def __init__(self, git_manager):
        """
        Initialize CommitManager
        
        Args:
            git_manager: GitManager instance
        """
        self.git_manager = git_manager
        self.file_manager = FileManager(git_manager.repo_path)
        
    def get_random_activity_message(self) -> str:
        """Return a random message for the commit"""
        activities = [
            "Updating documentation",
            "Code improvements",
            "New features",
            "Bug fixes",
            "Daily updates",
            "Performance optimizations",
            "Interface improvements",
            "Data updates",
            "Code refactoring",
            "Architecture improvements",
            "Fine adjustments",
            "Preventive maintenance",
            "General optimizations",
            "Deploy preparation",
            "Security updates"
        ]
        import random
        return random.choice(activities)
    
    def make_commit(self, force: bool = False) -> bool:
        """
        Make daily commit - ALWAYS creates a commit to keep statistics active
        
        Args:
            force: If True, force commit even without changes
            
        Returns:
            True if commit was successful, False otherwise
        """
        try:
            # Check if it's the first commit
            is_first_commit = self.git_manager.is_first_commit()
            
            # ALWAYS create a file for commit (even without changes)
            logger.info("Creating file for daily commit...")
            self.file_manager.create_daily_file(self.git_manager.repo)
            
            # Add all files except logs
            self.git_manager.repo.index.add('*')
            
            # Remove log files from staging area
            self._remove_log_files_from_staging()
            
            # Create commit message
            if is_first_commit:
                message = "First commit - DailyPush setup"
                logger.info("Creating first commit...")
            else:
                message = self.get_random_activity_message()
            
            # Make the commit
            commit = self.git_manager.repo.index.commit(message)
            logger.info(f"Commit completed: {commit.hexsha[:8]} - {message}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error making commit: {e}")
            return False
    
    def _remove_log_files_from_staging(self):
        """Remove log files from staging area"""
        try:
            # List all files in staging area
            staged_files = [item.a_path for item in self.git_manager.repo.index.diff('HEAD')]
            # Remove logs
            for file_path in staged_files:
                if file_path.endswith('.log'):
                    self.git_manager.repo.index.remove([file_path])
                    logger.info(f"Log file removed from commit: {file_path}")
        except Exception as e:
            logger.debug(f"Error removing logs: {e}")
    
    def should_push_to_github(self) -> tuple[bool, int, int]:
        """
        Check if should push to GitHub
        
        Returns:
            (should_push, total_commits, remaining_commits)
        """
        total_commits = self.git_manager.get_total_commits()
        
        # Define random limit between 25 and 30 commits
        if not hasattr(self, '_push_threshold'):
            import random
            self._push_threshold = random.randint(25, 30)
            logger.info(f"🎯 Commit limit set: {self._push_threshold}")
        
        # Push when limit is reached
        if total_commits >= self._push_threshold:
            return True, total_commits, 0
        
        # Calculate how many commits still needed
        commits_needed = self._push_threshold - total_commits
        return False, total_commits, commits_needed
