import subprocess
import os
import pytz
from apscheduler.triggers.cron import  CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from services.scraper_service import clear_products
from utils.logging_config import logger
from utils.database import get_db

scheduler = BackgroundScheduler()

def get_project_paths():
    """Get the paths for the virtual environment and scraper directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    env_path = os.path.join(base_dir, 'env', 'Scripts', 'activate.bat')
    scraper_path = os.path.join(base_dir, 'FTCrawler')

    logger.info(f"Base directory: {base_dir}")
    logger.info(f"Path for virtual environment activation script: {env_path}")
    logger.info(f"Path for Scrapy scraper directory: {scraper_path}")

    return env_path, scraper_path

def run_scraper() -> None:
    """Run the Scrapy scraper for the 'free3d' spider."""
    try:
        db: Session = next(get_db())

        clear_products(db)

        env_path, scraper_path =get_project_paths()

        command = f"cmd /c \"{env_path} && cd {scraper_path} && scrapy crawl free3d\""

        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"Scrapy error: {stderr}")
        else:
            logger.info(f"Scrapy output: {stdout}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

pk_timezone = pytz.timezone('Asia/Karachi')

scheduler.add_job(run_scraper,
                  CronTrigger(hour=2, minute=0, second=0, timezone=pk_timezone),
                  id='scrapy_job',
                  replace_existing=True)

scheduler.start()
