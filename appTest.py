from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL 
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
#from flask_mail import Mail
from cryptography.fernet import Fernet as frt

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from copy import deepcopy
from datetime import datetime
from datetime import timedelta

import os
import uuid
import random
import string
import re

import weexConstants
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.config['MYSQL_HOST'] = weexConstants.MYSQL_HOST
app.config['MYSQL_USER'] = weexConstants.MYSQL_USER
app.config['MYSQL_PASSWORD'] = weexConstants.MYSQL_PASSWORD
app.config['MYSQL_DB'] = weexConstants.MYSQL_DB
mysql = MySQL(app)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/index')
def index():
    print("index")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM m_cliente")   ###The reasoning is that execute's second parameter represents a list of the objects to be converted
    data = cur.fetchall()
    print("data", data)
    return render_template("login.html")

if __name__ == '__main__':
   app.run()