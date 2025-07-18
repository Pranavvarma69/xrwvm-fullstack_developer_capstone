from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # User authentication routes
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration, name='register'),

    # Dealership and car-related routes
    path('get_cars', views.get_cars, name='get_cars'),
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),

    # Dealer-specific data routes
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review/<int:dealer_id>/', views.add_review, name='add_review'),
]

# Media files (only used if serving user-uploaded files in dev)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
