from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class Users(db.Model):
    """
    Модель данных для таблицы User(Пользователь) в базе данных
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    token = db.Column(UUID(as_uuid=True))


class Record(db.Model):
    """
    Модель данных для таблицы Record(Аудиозапись) в базе данных
    """
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True))
    mp3 = db.Column(db.Text)
    link = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('Users', backref='Users.id', primaryjoin='Users.id==Record.user_id')
