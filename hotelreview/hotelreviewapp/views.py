from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from multi_rake import Rake
from django.http import HttpResponse

import pandas as pd
import copy


class HomeView(TemplateView):
    template_name = 'reviewform.html'


#def index(request):
#     rake = Rake()
#     temp = rake.apply('No real complaints the hotel was great great location surroundings rooms amenities and service Two recommendations however firstly the staff upon check in are very confusing regarding deposit payment')
#     return HttpResponse(temp)

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

    if len(positiveResult) > 0:
        for i in range(0, len(positiveResult)) :
            positiveScore = positiveScore + positiveResult[i][1]
    
    if len(negativeResult) > 0:
        for i in range(0, len(negativeResult)):
            negativeScore = negativeScore + negativeResult[i][1]
    
    totalScore = positiveScore - negativeScore

    expectedReviewScore = 0.40609431*totalScore + 8.31906161
    if expectedReviewScore > 10.0:
        expectedReviewScore = 10.0
    elif expectedReviewScore < 0.0:
        expectedReviewScore = 0.0
    else:
        expectedReviewScore = round(expectedReviewScore,2)

    reviewsRawData = pd.read_csv("../data/Hotel_Reviews.csv", usecols=['Positive_Review', 'Negative_Review', 'Reviewer_Score'])
    resultTuple = reviewsRawData[reviewsRawData["Positive_Review"].str.contains(positive)]
    
    resultVal = ''
    actual = ' | This review is not from database'
    analysis = ''
    if len(resultTuple["Reviewer_Score"].values) > 0:
        resultVal = resultTuple["Reviewer_Score"].values
        if resultVal[0] > 0.0:
            tempVal = copy.deepcopy(resultVal[0])
            actual = ' | Actual '
            actual = actual + copy.deepcopy(str(resultVal[0]))
            actual = actual + ' | Accuracy: '
            if expectedReviewScore > resultVal[0]:
                analysis = (expectedReviewScore-resultVal[0])
            else:
                analysis = (resultVal[0]-expectedReviewScore)
            analysis = str(round(100-(analysis/tempVal*100),2))
            analysis = analysis + '%'

    result = "User Rating: Expected " + str(expectedReviewScore) + actual + analysis
    return HttpResponse(result)
