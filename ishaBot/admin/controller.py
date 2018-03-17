from flask import Blueprint ,render_template ,request ,Response,session
from ishaBot.settings import APP_STATIC
import os
import csv
import time


admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return render_template("login.html")


@admin.route('/login',methods=['POST'])
def login():
    uname = request.form['uname']
    pwd = request.form['pwd']


    if(uname=='admin' and pwd=='isha114') :
        session['authenticated'] = True
        #Read existing file contents , store it in a list and return to view
        tweetList=[]

        try:
            with open(os.path.join(APP_STATIC, 'tweets.csv'), "r") as file:
                reader = csv.reader(file)
                for line in reader:
                    tweetList.append(line[0])
        except:
            print('No file present')

        return render_template("editFile.html",tweetList=tweetList)


    else:
        return render_template("login.html",error=True)

@admin.route('/uploadFile',methods=['POST'])
def uploadFile():

    file = request.files['file']        
    myfile = file.read()
    try:
        myFile = (myfile).decode('utf-8').split('\n')
        with open(os.path.join(APP_STATIC, 'tweets.csv'), "w+") as file:
            f = csv.writer(file)
            for line in myFile:
                f.writerow([line])
    except Exception as e:
        print('Exception occured while writing tweets to file')
        print(e)
        return render_template("editFile.html",error=True)


    return render_template("editFile.html",tweetList=myFile)


@admin.route('/logout')
def logout():
   # remove the username from the session if it is there
    session.pop('authenticated', None)
    return render_template("login.html")

