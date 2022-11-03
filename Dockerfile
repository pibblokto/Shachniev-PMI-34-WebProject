FROM python:3.8-slim

RUN useradd webapp

WORKDIR /home/webapp

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN venv/bin/pip install -r requirements.txt
RUN apt-get update -y
RUN apt-get install --no-install-recommends -qy gcc 
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY webapp.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP webapp.py

RUN chown -R webapp:webapp ./
USER webapp

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
