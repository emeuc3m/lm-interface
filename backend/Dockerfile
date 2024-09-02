FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install python3-pip -y

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./run.py ./run.py
