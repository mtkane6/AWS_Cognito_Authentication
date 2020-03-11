import application
import string
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
import requests

def GetNewsApi(city):
    newsURL = "https://newsapi.org/v2/everything?q=" + city + "&from=2020-03-10&sortBy=popularity&apiKey=" + "3d3674b186e4412fb0f625dd7e30e8d1"
    r = requests.get(url = newsURL)
    returnList = ''
    if r.status_code < 400:
        data = r.json()
        if len(data['articles']) > 0:
            article = data['articles'][0]
            returnList = ["Author: " + article['author'], "Source: " + article['source']['name'], "Title: " + article['title'], article['content']]
    return returnList
    