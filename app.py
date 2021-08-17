from flask import Flask, jsonify, request

from celery import Celery
from celery.schedules import crontab

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

CELERY_TASK_LIST = [
    'main.tasks'
]


def make_celery():
    celery = Celery(
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=CELERY_TASK_LIST
    )

    celery.conf.task_routes = {
        'web.*': {'queue': 'web'}
    }

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

cel = Celery()  # декоратор @cel Celery

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))

Base = declarative_base()
Base.query = session.query_property()


from models import *


Base.metadata.create_all(bind=engine)

# @app.route('/api/apps/<int:app_id>/<message>/', methods=['GET'])
# def get_list(app_id, message):
#     return f"<p> fff {app_id}{message}</p>"

@app.route('/api/apps/', methods=['POST'])
def add_info():
    message = request.json
    app_id = message["app_id"]
    #mes = "noinfo"
    if message.get("message"):
        mes = message.get("message")
        vardb = appInfo(app_id=app_id, message=mes)
    else:
        vardb = appInfo(app_id=app_id)
    session.add(vardb)
    session.commit()
    return "233"

# req = client.post('/api/apps/', json = {"app_id":23, "message":"abcdefg"})
#sd = session.query(appInfo).filter_by(app_id=88).order_by(func.max(appInfo.date)).all()


@cel.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@cel.task
def test(arg):
    print(arg)

@cel.task
def add(x, y):
    z = x + y
    print(z)




cel.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
cel.conf.timezone = 'UTC'





@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()

#q = session.query(Apps.app_id, func.max(Apps.ts).group_by(User.app_id).having(func.max(Apps.ts) < (time.time()-N*60)*1000)



# query = session.query(
#     func.date(SpendEstimation.time).label('date'),
#     SpendEstimation.resource_id,
#     SpendEstimation.time
# ).distinct(
#     func.date(SpendEstimation.time).label('date')
# ).order_by(
#     func.date(SpendEstimation.time).label('date'),
#     SpendEstimation.time
# )
#query.filter(User.bank_address == request.form['bank_address_field']).first()