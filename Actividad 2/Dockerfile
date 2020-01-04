FROM python:latest

ADD server.py ./
ADD client.py  ./
ADD Dummy.py    ./

RUN pip install --upgrade pip && \
    pip install pika

WORKDIR ./