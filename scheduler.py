#!/usr/bin/env python3
"""
Scheduler - Schedules DailyPush execution locally
"""

import schedule
import time
import logging
import sys
from pathlib import Path

# Add src to path to import modules
sys.path.append(str(Path(__file__).parent / "src"))

from main import main

# Configure logging (console only, no file logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_daily_push():
    """Execute DailyPush"""
    try:
        logger.info("🕐 Executing scheduled DailyPush...")
        main()
        logger.info("✅ Scheduled DailyPush executed successfully!")
    except Exception as e:
        logger.error(f"❌ Error executing scheduled DailyPush: {e}")

def main_scheduler():
    """Main scheduler function"""
    logger.info("🚀 Starting DailyPush Scheduler...")
    
    # Schedule daily execution at 09:00 (configurable via .env)
    execution_time = os.getenv('EXECUTION_TIME', '09:00')
    schedule.every().day.at(execution_time).do(run_daily_push)
    
    logger.info(f"📅 DailyPush scheduled to run every day at {execution_time}")
    logger.info("⏰ Press Ctrl+C to stop the scheduler")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    main_scheduler()
