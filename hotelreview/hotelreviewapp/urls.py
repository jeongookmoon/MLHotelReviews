from django.contrib import admin
from django.urls import path
from hotelreviewapp.views import HomeView # Import the new view we created
from hotelreviewapp.views import HotelView
from . import views

urlpatterns =[
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()), # Map the HomeView to the index route
    path('hotel/', HotelView.as_view()), # Map the HomeView to the index route
    #path('index/', views.index, name='index'),
    path('reviewscore/', views.reviewscore, name='reviewscore'),
    path('similarhotel/', views.similarhotel, name='similarhotel'),
]
