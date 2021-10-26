FROM python:3.9-slim-buster

WORKDIR /app

COPY yourfile.txt yourfile.txt
RUN pip3 install -r yourfile.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD [ "python3", "bot.py"]