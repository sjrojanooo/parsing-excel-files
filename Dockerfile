FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y software-properties-common python3.8 python3-pip curl unzip libpq-dev build-essential libssl-dev libffi-dev python3-dev && \
    apt-get clean

WORKDIR app
COPY . /app

RUN pip3 install pandas==1.1.4

CMD ['python3', 'main.py']