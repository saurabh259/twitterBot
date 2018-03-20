from flask import Blueprint ,render_template ,request ,Response
import twitter
import json
import os
import csv
import time
import datetime
from dateutil import tz
from ishaBot.settings import APP_STATIC
from ishaBot.database.db import *


main = Blueprint('main', __name__)


@main.route('/')
def index():
    localTime = getUpdationTime()
    localTime = datetime.datetime.strptime(localTime,'%d-%m-%Y %H:%M')
    istTime = localTime.astimezone(tz.gettz('Asia/Kolkata'))
    istTime = istTime.strftime('%d-%m-%Y %H:%M')
    return render_template("index.html",last_modified=istTime)


@main.route('runbot',methods=['POST'])
def runBot():
    consumer_key=''
    consumer_secret=''
    access_token_key=''
    access_token_secret=''

    if request.form['submit'] == 'downloadKey':
        key={}
        key['consumer_key']=request.form['consumer_key']
        key['consumer_secret']=request.form['consumer_secret']
        key['access_token_key']=request.form['access_token_key']
        key['access_token_secret']=request.form['access_token_secret']
        content = json.dumps(key)

        return Response(content, 
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=ishaTwitterBot.json'})

    if request.form['submit'] == 'runBot':

        consumer_key=request.form['consumer_key']
        consumer_secret=request.form['consumer_secret']
        access_token_key=request.form['access_token_key']
        access_token_secret=request.form['access_token_secret']

    elif request.form['submit'] == 'parseKey':
        # bad file upload
        try:
            file = request.files['file']        
            myfile = file.read()
            file = json.loads(myfile)
            consumer_key=file['consumer_key']
            consumer_secret=file['consumer_secret']
            access_token_key=file['access_token_key']
            access_token_secret=file['access_token_secret']
        except Exception as e:
            print('Bad file uploaded')
            print(e)
            return render_template("index.html",error=True)


    try:
        api = twitter.Api(consumer_key=consumer_key,
          consumer_secret=consumer_secret,
          access_token_key=access_token_key,
          access_token_secret=access_token_secret)
        (api.VerifyCredentials())

    except Exception as e:
        print('[_/\_ Namaskaram] Error authenticating twitter , please check credentials')
        print(e)
        return render_template("index.html",error=True)
 
    result = {}
    user = api.VerifyCredentials()
    name = user.name
    screenName = user.screen_name

    count=1
    for tweet in loadTweets():
        print(tweet[0])
        if len(tweet)==0:
            continue
        temp_list = []
        temp_list.append(tweet[0])
        tweet_id = tweet[0].split('/')[-1]
        print('BOT extracted tweet id as {} from file'.format(tweet_id))
        try:
            (api.PostRetweet(tweet_id))
            (api.CreateFavorite(status_id=int(tweet_id)))
            temp_list.append('Success')
            temp_list.append('green')

            print('[_/\_ Namaskaram] , Retweet & Like completed!')

        except Exception as e:
            print('[_/\_ Namaskaram] Error retweeting/liking the tweet')
            print((e.message[0]['message']))
            temp_list.append(e.message[0]['message'])
            temp_list.append('red')

        result[count]=temp_list
        count+=1

    # print('[_/\_ Namaskaram] Process succesfully completed . Thanks for taking out your time')
    return render_template("result.html",data=result,name=name,screenName=screenName)


