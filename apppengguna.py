import pymysql
from flask import jsonify
from urllib.request import urlopen
import requests
import json

from appflask import app
from config import mysql
from clientlogin import token_required
# import apppenyedia

def get_city_in_germany():
    LIST_CITY_IN_GERMANY = []
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT city FROM `living_cost` WHERE city LIKE '%, Germany'")
        read_row = cursor.fetchall()
        
        for row in read_row:
            city = row['city'].split(',')[0]
            LIST_CITY_IN_GERMANY.append(city)
        return LIST_CITY_IN_GERMANY

    except Exception as e:
        print(e)
        return []

    finally:
        cursor.close()
        conn.close()

def get_token_by_login():
    # Login to API estimatecost (login ke api penyedia rekan)
    url = 'http://clientkafi:clientkafi@wakacipuy.my.id/estimatecost/login'
    response = requests.get(url)
    response = (response.json())    
    token = response['token']
    return token

@app.route('/get-recomm-by-job/')
def get_reccom_by_job_index():
    response = {"usage1" : "/<job_role>", "usage2" : "/<job_role_first>/<job_role_last>"}
    return jsonify(response)

@app.route('/get-recomm-by-job/<rolefirst>')
def get_reccom_by_job_using_single_role(rolefirst):
    # GET REGION DATA
    list_city = get_city_in_germany()
    list_view_data = []
    for city in list_city:
        # Rearrange city string
        city = city.split()[0]
        # Get Average Salary
        token = get_token_by_login()
        url = 'https://wakacipuy.my.id/estimatecost/getsalaries/'+ city +'/'+ rolefirst + '/f/f/f?token=' + str(token)
        dataresponse = urlopen(url)
        dataresponse = json.loads(dataresponse.read())['avg_salary_usd']
        if dataresponse:
            salary = round(float(dataresponse), 2)
        else:
            salary = 0
        # Get Average Vacation Days
        token = get_token_by_login()
        url = 'https://wakacipuy.my.id/estimatecost/getvacationdays/'+ city +'/'+ rolefirst + '/f/f/f?token=' + str(token)
        dataresponse = urlopen(url)
        dataresponse = json.loads(dataresponse.read())['avg_vacation_days']
        if dataresponse:
            vacation_days = int(dataresponse)
        else:
            vacation_days = 0
        # Create Data Dictionary
        data = {"job" : rolefirst, "city" : city, "salary" : salary, "vacation_days" : vacation_days}
        # Append
        list_view_data.append(data)
    data = {"job" : rolefirst, "city" : "MALANGBOZ", "salary" : 107856.0, "vacation_days" : 1}
    list_view_data.append(data)
    list_view_data = sorted(list_view_data, key=lambda i: (i["salary"], i["vacation_days"]), reverse=True)

    # GET REGION RECOMMENDATION
    list_region_recomm = []
    for i in range(5):
        list_region_recomm.append(list_view_data[i])
        
    return jsonify(list_region_recomm)

@app.route('/get-recomm-by-job/<rolefirst>/<rolelast>')
def get_reccom_by_job_using_full_role(rolefirst, rolelast):
    # GET REGION DATA
    list_city = get_city_in_germany()
    list_view_data = []
    for city in list_city:
        # Rearrange city string
        city = city.split()[0]
        # Get Average Salary
        token = get_token_by_login()
        url = 'https://wakacipuy.my.id/estimatecost/getsalaries/'+ city +'/'+ rolefirst + '/' + rolelast + '/f/f?token=' + str(token)
        dataresponse = urlopen(url)
        dataresponse = json.loads(dataresponse.read())['avg_salary_usd']
        if dataresponse:
            salary = round(float(dataresponse), 2)
        else:
            salary = 0
        # Get Average Vacation Days
        token = get_token_by_login()
        url = 'https://wakacipuy.my.id/estimatecost/getvacationdays/'+ city +'/'+ rolefirst + '/' + rolelast + '/f/f?token=' + str(token)
        dataresponse = urlopen(url)
        dataresponse = json.loads(dataresponse.read())['avg_vacation_days']
        if dataresponse:
            vacation_days = int(dataresponse)
        else:
            vacation_days = 0
        # Create Data Dictionary
        job = rolefirst + " " + rolelast
        data = {"job" : job, "city" : city, "salary" : salary, "vacation_days" : vacation_days}
        # Append
        list_view_data.append(data)
    data = {"job" : job, "city" : "MALANGBOZ", "salary" : 107856.0, "vacation_days" : 1}
    list_view_data.append(data)
    list_view_data = sorted(list_view_data, key=lambda i: (i["salary"], i["vacation_days"]), reverse=True)

    # GET REGION RECOMMENDATION
    list_region_recomm = []
    for i in range(5):
        list_region_recomm.append(list_view_data[i])
        
    return jsonify(list_region_recomm)

@app.route('/get-recomm-by-living-cost/<categorylivingcost>')
def getRegionRecommbyLivingCost(categorylivingcost):
    list_city = get_city_in_germany()
    return "hai"

@app.route('/get-recomm-by-all')
def getRegionRecommbyAll():
    list_city = get_city_in_germany()
    return "hai"