from logging import getLogger

from apscheduler.schedulers.blocking import BlockingScheduler

from project.task import main, update_deals
from conf.log_conf import setup_logging

setup_logging()
scheduler = BlockingScheduler()
logger = getLogger(__name__)

scheduler.add_job(main, "cron", hour="9,14,19")
scheduler.add_job(update_deals, "cron", hour="8,13,18")

if __name__ == "__main__":
    logger.info("START PROJECT")
    scheduler.start()
