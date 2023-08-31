FROM python:3.10-slim-buster

WORKDIR /backend_api

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "uvicorn" , "app:app", "--host=0.0.0.0", "--port=80", "--reload"]