FROM ubuntu:latest

ARG token
ARG channel_id
ARG guild_id

RUN apt-get update && apt-get install python3-pip python3.10-venv git -y && pip3 install python-dotenv

RUN mkdir /app

RUN cd /app

RUN git clone https://github.com/Magicred-1/self-improvement-bot

WORKDIR /self-improvement-bot

RUN pip3 install -r requirements.txt

RUN mv ./.env.example ./.env

RUN sed -i "s/your_token_here/$token/g" .env && sed -i "s/your_channel_id_here/$channel_id/g" .env && sed -i "s/your_guild_id/$guild_id/g" .env

RUN python3 -m venv venv

RUN . venv/bin/activate && pip3 install -r requirements.txt

# Run the bot in python env

# python -B main.py
CMD ["venv/bin/python3", "-B", "main.py"]
