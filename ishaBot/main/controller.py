from flask import Blueprint ,render_template ,request ,Response
import twitter
import json
import os
import csv
import time
from ishaBot.settings import APP_STATIC


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("index.html")


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
            headers={'Content-Disposition':'attachment;filename=zones.geojson'})

    if request.form['submit'] == 'runBot':

        consumer_key=request.form['consumer_key']
        consumer_secret=request.form['consumer_secret']
        access_token_key=request.form['access_token_key']
        access_token_secret=request.form['access_token_secret']

    elif request.form['submit'] == 'parseKey':
        file = request.files['file']        
        myfile = file.read()
        file = json.loads(myfile)
        consumer_key=file['consumer_key']
        consumer_secret=file['consumer_secret']
        access_token_key=file['access_token_key']
        access_token_secret=file['access_token_secret']

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
    with open(os.path.join(APP_STATIC, 'tweets.csv'), "r") as file:
        reader = csv.reader(file)
        for line in reader:
            if len(line)==0:
                continue
            temp_list = []
            temp_list.append(line[0])
            tweet_id = line[0].split('/')[-1]
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