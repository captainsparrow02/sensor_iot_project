FROM python:3.10-slim-buster

WORKDIR /sensor-publish

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "publish.py" ]
