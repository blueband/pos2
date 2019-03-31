import sqlite3
import  os
DEFAULT_PATH = os.path.join(os.path.dirname(__file__),'stock_DB.sqlite')


def con(db_path=DEFAULT_PATH):
    dbconn = sqlite3.connect(db_path)
    return dbconn