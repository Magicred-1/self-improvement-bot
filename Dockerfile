FROM ubuntu:latest

RUN apt-get update && apt-get install python3-pip git -y

RUN mkdir /app

RUN cd /app

RUN git clone https://github.com/Magicred-1/self-improvement-bot

WORKDIR /self-improvement-bot

RUN mv ./.env.example ./.env

RUN pip3 install -r requirements.txt

RUN echo "Don't forget to edit the .env file and adding your token and channel id before running the bot !"

CMD ["python3", "main.py"]
