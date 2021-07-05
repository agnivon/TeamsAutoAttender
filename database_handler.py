import sqlite3
from SQL_QUERIES import *
from logger import ActivityLogger

logger = ActivityLogger(__name__)


class DBHandler:
    def __init__(self, table_name='timetable'):
        self.conn = sqlite3.connect('timetable.db')
        logger.log_event_info('Connected to database')
        self.c = self.conn.cursor()
        self.table_name = table_name
        if (table_name,) not in [row for row in self.c.execute(LIST_TABLES)]:
            self.c.execute(
                CREATE_TABLE.format(table_name, "class text", "start_time text", "end_time text",
                                    "day text"))
            logger.log_event_info('Created new table')
        self.conn.commit()

    def add(self, name, start_time, end_time, day):
        table = self.table_name
        if [row for row in self.c.execute(SEARCH_ROW.format(table, start_time, day))]:
            logger.log_event_info('Same {} class found. Prompt to replace'.format(name))
            ask = input("Replace class?(yY/nN)")
            if ask in ['y', 'Y']:
                self.c.execute(DELETE_ROW_REPLACE.format(table, start_time, day))
                logger.log_event_info('Redundant {} class deleted'.format(name))
        self.c.execute(INSERT_ROW.format(table, name, start_time, end_time, day))
        logger.log_event_info('New {} class added successfully'.format(name))
        self.conn.commit()

    def delete(self, name, start_time, end_time, day):
        table = self.table_name
        self.c.execute(DELETE_ROW.format(table, name, start_time, end_time, day))
        logger.log_event_info('{} class deleted successfully'.format(name))
        self.conn.commit()

    def view(self):
        for row in self.c.execute(VIEW_ROWS.format(self.table_name)):
            print(row)

    def retrieve_all_rows(self):
        return [row for row in self.c.execute(VIEW_ROWS.format(self.table_name))]

    def close(self):
        self.conn.close()
        logger.log_event_info('Closed database')
