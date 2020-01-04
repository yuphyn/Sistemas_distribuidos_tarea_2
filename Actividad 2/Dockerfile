FROM python:latest

ADD server.py ./
ADD client.py  ./

RUN pip install --upgrade pip && \
    pip install pika

WORKDIR ./