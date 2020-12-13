from load_vac_utils import load_vacancies_pipeline, healthcheck
# from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from dotenv import load_dotenv

logging.basicConfig(level = 'DEBUG')


if __name__ == "__main__":
    load_dotenv()
    load_vacancies_pipeline()
    # sched = BlockingScheduler()
    #
    # sched.add_job(load_vacancies_pipeline, 'interval', minutes = 5)
    #
    # sched.add_job(healthcheck, 'interval', minutes = 1)
    # sched.start()
