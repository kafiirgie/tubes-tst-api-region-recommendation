from appflask import app
from config import mysql
import apppenyedia

from flask import jsonify, flash, request, make_response
from functools import wraps
from urllib.request import urlopen
import requests
import json


@app.route('/')
def index():
    data = {"msg":"Selamat datang di service rekomendasi tempat tinggal di Jerman"}
    return jsonify(data)


# contoh pemanggilan domain 1 buat di domain 2, tinggal variasi mainin di variable2nya
@app.route('/cobaaja')
def cobaaja():

    url = 'http://clientrofif:clientrofif@wakacipuy.my.id/region-recommendation/login'
    response = requests.get(url).json()    
    token = response['token']

    url = 'https://wakacipuy.my.id/region-recommendation/get-living-cost/Munich?token=' + str(token)
    data_response = urlopen(url)
    data_json = json.loads(data_response.read())
    
    return data_json

# @app.route('/rekomendasi/<username>/<password>/getlblbbl/<sdasa>')
# def coba(username, password):
#     url = "http://"+username+":"+password+"@wakacipuy.my.id/estimatecost/login"
#     try:
#         response = requests.get(url).json()
#         token = response["token"]
#         return token
#     except:
#         return "ERROR"
    

# @app.route('/test')
# def test():
#     url = "https://api.github.com"
#     response = urlopen(url)
#     data_json = json.loads(response.read())
#     print(data_json)
#     return data_json


if __name__ == "__main__":
    app.run()