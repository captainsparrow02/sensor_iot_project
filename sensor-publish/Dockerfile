FROM python:3.10-slim-buster

WORKDIR /sensor-publish

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.sh

CMD [ "bash", "run.sh" ]
