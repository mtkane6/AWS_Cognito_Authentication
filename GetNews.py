import application
import string
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
import requests

def GetNewsApi(city):
    newsURL = "https://newsapi.org/v2/everything?q=" + city + "&from=2020-03-10&sortBy=popularity&apiKey=" + "3d3674b186e4412fb0f625dd7e30e8d1"
    r = requests.get(url = newsURL)
    data = r.json()
    print("from news api ", data['articles'][0]['source']['name'])