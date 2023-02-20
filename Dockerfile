FROM ubuntu:latest

ARG token = "your token"
ARG channel_id = "your channel id"

RUN apt-get update && apt-get install python3-pip git -y

RUN mkdir /app

RUN cd /app

RUN git clone https://github.com/Magicred-1/self-improvement-bot

WORKDIR /self-improvement-bot

VOLUME /logs

RUN echo "*/1 * * * * /bin/bash -c 'cp /self-improvement-bot/logs/* /logs'" >> /etc/crontab

RUN mv ./.env.example ./.env

RUN sed -i "s/your token/$token/g" .env && sed -i "s/your channel id/$channel_id/g" .env

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
