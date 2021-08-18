from flask import Flask, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
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


# req = client.post('/api/apps/', json = {"app_id":23, "message":"OK:200"})
@app.route('/api/apps/', methods=['POST'])
def add_info():
    message = request.json
    app_id = message["app_id"]
    if message.get("message"):
        mes = message.get("message")
        vardb = appInfo(app_id=app_id, message=mes)
    else:
        vardb = appInfo(app_id=app_id)
    session.add(vardb)
    session.commit()
    return "233"


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()



