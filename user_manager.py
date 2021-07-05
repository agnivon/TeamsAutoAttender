from threader import *
# from multiprocessor import *
from users import *
from class_scheduler import clear_schedule
from timetable_manager import get_class_details
from logger import ActivityLogger
# from discord_bot import run_discord_bot

USERS = open('users.txt', 'r').readlines()
users_list = []
logger = ActivityLogger(__name__)


def users_initialize():
    for creds in USERS:
        creds = creds.rstrip('\n').split()
        users_list.append(User(*creds))
        logger.log_event_info('Created user {}'.format(creds[0]))
    # start_discord_process(run_discord_bot)
    initialize_threads(len(users_list))


def users_schedule_classes():
    clear_schedule()
    for user in users_list:
        user.schedule_classes()


def users_deal_tasks():
    resume.set()


def users_stop_dealing():
    resume.clear()


def user_join_class(leave=0):
    print(*list(enumerate([user.ign for user in users_list], start=1)), sep='\n')
    try:
        while True:
            inp = input("Enter index number of user :")
            if inp:
                inp = int(inp)
                if 0 < inp <= len(users_list):
                    user = users_list[inp - 1]
                    args = get_class_details()[:-1]
                    if not leave:
                        add_task(user.join_class, *args)
                    else:
                        add_task(user.leave_class, *args)
                else:
                    print("Invalid Input")
            else:
                break
    except IndexError:
        print("Invalid Input")
        return


def users_login():
    for user in users_list:
        add_task(user.login)


def user_login():
    print(*list(enumerate([user.ign for user in users_list], start=1)), sep='\n')
    try:
        while True:
            inp = input("Enter index number of user :")
            if inp:
                inp = int(inp)
                if 0 < inp <= len(users_list):
                    user = users_list[inp - 1]
                    add_task(user.login)
                else:
                    print("Invalid Input")
            else:
                break
    except IndexError:
        print("Invalid Input")
        return


def users_kill():
    for user in users_list:
        user.kill_instance()
