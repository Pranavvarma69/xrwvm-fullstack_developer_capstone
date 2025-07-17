# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set backend and sentiment analysis service URLs
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


# Add code for GET requests to back end
def get_request(endpoint, **kwargs):
    params = ''
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}{endpoint}"
    if params:
        request_url += f"?{params}"
    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None


# Add code for retrieving sentiments
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected error: {err}, type: {type(err)}")
        print("Network exception occurred")
        return {"sentiment": "unknown"}


# Add code for posting review
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return {"status": 500, "message": "Post failed"}