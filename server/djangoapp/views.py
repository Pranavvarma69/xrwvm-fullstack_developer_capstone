# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            return JsonResponse({"status": "Authenticated", "userName": username})
        else:
            return JsonResponse({"status": "Unauthorized"}, status=401)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug(f"{username} is a new user")

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name,
                                        last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})

# Update the `get_dealerships` view
@csrf_exempt
def get_dealerships(request, state='All'):
    if state == 'All':
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Get dealer reviews and analyze sentiment
@csrf_exempt
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Get dealer details
@csrf_exempt
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Add a review for a dealer
@csrf_exempt
@csrf_exempt
def add_review(request,dealer_id):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        print("REVIEW DATA RECEIVED:", data)

        try:
            response = post_review(data)
            print("POST REVIEW RESPONSE:", response)

            if response.get("status") == 200:
                return JsonResponse({"status": 200, "message": "Review added successfully"})
            else:
                return JsonResponse({"status": 500, "message": "Backend failed to add review"})

        except Exception as e:
            print("Error posting review:", e)
            return JsonResponse({"status": 500, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

# Get list of car models with car make names
@csrf_exempt
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
    return JsonResponse({"CarModels": cars})