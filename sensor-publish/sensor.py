import random
from datetime import datetime

def generate_sensor_id():
    '''Function to generate a random Sensor ID between and including 101 to 200.'''
    return random.randint(101,200)

def generate_sensor_reading():
    '''Function to generate random sensor reading.'''
    return round(random.uniform(0, 100), 2)

def get_sensor_timestamp():
    '''Function to generate ISO8601 formatted datetime.'''
    return datetime.now().isoformat()

def get_sensor_payload():
    '''Function to generate desired sensor payload.'''
    return { 
        "sensor_id": generate_sensor_id(), 
        "value": generate_sensor_reading(), 
        "timestamp": get_sensor_timestamp() 
        }