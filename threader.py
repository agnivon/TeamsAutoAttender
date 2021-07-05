import threading
from logger import ActivityLogger
from queue import Queue

tasks = Queue(maxsize=5)
threads = []
logger = ActivityLogger(__name__)
resume = threading.Event()


def add_task(job_func, *args):
    tasks.put({'job_func': job_func, 'args': args})
    logger.log_event_debug('Created join task {}'.format(args))


def deal_task():
    import class_scheduler
    while True:
        resume.wait()
        class_scheduler.run_pending()


def execute_task():
    while True:
        task = tasks.get()
        resume.wait()
        job_func = task['job_func']
        args = task['args']
        logger.log_event_debug('{} going to execute {} task'.format(threading.currentThread().name, args))
        job_func(*args)
        logger.log_event_debug('{} done executing {} task'.format(threading.currentThread().name, args))


def initialize_threads(count):
    dealer_thread = threading.Thread(target=deal_task, name="Dealer Thread", daemon=True)
    threads.append(dealer_thread)
    logger.log_event_debug("Dealer thread created")
    for i in range(count):
        thread = threading.Thread(name='Thread {}'.format(i + 1), target=execute_task, daemon=True)
        logger.log_event_debug("Thread {} created".format(i + 1))
        threads.append(thread)
    start_threads()


def start_threads():
    for thread in threads:
        thread.start()
        logger.log_event_debug("{} started".format(thread.name))
