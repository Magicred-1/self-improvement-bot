FROM ubuntu:latest

MAINTAINER "Djason Gadiou (djasongadiou@gmail.com)"

RUN apt-get update \
    apt-get install -y python3 python3-pip git \
    pip3 install --upgrade pip

RUN mkdir /app

RUN git clone https://github.com/Magicred-1/self-improvement-bot

WORKDIR /app/self-improvement-bot

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
