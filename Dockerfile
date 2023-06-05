# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
#RUN apt-get update
#RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt