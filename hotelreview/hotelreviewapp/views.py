from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from multi_rake import Rake
from django.http import HttpResponse

import pandas as pd
import copy

import numpy as np
from textblob import TextBlob
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity


class HomeView(TemplateView):
    template_name = 'reviewform.html'
    

class HotelView(TemplateView):
    template_name = 'similarhotel.html'


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

    expectedReviewScore = 0.18*totalScore + 8.31
    
    # limit expected score range from 0 to 10
    if expectedReviewScore > 10.0:
        expectedReviewScore = 10.0
    elif expectedReviewScore < 0.0:
        expectedReviewScore = 0.0
    else:
        expectedReviewScore = round(expectedReviewScore,2)

    # import actual data for actual user score
    reviewsRawData = pd.read_csv("../data/Hotel_Reviews.csv", usecols=['Positive_Review', 'Negative_Review', 'Reviewer_Score'])
    resultTuple = reviewsRawData[reviewsRawData["Positive_Review"].str.contains(positive)]
    
    resultVal = ''
    actual = ' | This review is not from database'
    analysis = ''

    # handle if the review doesn't exist on database
    if len(resultTuple["Reviewer_Score"].values) > 0:
        resultVal = resultTuple["Reviewer_Score"].values
        if resultVal[0] > 0.0:
            tempVal = copy.deepcopy(resultVal[0])
            actual = ' | Actual '
            actual = actual + copy.deepcopy(str(resultVal[0]))
            actual = actual + ' | Accuracy: '
            if expectedReviewScore > resultVal[0]:
                analysis = (expectedReviewScore-resultVal[0])
                analysis = str(round(100-(analysis/expectedReviewScore*100),2))
            else:
                analysis = (resultVal[0]-expectedReviewScore)
                analysis = str(round(100-(analysis/tempVal*100),2))
            analysis = analysis + '%'

    result = "User Rating: Predicted " + str(expectedReviewScore) + actual + analysis
    return HttpResponse(result)


def similarhotel(request):
    hotelname = request.POST['hotelname']
    
    # read in file
    train = pd.read_csv("./Hotel_Reviews.csv",usecols=['Hotel_Name','Positive_Review','Average_Score'])
    train = train.iloc[0:5000,]

    # group dataset by hotel name
    grouped_df = train.groupby('Hotel_Name')
    grouped_df_sum = train.groupby('Hotel_Name').apply(lambda x: x.sum())

    # create hashmap by having comment keyword attributes as the keys
    keywordArray = {}
    attributes = {}
    attributes['staff'] = 0
    attributes['room'] = 1
    attributes['location'] = 2
    attributes['breakfast'] = 3
    attributes['bed']=4
    attributes['service']=5
    attributes['station'] = 6
    attributes['bathroom'] = 7
    attributes['area'] = 8
    attributes['bar'] = 9
    attributes['view']= 10
    attributes['metro'] = 11
    attributes['tube'] = 12
    attributes['food'] = 13

    # assign each key with average revew score arrays
    rowSize = []
    for k in grouped_df.size():
        rowSize.append(k)

    scores = []
    i = 0
    for k in grouped_df_sum['Average_Score']:
        score = int(round(k/rowSize[i],0))
        scores.append(score)
        i = i + 1

    j = 0
    keyArr = grouped_df.groups.keys()
    for k in keyArr :
        keywordArray[k] = copy.deepcopy([scores[j], scores[j], scores[j], scores[j], scores[j], scores[j], scores[j], scores[j], scores[j], scores[j], scores[j],scores[j], scores[j], scores[j]])
        j = j + 1

    # analize each review and find the most common keywords
    reviewTags = []
    for i in range(0, len(grouped_df_sum)) :
        eachReview = TextBlob(grouped_df_sum['Positive_Review'][i])
        reviewTags.append([])
        for j in range(0, len(eachReview.tags)) :
            if eachReview.tags[j][1] == 'NN' :
                reviewTags[i].append(eachReview.tags[j][0])

    # add the frequency of each keyword to the hotel's score array
    hotelnames = []
    for k in keywordArray.keys() :
        hotelnames.append(k)

    for i in range(0,len(reviewTags)):
        counter = Counter(reviewTags[i])
        mostOccurTag = counter.most_common(10) 
        for j in range (0,len(mostOccurTag)-1):
            tempNum2 = str(mostOccurTag[j][1])
            tempNum3 = str(attributes.get(mostOccurTag[j][0]))
            for k in range(0, len(mostOccurTag)):
                if mostOccurTag[j][0] in attributes :
                    keywordArray[hotelnames[i]][int(tempNum3)] = int(tempNum2)

    simScores = []
    for k in keywordArray.keys():
        if k != hotelname:
            simScores.append(cosine_similarity([keywordArray.get(hotelname)], [keywordArray.get(k)])[0][0])
    npsimScores = np.array(simScores)
    indexes = npsimScores.argsort()[-3:][::-1]
    nphotelnames = np.array(hotelnames)

    result = []
    for k in nphotelnames[indexes]:
        result.append(k)
        result.append("          ")
    return HttpResponse(result)