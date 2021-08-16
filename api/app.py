import datetime
from flask import Flask, jsonify, request

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)

client = app.test_client()

engine = create_engine("sqlite:///app_status.db")

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

app.debug = True
app.secret_key = "123"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


# @app.route('/api/apps/<int:app_id>/<message>/', methods=['GET'])
# def get_list(app_id, message):
#     return f"<p> fff {app_id}{message}</p>"

@app.route('/api/apps/<int:app_id>/', methods=['POST'])
def add_info(app_id):
    message = request.POST['message']



# @app.route('/tutorials', methods=['POST'])
# def update_list():
#     new_one = request.json
#     tutorials.append(new_one)
#     return jsonify(tutorials)
#
#
# @app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
# def update_tutorial(tutorial_id):
#     item = next((x for x in tutorials if x['id'] == tutorial_id), None)
#     params = request.json
#     if not item:
#         return {'message': 'No tutorials with this id'}, 400
#     item.update(params)
#     return item
#
#
# @app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
# def delete_tutorial(tutorial_id):
#     idx, _ = next((x for x in enumerate(tutorials)
#                    if x[1]['id'] == tutorial_id), (None, None))
#
#     tutorials.pop(idx)
#     return '', 204


if __name__ == '__main__':
    app.run()
