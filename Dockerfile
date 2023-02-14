FROM ubuntu:latest

LABEL version="1.0" \
      description="Dockerfile for self-improvement-bot" \
MAINTAINER "Djason Gadiou (djasongadiou@gmail.com)"

RUN apt-get update \
    apt-get install -y python3 python3-pip git \
    pip3 install --upgrade pip

RUN mkdir /app

RUN git clone https://github.com/Magicred-1/self-improvement-bot

WORKDIR /app/self-improvement-bot

RUN mv .env.example .env

RUN pip3 install -r requirements.txt

RUN echo "Don't forget to edit the .env file and adding your token and channel id before running the bot !"

CMD ["python3", "main.py"]
