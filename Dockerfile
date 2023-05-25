FROM python

RUN apt-get update && apt-get install -y ffmpeg

RUN mkdir /main_app

COPY requirements.txt /main_app/

COPY app /main_app/

RUN python -m pip install -r /main_app/requirements.txt

WORKDIR /main_app

ENTRYPOINT ["python", "app.py"]