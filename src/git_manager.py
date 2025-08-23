#!/usr/bin/env python3
"""
GitManager - Manages Git operations for DailyPush
"""

import os
import logging
from pathlib import Path

import git

logger = logging.getLogger(__name__)

class GitManager:
    def __init__(self, repo_path: Path):
        """
        Initialize GitManager
        
        Args:
            repo_path: Path to Git repository
        """
        self.repo_path = repo_path
        self.repo = None
        
    def initialize_repo(self):
        """Initialize Git repository or create new one if needed"""
        try:
            # Try to open existing repository
            self.repo = git.Repo(self.repo_path)
            logger.info(f"Existing repository initialized: {self.repo_path}")
        except git.InvalidGitRepositoryError:
            # Create new Git repository
            logger.info("Creating new Git repository...")
            self.repo = git.Repo.init(self.repo_path)
            
            # Configure Git user (uses environment variables if available)
            try:
                git_name = os.getenv('GIT_USER_NAME', 'DailyPush Bot')
                git_email = os.getenv('GIT_USER_EMAIL', 'dailypush@github.com')
                
                self.repo.config_writer().set_value("user", "name", git_name).release()
                self.repo.config_writer().set_value("user", "email", git_email).release()
                logger.info(f"Git configuration set: {git_name} <{git_email}>")
            except:
                logger.warning("Could not set default Git user configuration")
            
            logger.info(f"New Git repository created: {self.repo_path}")
        except Exception as e:
            logger.error(f"Error initializing repository: {e}")
            raise
    
    def push_to_remote(self, remote_name: str = "origin") -> bool:
        """
        Push to remote repository
        
        Args:
            remote_name: Remote name (default: origin)
            
        Returns:
            True if push was successful, False otherwise
        """
        try:
            remote = self.repo.remotes[remote_name]
            remote.push()
            logger.info(f"Push completed to {remote_name}")
            return True
        except Exception as e:
            logger.error(f"Error pushing to remote: {e}")
            return False
    
    def get_total_commits(self) -> int:
        """Return total commits in repository"""
        return len(list(self.repo.iter_commits()))
    
    def is_first_commit(self) -> bool:
        """Check if this is the first commit"""
        return self.get_total_commits() == 0
