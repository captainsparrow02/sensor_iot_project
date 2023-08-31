from configparser import ConfigParser
from fastapi import FastAPI
import json
import logging as log
from pymongo import MongoClient
import redis


log.basicConfig(filename='backend_api_logs/backend_api.log', filemode='w', level=log.INFO, format="[%(asctime)s] %(levelname)s %(message)s", datefmt='%d-%m-%Y %I:%M:%S %p')

config = ConfigParser()
config.read("config/project.conf")

# Redis
redis_host = config["REDIS"]["hostname"]
redis_port = int(config["REDIS"]["port"])
redis_client = redis.Redis(host=redis_host, port=redis_port)

# MongoDB
mongo_client = MongoClient(config["MONGODB"]["hostname"])
db = mongo_client[config["MONGODB"]["db"]]
collections_temp = db[config["MONGODB"]["temperature_collection"]]
collections_humid = db[config["MONGODB"]["humidity_collection"]]

# FastAPI Implementation Code


app = FastAPI()

@app.get("/sensor/{id}")
def get_sensor_data(id: int):
    log.info(f"Sensor data for ID {id} triggered.")
    cache = redis_client.get(f"latest_{id}")
    if cache:
        log.info("Cache Hit")
        result = json.loads(cache)
        
    else:
        log.info("Cache Miss")
        res_temp = list(collections_temp.find({"sensor_id": id}, {'_id': False}).sort([("timestamp", -1)]).limit(10))
        res_humid = list(collections_humid.find({"sensor_id": id}, {'_id': False}).sort([("timestamp", -1)]).limit(10))
        result = {
            "temperature" : res_temp, 
            "humidity" : res_humid
            }
        redis_client.set(f"latest_{id}", json.dumps(result))
        redis_client.expire(f"latest_{id}", 5)
    return result

@app.get("/date")
def get_sensors_data_from_date_range(start_date: str, end_date: str):
    log.info("Sensors data wrt to date triggered.")
    start_date = start_date + "T00:00:00"
    end_date = end_date + "T23:59:59"

    res_temp = list(collections_temp.find({"timestamp": {"$gte": start_date, "$lte": end_date}}, {'_id': False}).sort([("timestamp", 1)])), 
    res_humid = list(collections_humid.find({"timestamp": {"$gte": start_date, "$lte": end_date}}, {'_id': False}).sort([("timestamp", 1)]))
    result = {
        "temperature" : res_temp, 
        "humidity" : res_humid
        }
    return result


        
