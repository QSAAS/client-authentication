# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY wait-for-it.sh /code/wait-for-it.sh

RUN chmod +x /code/wait-for-it.sh

COPY . /code/

