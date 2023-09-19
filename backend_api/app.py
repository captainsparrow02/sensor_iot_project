from configparser import ConfigParser
from fastapi import FastAPI
import json
import logging as log
from pymongo import MongoClient
import redis

# Initializing Logging.
log.basicConfig(filename='backend_api_logs/backend_api.log', filemode='w', level=log.INFO, format="[%(asctime)s] %(levelname)s %(message)s", datefmt='%d-%m-%Y %I:%M:%S %p')

# Initializing Configuration Parser to read config file.
config = ConfigParser()
config.read("config/project.conf")

# Setting up Redis.
redis_host = config["REDIS"]["hostname"]
redis_port = int(config["REDIS"]["port"])
redis_client = redis.Redis(host=redis_host, port=redis_port)

# Setting up MongoDB.
mongo_client = MongoClient(config["MONGODB"]["hostname"])
db = mongo_client[config["MONGODB"]["db"]]
collections_temp = db[config["MONGODB"]["temperature_collection"]]
collections_humid = db[config["MONGODB"]["humidity_collection"]]

# Initializing FastAPI app instance.
app = FastAPI()

@app.get("/sensor/{id}")
async def get_sensor_data(id: int):
    '''This fucntion handles requestes coming for sensor readings with a specific sensor ID.'''

    log.info(f"Sensor data for ID {id} triggered.")
    
    # Attempting to fetch data from Redis cache.
    cache = redis_client.get(f"latest_{id}")

    if cache:
        log.info("Cache Hit")
        result = json.loads(cache)
    else:
        log.info("Cache Miss")

        # Fetching Data from MongoDB, sorting in descending order of timestamp and keeping only the first 10 readings.
        res_temp = list(collections_temp.find({"sensor_id": id}, {'_id': False}).sort([("timestamp", -1)]).limit(10))
        res_humid = list(collections_humid.find({"sensor_id": id}, {'_id': False}).sort([("timestamp", -1)]).limit(10))
        
        # Response payload setup.
        result = {
            "temperature" : res_temp, 
            "humidity" : res_humid
            }
        
        # Setting the latest fetched data in Redis cache.
        redis_client.set(f"latest_{id}", json.dumps(result))

        # Setting data expiry limit to 10 seconds.
        # Data is removed from Redis cache after 10 seconds.
        redis_client.expire(f"latest_{id}", 10)

    return result

@app.get("/date")
async def get_sensors_data_from_date_range(start_date: str, end_date: str):
    '''This function handles request for all sensors reading captured withing a date range.'''

    log.info("Sensors data wrt to date triggered.")

    # Timestamp in DB includes both date and time.
    # Query params only have start and end date, hence appenidng time.
    start_date = start_date + "T00:00:00"
    end_date = end_date + "T23:59:59"
    
    # Fetching data from MongoDB in sorted order.
    res_temp = list(collections_temp.find({"timestamp": {"$gte": start_date, "$lte": end_date}}, {'_id': False}).sort([("timestamp", 1)])), 
    res_humid = list(collections_humid.find({"timestamp": {"$gte": start_date, "$lte": end_date}}, {'_id': False}).sort([("timestamp", 1)]))
       
    # Response payload setup.
    result = {
        "temperature" : res_temp, 
        "humidity" : res_humid
        }
    return result


        
