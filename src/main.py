#!/usr/bin/env python3
"""
DailyPush - Main script for automated daily GitHub commits
Keeps GitHub statistics always active with regular commits
"""

import sys
import logging
from dotenv import load_dotenv

from daily_push import DailyPush

# Configure logging (console only, no file logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function"""
    load_dotenv()
    
    # Initialize DailyPush (creates Git repository if needed)
    daily_push = DailyPush()
    
    # Execute daily routine
    success = daily_push.daily_routine()
    
    if success:
        logger.info("DailyPush executed successfully!")
        
        # Check if it's the first commit and give instructions
        if len(list(daily_push.git_manager.repo.iter_commits())) == 1:
            logger.info("")
            logger.info("🎉 First commit completed successfully!")
            logger.info("📋 Next steps to sync with GitHub:")
            logger.info("1. Create a repository on GitHub")
            logger.info("2. Run: git remote add origin <REPOSITORY-URL>")
            logger.info("3. Run: git push -u origin master")
            logger.info("4. Configure GitHub Actions for complete automation")
        
        sys.exit(0)
    else:
        logger.error("DailyPush failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
