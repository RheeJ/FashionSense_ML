FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apt-get upgrade
RUN apt-get update

RUN pip install flask

ADD . /app/
EXPOSE 5000

CMD python run.py
