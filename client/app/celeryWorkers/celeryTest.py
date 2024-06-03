from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready, worker_shutdown
import time
from celery.utils.log import get_task_logger
from TheEdgeTools import driver, sign_in


app = Celery()
app.config_from_object('celeryConfig')
logger = get_task_logger(__name__)

# cd venv/EdgeBookingApp/app/celeryWorkers
# celery -A celeryTest worker --pool=solo -n testWorker1 -l INFO -c 1 -Q testQueue
# celery -A celeryTest control shutdown

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#
#     sender.add_periodic_task(5.0, test.s(5, 2), name='add every 5', expires=10)

@worker_ready.connect(sender='testWorker1')
def start_test(**kwargs):

    logger.info('start_test running.')
    task = test.delay()

@app.task(name='test', ignore_result=False)
def test():

    logger.info('Running test function.')
    return sign_in('secas20', 'AlwaysonEdge345!')
