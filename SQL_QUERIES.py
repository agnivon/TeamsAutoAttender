LIST_TABLES = r"SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
CREATE_TABLE = r"CREATE TABLE {}({}, {}, {}, {})"
SEARCH_ROW = r"SELECT * FROM {} WHERE start_time='{}' AND day='{}'"
DELETE_ROW_REPLACE = r"DELETE FROM {} WHERE start_time='{}' AND day='{}'"
INSERT_ROW = "INSERT INTO {} VALUES ('{}','{}','{}','{}')"
DELETE_ROW = r"DELETE FROM {} WHERE class='{}' AND start_time='{}' AND end_time='{}' AND day='{}'"
VIEW_ROWS = r"SELECT * FROM {}"