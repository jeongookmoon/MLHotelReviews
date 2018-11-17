from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from multi_rake import Rake
from django.http import HttpResponse

class HomeView(TemplateView):
    template_name = 'reviewform.html'



def index(request):
    rake = Rake()
    temp = rake.apply('No real complaints the hotel was great great location surroundings rooms amenities and service Two recommendations however firstly the staff upon check in are very confusing regarding deposit payment')

    return HttpResponse(temp)

# def reviewform(request):
#     template = loader.get_template("hotelreview/reviewform.html")
#     return HttpResponse(template.render())

def reviewscore(request):
    rake = Rake()
    positive = request.POST['positive']
    negative = request.POST['negative']

    if len(positive) == 0 :
        positive =  "No positive"
    if len(negative) == 0:
        #message = 'You searched for: %r' % request.GET['negative']
        negative = "No negative"
    
    positiveResult = rake.apply(positive)
    negativeResult = rake.apply(negative)

    positiveScore = 0
    negativeScore = 0

    for i in range(0, len(positiveResult)) :
        positiveScore = positiveScore + positiveResult[i][1]
    
    for i in range(0, len(negativeResult)):
        negativeScore = negativeScore + negativeResult[i][1]
    
    totalScore = positiveScore + negativeScore

    return HttpResponse(totalScore)
