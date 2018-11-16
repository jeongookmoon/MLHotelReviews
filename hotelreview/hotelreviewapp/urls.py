from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.reviewform, name='reviewform'),
    path('', views.reviewscore, name='reviewscore'),
]