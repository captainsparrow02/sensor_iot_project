import random
from datetime import datetime

def generate_sensor_reading():
    '''Function to generate random sensor reading.'''
    return round(random.uniform(0, 100), 2)

def get_sensor_timestamp():
    '''Function to generate ISO8601 formatted datetime.'''
    return datetime.now().isoformat()

def get_sensor_payload():
    '''Function to generate desired sensor payload.'''
    return {  
        "value": generate_sensor_reading(), 
        "timestamp": get_sensor_timestamp() 
        }