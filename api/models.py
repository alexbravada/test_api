import time

from app import db, session, Base, relationship, ForeignKey
# from flask_sqlalchemy import SQLAlchemy


#from sqlalchemy.sql.expression import func

#id записи, id приложения, текущее дата и время, информационное сообщение от приложения. (Это пример, не требование)

# class All_apps(Base):
#     __tablename__ = 'all_apps'
#     id = db.Column(db.Integer, primary_key=True)
#     app_id = db.Column(db.Integer, nullable=False, unique=True)
#     information = relationship("App_info")   # добавить отношение один к многим


class appInfo(Base):
    __tablename__ = 'appInfo'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: int(time.time()*1000))
    message = db.Column(db.String(512), nullable=True)





