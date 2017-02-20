FROM python:2.7
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get upgrade
RUN apt-get update

ADD . /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ./start.sh
