from os import getenv
from logging import getLogger
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from project.task import main
from conf.log_conf import setup_logging

task_delay = int(getenv("TASK_DELAY_INTERVAL"))

setup_logging()
scheduler = BlockingScheduler()
logger = getLogger(__name__)
scheduler.add_job(
    main,
    "interval",
    hours=task_delay,
    next_run_time=datetime.now()
)

if __name__ == "__main__":
    logger.info("START PROJECT")
    scheduler.start()
