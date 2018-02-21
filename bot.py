import requests
import os
from nasa import apod
import urllib.request
import tweepy
import random
import time
from secrets import *

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    #return strTimeProp(start, end, '%m/%d/%Y', prop)
    return strTimeProp(start, end, '%Y-%m-%d', prop)

os.environ['NASA_API_KEY'] = 'sUMrj7lWaYKyQA5w0Zs0PPz9YhBtJ6Pt5cSHVCzK'

date = randomDate('1996-1-1', time.strftime('%Y-%m-%d'), random.random())

picture = apod.apod(date)

tweet = '#nasa '+picture.title+' -Date of photo: '+date

if(len(tweet) < 276):
    ocL = len(picture.explanation)
    tL = len(tweet)
    tot = ( ocL if ocL+tL <= 276 else 275-tL)
    tweet += ' '+picture.explanation[:tot] + "..."

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
api = tweepy.API(auth)

filename = 'temp.jpg'
request = requests.get(picture.url, stream=True)
if request.status_code == 200:
    with open(filename, 'wb') as image:
        for chunk in request:
            image.write(chunk)
    api.update_with_media(filename, tweet)
    os.remove(filename)
else:
    print("Unable to download image")
    api.update_status(tweet)
