from django.shortcuts import render

from django.http import HttpResponse
from django import forms


#def index(request):
 #   return HttpResponse("Hello, world. You're at the hotel review.")


def reviewform(request):
    return render(request, './reviewform.html')

def reviewscore(request):
    if 'positive' in request.GET:
        message = 'You searched for: %r' % request.GET['positive']
    if 'negative' in request.GET:
        message = 'You searched for: %r' % request.GET['negative']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)