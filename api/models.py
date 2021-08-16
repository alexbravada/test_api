from datetime import datetime

from app import db, session, Base, relationship, ForeignKey
# from flask_sqlalchemy import SQLAlchemy


#from sqlalchemy.sql.expression import func



#id записи, id приложения, текущее дата и время, информационное сообщение от приложения. (Это пример, не требование)

class All_apps(Base):
    __tablename__ = 'all_apps'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, nullable=False, unique=True)
    information = relationship("App_info")   # добавить отношение один к многим

class App_info(Base):
    __tablename__ = 'app_info'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, ForeignKey('all_apps.app_id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.String(512), nullable=False, default="STATUS:200")






