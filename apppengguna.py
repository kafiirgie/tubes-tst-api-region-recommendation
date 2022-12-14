import pymysql
from flask import jsonify

from appflask import app
from config import mysql
from clientlogin import token_required
import apppenyedia

@app.route('/get-recomm-by-job')
def getRegionRecommbyJob():
    return "hai"

@app.route('/get-recomm-by-living-cost')
def getRegionRecommbyJob():
    return "hai"

@app.route('/get-recomm-by-all')
def getRegionRecommbyJob():
    return "hai"