import os.path
import uuid

import sqlalchemy
from flask import Response, request, jsonify, send_file
from pydub import AudioSegment
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage

from models import Record, db, Users
from . import routes


def convert_wav_to_mp3(file: FileStorage) -> str:
    """
    Конвертер аудиозаписи из формата WAV в формат MP3. Файл сохраняется, конвертируется в новый формат, затем
    первоначальный файл удаляется
    :param file: файл, полученный из формы запроса
    :return: путь до нового сконвертированного файла
    """
    wav_filename, wav_file_extension = os.path.splitext(file.filename)
    wav_path: str = f'./media/{wav_filename}{wav_file_extension}'

    mp3_filename, mp3_file_extension = f'./media/{wav_filename}_converted', '.mp3'
    mp3_path: str = f'{mp3_filename}{mp3_file_extension}'

    if os.path.exists(wav_path):
        wav_filename: str = wav_filename + '_' + str(uuid.uuid4())[:10]
        wav_path: str = f'./media/{wav_filename}{wav_file_extension}'

    if os.path.exists(mp3_path):
        mp3_filename: str = mp3_filename + '_' + str(uuid.uuid4())[:10]
        mp3_path: str = f'{mp3_filename}{mp3_file_extension}'

    file.save(dst=wav_path)
    sound: AudioSegment = AudioSegment.from_wav(wav_path)
    os.remove(wav_path)

    sound.export(mp3_path, format='mp3')

    return mp3_path


@routes.route('/record/', methods=['GET', 'POST'])
def record_request() -> tuple[Response, Response.status_code]:
    """
    Обработчик запроса на скачивание конвертированной аудиозаписи и на конвертацию аудиофайла.

    Методы:
        POST: конвертирует аудиозапись WAV в формат MP3, сохраняет в базе данных и возвращает пользователю ссылку на
        скачивание.
        GET: отправляет запрашиваемый файл пользователю
    Аргументы:
        Нет.
    Формат входных данных:
        POST метод: форма, содержащая в себе user_id и user_token, а также файл с аудиозаписью в формате WAV
        GET метод: нет
    Формат выходных данных:
        POST метод: строка
        GET метод: нет
    :return: POST метод: ссылка на скачивание файла в формате MP3
        GET метод: нет
    """
    if request.method == 'POST':
        a: dict = request.form
        user_id: str = a.get('user_id', 'пусто')
        user_token: str = a.get('user_token', 'пусто')
        wav_file: FileStorage = request.files.get('audio', 'пусто')

        try:
            u: Users = Users.query.filter(Users.id == user_id, Users.token == user_token).all()
            if not u:
                raise ValueError
        except sqlalchemy.exc.DataError:
            return jsonify(error='Please check your credentials, need to send user_id (your ID number) and a token '
                                 'in uuid format'), 403

        except ValueError:
            return jsonify(error='Wrong authentication data. Access denied'), 403

        rec_uuid: uuid.UUID = uuid.uuid4()
        url_link_for_mp3: str = f'{request.base_url}?id={rec_uuid}&user={user_id}'
        r: Record = Record(uuid=rec_uuid, mp3=convert_wav_to_mp3(wav_file), link=url_link_for_mp3, user_id=user_id)

        db.session.add(r)
        db.session.commit()
        return jsonify(url=url_link_for_mp3), 200

    if request.method == 'GET':
        record_uuid: str = request.args.get('id')
        user_id: str = request.args.get('user')

        try:
            audiofile: Record = Record.query.filter(Record.uuid == record_uuid, Record.user_id == user_id).first()
            if not audiofile:
                raise ValueError
        except sqlalchemy.exc.DataError:
            return jsonify(error='Please check your credentials, need to send user_id (your ID number) and a token for '
                                 'audiofile in uuid format'), 403
        except ValueError:
            return jsonify(error='Wrong authentication data. Access denied'), 403

        t: str = os.path.basename(audiofile.mp3)
        return send_file(path_or_file=audiofile.mp3, as_attachment=True, download_name=t), 200
