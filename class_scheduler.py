import schedule
from threader import add_task
from database_handler import DBHandler
from logger import ActivityLogger

logger = ActivityLogger(__name__)


def join_task_scheduler(user):
    database = DBHandler()
    classdata = database.retrieve_all_rows()
    logger.log_event_info('Started scheduling classes for {}'.format(user.ign))
    for row in classdata:
        name, start_time, end_time, day = row
        if day.lower() == "monday":
            schedule.every().monday.at(start_time).do(add_task, user.join_class, name, start_time, end_time)
            
        elif day.lower() == "tuesday":
            schedule.every().tuesday.at(start_time).do(add_task, user.join_class, name, start_time, end_time)
            
        elif day.lower() == "wednesday":
            schedule.every().wednesday.at(start_time).do(add_task, user.join_class, name, start_time, end_time)
            
        elif day.lower() == "thursday":
            schedule.every().thursday.at(start_time).do(add_task, user.join_class, name, start_time, end_time)
            
        elif day.lower() == "friday":
            schedule.every().friday.at(start_time).do(add_task, user.join_class, name, start_time, end_time)
            
        elif day.lower() == "saturday":
            schedule.every().saturday.at(start_time).do(add_task, user.join_class, name, start_time, end_time)
            
        elif day.lower() == "sunday":
            schedule.every().sunday.at(start_time).do(add_task, user.join_class, name, start_time, end_time)

        logger.log_event_info("Scheduled class '%s' on %s at %s" % (name, day, start_time))

    database.close()


def clear_schedule():
    schedule.clear()


def run_pending():
    schedule.run_pending()
