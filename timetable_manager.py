from database_handler import DBHandler
from logger import ActivityLogger
import re

logger = ActivityLogger(__name__)


def validate_input(regex, inp):
    if not re.match(regex, inp):
        return False
    return True


def validate_day(inp):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if inp.lower() in days:
        return True
    else:
        return False


def get_class_details():
    name = input("Enter class name : ")
    start_time = input("Enter class start time in 24 hour format: (HH:MM) ")
    while not (validate_input(r"\d\d:\d\d", start_time)):
        print("Invalid input, try again")
        start_time = input("Enter class start time in 24 hour format: (HH:MM) ")

    end_time = input("Enter class end time in 24 hour format: (HH:MM) ")
    while not (validate_input(r"\d\d:\d\d", end_time)):
        print("Invalid input, try again")
        end_time = input("Enter class end time in 24 hour format: (HH:MM) ")

    day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")
    while not (validate_day(day.strip())):
        print("Invalid input, try again")
        day = input("Enter day (Monday/Tuesday/Wednesday..etc) : ")
    return name, start_time, end_time, day


class TTManager:
    def __init__(self):
        self.database = DBHandler()

    def add_classes(self):
        while True:
            self.view_classes()
            inp = int(input("1. Add class\n2. Done adding\nEnter option : "))
            if inp == 1:
                name, start_time, end_time, day = get_class_details()
                self.database.add(name, start_time, end_time, day)
                logger.log_event_info('{} class added to database'.format(name))
            else:
                break

    def delete_classes(self):
        while True:
            self.view_classes()
            inp = int(input("1. Delete class\n2. Done deleting\nEnter option : "))
            if inp == 1:
                name, start_time, end_time, day = get_class_details()
                self.database.delete(name, start_time, end_time, day)
                logger.log_event_info('{} class deleted from database'.format(name))
            else:
                break

    def view_classes(self):
        self.database.view()
        logger.log_event_info('Viewing classes')
