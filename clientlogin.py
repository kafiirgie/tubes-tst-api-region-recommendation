import pymysql
from flask import jsonify, request, make_response
from functools import wraps
import jwt
import datetime

from appflask import app
from config import mysql

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is Missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except:
            return jsonify({'message': 'Token is Invalid'}), 403

        return f(*args, **kwargs)
    return decorated
    

@app.route('/login')
def login():
    auth = request.authorization
    if auth and isLoginValid(auth.username, auth.password) == True:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.encode().decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def isLoginValid(username, password):
    status = False
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM account_client where username = '" + username + "' and password = '" + password + "'")
    if cursor.rowcount > 0:
        return True
    cursor.close()
    conn.close()
    return status