from flask import Flask
from ishaBot.main.controller import main
from ishaBot.admin.controller import admin
from ishaBot.settings import APP_STATIC

app = Flask(__name__)
app.secret_key = 'aumnamahshivaaya114'
app.config['UPLOAD_FOLDER'] = APP_STATIC

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')