import time

from app import db, session, Base

#id записи, id приложения, текущее дата и время, информационное сообщение от приложения. (Это пример, не требование)


class appInfo(Base):
    __tablename__ = 'appInfo'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False, default=lambda: int(time.time()*1000))
    message = db.Column(db.String(512), nullable=True)





