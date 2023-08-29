from bson.json_util import loads
from bson import ObjectId
from fastapi import FastAPI
import json
import pymongo
import redis

# Redis
redis_host = "redis"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)

# MongoDB
mongo_client = pymongo.MongoClient('mongodb://mongodb:27017/')
db = mongo_client['sensors']
collections_temp = db['temp']
collections_humid = db['humid']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    

# FastAPI Implementation Code

app = FastAPI()

@app.get("/sensor/{id}")
def get_sensor_data(id: int):
    res_temp, res_humid = [], []
    for data in collections_temp.find({"sensor_id": id}, {'_id': False}).sort([("timestamp", -1)]).limit(10):
        
        res_temp.append(data)
    for data in collections_humid.find({"sensor_id": id}, {'_id': False}).sort([("timestamp", -1)]).limit(10):
        
        res_humid.append(data)

    return json.dumps({"temperature":res_temp, "humidity":res_humid}, cls = JSONEncoder)

# @app.get("/humidity/{id}")
# def get_sensor_data(id: int):
#     result = []
#     for data in collections_humid.find({"sensor_id": id}).sort([("timestamp", -1)]).limit(10):
        
#         result.append(data)

#     return json.dumps(result, cls = JSONEncoder)

# @app.get("/sesnor/id")
# def get_temp_data_from_id_range(start_id: int, end_id: int):
#     res_temp, res_humid = [], []
#     for data in collections_temp.find({"sensor_id": {"$gte": start_id, "$lte": end_id}}).sort([("sensor_id", 1)]):
#         res_temp.append(data)
#     for data in collections_humid.find({"sensor_id": {"$gte": start_id, "$lte": end_id}}).sort([("sensor_id", 1)]):
#         res_humid.append(data)
#     return json.dumps({"temperature":res_temp, "humidity":res_humid}, cls = JSONEncoder)



# @app.get("/humidity/id")
# def get_humid_data_from_id_range(start_id: int, end_id: int):
#     result = []
#     for data in collections_humid.find({"sensor_id": {"$gte": start_id, "$lte": end_id}}).sort([("sensor_id", 1)]):
#         result.append(data)
#     return json.dumps(result, cls = JSONEncoder)

@app.get("/date")
def get_sensors_data_from_date_range(start_date: str, end_date: str):
    res_temp, res_humid = [], []
    start_date = start_date + "T00:00:00"
    end_date = end_date + "T23:59:59"
    for data in collections_temp.find({"timestamp": {"$gte": start_date, "$lte": end_date}}, {'_id': False}).sort([("timestamp", 1)]):
        res_temp.append(data)
    for data in collections_humid.find({"timestamp": {"$gte": start_date, "$lte": end_date}}, {'_id': False}).sort([("timestamp", 1)]):
        res_humid.append(data)
        
   
    return json.dumps({"temperature":res_temp, "humidity":res_humid}, cls=JSONEncoder)

@app.get("/latestTenTemperature")
def get_latest_ten_readings():
    res = redis_client.lrange("temperature_readings", 0, -1)
    result = [json.loads(item.decode('utf-8')) for item in res]

    return json.dumps(result)

@app.get("/latestTenHumidity")
def get_latest_ten_readings():
    res = redis_client.lrange("humidity_readings", 0, -1)
    result = [json.loads(item.decode('utf-8')) for item in res]

    return json.dumps(result)
    

        
