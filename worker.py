import schedule
import time
import sqlite3

conn = sqlite3.connect('db.sqlite')


def create_connection(db):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
    except ConnectionError as e:
        print(e)

    return conn


def timeme_wrapper(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))

        print(endTime - startTime,'ms')
        return result

    return wrapper

@timeme_wrapper
def select_all_tasks(conn):
    """
    Query all app_id in the appInfo table
    :param conn: the Connection object
    :return:
    """
    error_message_to_admin = set()  # apps that doesn't work correctly
    minute_responce = 1  # Manually set the number of minutes betweet check apps status in database
    cur = conn.cursor()
    cur.execute(f"SELECT app_id FROM appInfo GROUP BY app_id HAVING MAX(appInfo.date) < ({time.time()} - {minute_responce} * 60)*1000;")
    rows = cur.fetchall()

    for row in range(len(rows)):
        print(type(rows[row]))
        value = rows[row][0]
        error_message_to_admin.add(value)
        print(value)
    print(error_message_to_admin)


def scan_db():
    select_all_tasks(conn)
    print('Hello, World!')

def sched_job():
    schedule.every(1).seconds.do(scan_db)
    return schedule.CancelJob

schedule.every(0.5).minutes.do(scan_db)

while True:
    schedule.run_pending()
    time.sleep(1)