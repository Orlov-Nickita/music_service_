import uuid
from flask import Response, request, jsonify
from models import Users, db
from . import routes


@routes.route('/user/add/', methods=['POST'])
def user_request() -> tuple[Response, Response.status_code]:
    """
    Обработчик запроса на добавление нового пользователя в базу данных.

    Методы:
        POST: добавляет нового пользователя в базу данных.
    Аргументы:
        Нет.
    Формат входных данных:
        JSON-объект вида {"name": "string"}, где "string" - имя нового пользователя.
    Формат выходных данных:
        JSON-объект вида {"credentials": {"id": int, "token": str}}, где:
            - "id" - уникальный идентификатор нового пользователя;
            - "token" - уникальный токен, сгенерированный для нового пользователя.
    :return: Возвращает кортеж из двух элементов:
        - JSON-объект с данными нового пользователя и кодом ответа 200 в случае успешного выполнения запроса;
        - код ошибки и сообщение об ошибке в случае ошибки.
        Если входные данные некорректны или отсутствуют, возвращает код ошибки 400 и сообщение об ошибке.
    """
    if request.method == 'POST':
        a: dict = request.get_json()
        name: str = a.get('name', 'пусто')
        if name == 'пусто' or not isinstance(name, str):
            return jsonify(name='Please, send your name'), 400

        u = Users(name=name, token=uuid.uuid4())
        db.session.add(u)
        db.session.commit()
        data = {
            'id': u.id,
            'token': u.token,
        }
        return jsonify(credentials=data), 200
