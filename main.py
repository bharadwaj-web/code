from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flask import jsonify
import hashlib
import jwt
import datetime
import time
import socket

from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'CLINICALFIRST_01'

mysql = MySQL(app)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

            USER_MAIL_ID = request.json['USER_MAIL_ID']
            USER_PASSWORD = request.json['USER_PASSWORD']
            j = hashlib.md5(USER_PASSWORD.encode())
            print(j.hexdigest())
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM USER_SIGNUP WHERE USER_MAIL_ID = % s AND USER_PASSWORD = % s',
                        (USER_MAIL_ID, j.hexdigest()))
            account = cur.fetchone()
            if account:
                print(account)
                token = jwt.encode({'USER_MAIL_ID': USER_MAIL_ID, 'USER_PASSWORD': USER_PASSWORD,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                   app.config['SECRET_KEY'])
                #return jsonify({'token': token.decode('UTF-8')})
                return jsonify({'token': token})
            else:
                return jsonify({"unable to login"})


@app.route('/signup', methods=['POST'])
def USER_SIGNUP():
    if request.method == 'POST':
        try:
            USER_SIGNUP_ID = request.json['USER_SIGNUP_ID']
            USER_ID = request.json['USER_ID']
            USER_NAME = request.json['USER_NAME']
            USER_MAIL_ID = request.json['USER_MAIL_ID']
            USER_PHONE_NUMBER = request.json['USER_PHONE_NUMBER']
            USER_PASSWORD = request.json['USER_PASSWORD']
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            #IPAddr = socket.gethostbyname(hostname)
            #USER_IP = request.json['USER_IP']
            # USER_DATE_CREATED = request.json['USER_DATE_CREATED']

            j = hashlib.md5(USER_PASSWORD.encode())
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO USER_SIGNUP(USER_SIGNUP_ID,USER_ID,USER_NAME,USER_MAIL_ID,USER_PHONE_NUMBER,USER_PASSWORD, USER_IP, HOST_NAME ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (USER_SIGNUP_ID, USER_ID, USER_NAME, USER_MAIL_ID, USER_PHONE_NUMBER, j.hexdigest(), IPAddr, hostname)) #USER_IP
            mysql.connection.commit()
            cur.close()
            return jsonify('signup successful')
        except:
            return jsonify('user already exists try login or signup with different credentials')


if __name__ == '__main__':
    app.run()

