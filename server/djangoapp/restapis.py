import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Set backend and sentiment analysis service URLs
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


# GET request to back end with optional parameters
def get_request(endpoint, **kwargs):
    params = ''
    if kwargs:
        param_list = [f"{key}={value}" for key, value in kwargs.items()]
        params = "&".join(param_list)

    request_url = f"{backend_url}{endpoint}"
    if params:
        request_url += f"?{params}"

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None


# Retrieve sentiment for a given review text
def analyze_review_sentiments(text):
    encoded_text = quote_plus(text)
    request_url = f"{sentiment_analyzer_url}analyze/{encoded_text}"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Unexpected error: {err}, type: {type(err)}")
        return {"sentiment": "unknown"}


# POST review to back end
def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"status": 500, "message": "Post failed"}
