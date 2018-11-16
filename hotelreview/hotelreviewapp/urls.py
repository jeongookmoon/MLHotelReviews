from django.contrib import admin
from django.urls import path
from hotelreviewapp.views import HomeView # Import the new view we created

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()), # Map the HomeView to the index route
]