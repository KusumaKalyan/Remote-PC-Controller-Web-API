from flask import Flask, send_file, request
from datetime import datetime
import pytz
from cryptography.fernet import Fernet
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'host'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db name'

mysql = MySQL(app)

@app.route('/download')
def downloadFile ():
    path = "./Credential Vault.apk"
    return send_file(path, as_attachment=True)

@app.route('/version')
def version ():
    return '3'

@app.route('/getonoffvalue')
def getOnOffValue():
    cur = mysql.connection.cursor()
    cur.execute("select value from pc_controller;")
    z = cur.fetchall()[0][0]
    mysql.connection.commit()
    cur.close()
    return str(z)

@app.route('/setonvalue', methods=['POST'])
def setOnValue():
    f = Fernet(b'unique key')
    raw_time = str(datetime.now(pytz.timezone('Asia/Kolkata'))).split(' ')[1].split(':')
    if(f.decrypt(bytes(request.args.get('code'), 'utf-8')).decode('utf-8') == raw_time[0]+raw_time[1]):
        cur = mysql.connection.cursor()
        cur.execute("update pc_controller set value=1;")
        mysql.connection.commit()
        cur.close()
        return "successfull"
    else:
        return "failed"

@app.route('/setoffvalue', methods=['POST'])
def setOffValue():
    f = Fernet(b'unique key')
    raw_time = str(datetime.now(pytz.timezone('Asia/Kolkata'))).split(' ')[1].split(':')
    if(f.decrypt(bytes(request.args.get('code'), 'utf-8')).decode('utf-8') == raw_time[0]+raw_time[1]):
        cur = mysql.connection.cursor()
        cur.execute("update pc_controller set value=0;")
        mysql.connection.commit()
        return "successfull"
    else:
        return "failed"
    cur.close()
    return "successfull"
