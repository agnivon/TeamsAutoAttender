from teams_instance import TeamsInstance
from class_scheduler import join_task_scheduler
from threading import Lock
from logger import ActivityLogger


class User:
    def __init__(self, ign, email, passwd, table_name='timetable', att_token='kudi'):
        self.ign = ign
        self.email = email
        self.passwd = passwd
        self.teams = TeamsInstance(ign, email, passwd, att_token)
        self.table_name = table_name
        self._lock = Lock()
        self.logger = ActivityLogger(self.ign + ' user')
        self.logger.log_event_info("{} user created".format(self.ign))

    def login(self):
        with self._lock:
            self.teams.login()

    def schedule_classes(self):
        with self._lock:
            join_task_scheduler(self)

    def join_class(self, class_name, start_time, end_time):
        with self._lock:
            self.teams.join_class(class_name, start_time, end_time)

    def leave_class(self, class_name, start_time, end_time):
        with self._lock:
            self.teams.leave_class(class_name, start_time, end_time)

    def kill_instance(self):
        self.teams.kill()
