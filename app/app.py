from flask import Flask
from loader import DEBUG
from routes import routes
from models import db


def create_app(config: str):
    """
    Создает экземпляр класса Flask. Подключает нужные конфигурации, маршруты и привязывается объект базы данных
    SQLAlchemy.
    :param config: Передается ссылка на нужный класс конфигурации из файла config.py
    :return: экземпляр класса Flask с нужными настройками для дальнейшей работы
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    flask_app.register_blueprint(routes)
    db.init_app(flask_app)
    return flask_app


if __name__ == '__main__':
    app = create_app('config.MainConfig')
    with app.app_context():
        db.create_all()
    app.run(debug=DEBUG, host='0.0.0.0')
