#!/bin/bash

exec python3 ./sub.py
sleep 2
exec python3 ./pub_temp.py
exec python3 ./pub_humid.py

