import shutil
import sys
import os
import signal
# import time
from os import system, name
from timetable_manager import TTManager
from user_manager import *
from logger import ActivityLogger

logger = ActivityLogger(__name__)
FIRST_RUN = True


def clear_console():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def delete_temp_files():
    if os.path.exists('/tmp'):
        temp_folders = list(filter(lambda x: x.startswith('.com.google.Chrome'), os.listdir('/tmp')))
        for temp_folder in temp_folders:
            shutil.rmtree(os.path.join("/tmp/", temp_folder), ignore_errors=True)


# noinspection PyUnusedLocal
def kill_bot(signum, frame):
    logger.log_event_info("Killing teams sessions")
    users_kill()
    logger.log_event_info("Purging temporary files")
    delete_temp_files()
    logger.log_event_info("KILLING BOT")
    sys.exit()


signal.signal(signal.SIGINT, kill_bot)


def run_bot():
    global FIRST_RUN
    if FIRST_RUN:
        users_schedule_classes()
        users_login()
        FIRST_RUN = False
    logger.log_event_info('RUNNING BOT')
    # teams.join_class("CSE 5A 18CS55", "9:10", "10:10")
    try:
        users_deal_tasks()
        input()
        users_stop_dealing()
    except KeyboardInterrupt:
        pass


def manage_timetable():
    timetable = TTManager()
    while True:
        inp = int(input(
            "\n1.Add classes to timetable\n2.Delete classes from timetable\n3.View timetable\n4.Back\nEnter option :"))
        if inp == 1:
            timetable.add_classes()
        elif inp == 2:
            timetable.delete_classes()
        elif inp == 3:
            timetable.view_classes()
        else:
            break


def manage_user():
    while True:
        inp = int(input("\n1.Schedule classes\n2.Join class\n3.Schedule leave\n4.Login\n5.Back\nEnter option :"))
        if inp == 1:
            users_schedule_classes()
        elif inp == 2:
            user_join_class()
        elif inp == 3:
            user_join_class(leave=1)
        elif inp == 4:
            user_login()
        else:
            break


if __name__ == "__main__":
    try:
        users_initialize()
        # time.sleep(5)
        while True:
            try:
                op = int(input("\n1.Manage Timetable\n2.Manage User\n3.Start Bot\n4.Exit\nEnter option :"))
            except Exception as e:
                logger.log_event_error("Exeption Occured!", e)
            else:
                if op == 1:
                    manage_timetable()
                elif op == 2:
                    manage_user()
                elif op == 3:
                    run_bot()
                else:
                    kill_bot(0, 0)
                    break
    except Exception as e:
        logger.log_event_error("Exception Occured!")
        logger.logger.exception(e)
