from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

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
    print(message)
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

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()

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