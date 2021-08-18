import schedule
import time
import sqlite3

from senderrors import mail_to_admin

conn = sqlite3.connect('db.sqlite')


def create_connection(db):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
    except ConnectionError as e:
        print(e)

    return conn


def time_wrapper(method):
    def wrapper(*args, **kw):
        start_time = int(round(time.time() * 1000))
        result = method(*args, **kw)
        end_time = int(round(time.time() * 1000))

        print(end_time - start_time, 'ms')
        return result

    return wrapper


@time_wrapper
def check_all_apps(conn):
    """
    Query all app_id in the appInfo table
    """
    error_message_to_admin = set()  # apps that doesn't work correctly
    minute_responce = 1  # Manually set the number of minutes between check apps status in database
    cur = conn.cursor()
    cur.execute(f"SELECT app_id FROM appInfo GROUP BY app_id HAVING MAX(appInfo.date) < ({time.time()} - {minute_responce} * 60)*1000;")
    rows = cur.fetchall()
    for row in range(len(rows)):
        value = rows[row][0]
        error_message_to_admin.add(value)
    print(error_message_to_admin)
    mail_to_admin(error_message_to_admin, ['sc2alex@yandex.ru'])
    return schedule.CancelJob


def scan_db():
    check_all_apps(conn)


schedule.every(1).minutes.do(scan_db)

while True:
    schedule.run_pending()
    time.sleep(1)
