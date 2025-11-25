import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from redis import Redis
import requests

load_dotenv()

app = FastAPI()


API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("WEATHER_API_KEY is not set in environment variables")
REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL is not set in environment variables")

redis_client = Redis.from_url(REDIS_URL)


@app.get("/weather")
def get_weather():
    cached_data = redis_client.get("WEATHER_DATA")
    if cached_data:
        cached_data = json.loads(cached_data)
        return cached_data
    
    res = requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q=Karachi")
    data = res.json()
    redis_client.setex("WEATHER_DATA", 30, json.dumps(data))
    return data