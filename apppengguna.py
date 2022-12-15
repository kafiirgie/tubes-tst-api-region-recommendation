import pymysql
from flask import jsonify
from urllib.request import urlopen
import requests
import json

from appflask import app
from config import mysql
from clientlogin import token_required
import apppenyedia

COST_OF_LIVING_NYC = 1427.60

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

def get_city_with_livingcost_in_germany():
    LIST_CITY_AND_LIVINGCOST_IN_GERMANY = []
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT city, cost_of_living_index FROM `living_cost` WHERE city LIKE '%, Germany'")
        read_row = cursor.fetchall()
        
        for row in read_row:
            city = row['city'].split(',')[0]
            living_cost = round(float(row['cost_of_living_index']) * COST_OF_LIVING_NYC / 100, 2)
            data = { "city" : city, "living_cost_in_usd" : living_cost }
            LIST_CITY_AND_LIVINGCOST_IN_GERMANY.append(data)
        return LIST_CITY_AND_LIVINGCOST_IN_GERMANY

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

# http://127.0.0.1:5000/get-recomm-by-job
@app.route('/get-recomm-by-job/')
def get_recomm_by_job_index():
    response = {"usage1" : "/<job_role>", "usage2" : "/<job_role_first>/<job_role_last>"}
    return jsonify(response)

# http://127.0.0.1:5000/get-recomm-by-job/Software
@app.route('/get-recomm-by-job/<rolefirst>')
def get_recomm_by_job_using_single_role(rolefirst):
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
        data = {"job" : rolefirst, "city" : city, "salary_in_usd" : salary, "vacation_days" : vacation_days}
        # Append
        list_view_data.append(data)
    data = {"job" : rolefirst, "city" : "MALANGBOZ", "salary_in_usd" : 107856.0, "vacation_days" : 1}
    list_view_data.append(data)
    list_view_data = sorted(list_view_data, key=lambda i: (i["salary_in_usd"], i["vacation_days"]), reverse=True)
    
    return jsonify(list_view_data[0:5])

# http://127.0.0.1:5000/get-recomm-by-job/Software/a
@app.route('/get-recomm-by-job/<rolefirst>/<rolelast>')
def get_recomm_by_job_using_double_role(rolefirst, rolelast):
    # GET REGION DATA
    list_city = get_city_in_germany()
    list_view_data = []
    for city in list_city:
        # Rearrange city string
        city_first = city.split()[0]
        # Get Average Salary
        token = get_token_by_login()
        url = 'https://wakacipuy.my.id/estimatecost/getsalaries/'+ city_first +'/'+ rolefirst + '/' + rolelast + '/f/f?token=' + str(token)
        dataresponse = urlopen(url)
        dataresponse = json.loads(dataresponse.read())['avg_salary_usd']
        if dataresponse:
            salary = round(float(dataresponse), 2)
        else:
            salary = 0
        # Get Average Vacation Days
        token = get_token_by_login()
        url = 'https://wakacipuy.my.id/estimatecost/getvacationdays/'+ city_first +'/'+ rolefirst + '/' + rolelast + '/f/f?token=' + str(token)
        dataresponse = urlopen(url)
        dataresponse = json.loads(dataresponse.read())['avg_vacation_days']
        if dataresponse:
            vacation_days = int(dataresponse)
        else:
            vacation_days = 0
        # Create Data Dictionary
        job = rolefirst + " " + rolelast
        data = {"job" : job, "city" : city, "salary_in_usd" : salary, "vacation_days" : vacation_days}
        # Append
        list_view_data.append(data)
    data = {"job" : job, "city" : "MALANGBOZ", "salary_in_usd" : 107856.0, "vacation_days" : 1}
    list_view_data.append(data)
    list_view_data = sorted(list_view_data, key=lambda i: (i["salary_in_usd"], i["vacation_days"]), reverse=True)

    return jsonify(list_view_data[0:5])

@app.route('/get-recomm-by-living-cost/')
def get_recomm_by_living_cost_index():
    response = {"usage" : "/<category>"}
    # category ny high sama low
    return jsonify(response)

@app.route('/get-recomm-by-living-cost/<categorylivingcost>')
# category ny cuma ada 2, medium-high : index >= 70.05 sama medium-low : index < 70.05
# category ny cuma ada 2, medium-high : cost >= 1000usd sama medium-low : index < 1000usd
def high_living_cost(dic):
    return dic['living_cost_in_usd'] >= 1000
def low_living_cost(dic):
    return dic['living_cost_in_usd'] < 1000
def get_recomm_by_living_cost(categorylivingcost):
    list_city_livingcost = get_city_with_livingcost_in_germany()
    if categorylivingcost == "high":
        list = [d for d in list_city_livingcost if high_living_cost(d)]
    elif categorylivingcost == "low":
        list = [d for d in list_city_livingcost if low_living_cost(d)]
    else:
        return "Input salah"
    list = sorted(list, key=lambda i: i["living_cost_in_usd"])

    return jsonify(list[0:5])

@app.route('/get-recomm-by-all/')
def get_recomm_by_all_index():
    response = {"usage1" : "/<categorylivingcost>/<job_role>", "usage2" : "/<categorylivingcost>/<job_role_first>/<job_role_last>"}
    return jsonify(response)

@app.route('/get-recomm-by-all/<categorylivingcost>/<rolefirst>')
def get_recomm_by_all_using_single_role(categorylivingcost, rolefirst):
    # GET REGION AND LIVINGCOST DATA
    list_city_livingcost = get_city_with_livingcost_in_germany()
    if categorylivingcost == "high":
        list = [d for d in list_city_livingcost if high_living_cost(d)]
    elif categorylivingcost == "low":
        list = [d for d in list_city_livingcost if low_living_cost(d)]
    else:
        return "Input salah"
    list = sorted(list, key=lambda i: i["living_cost_in_usd"])

    # GET
    list_view_data = []
    for data in list:
        # Rearrange city string
        city = data['city'].split()[0]
        living_cost = data['living_cost_in_usd']
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
        if salary != 0 and vacation_days != 0:
            data = {"job" : rolefirst, "city" : city, "living_cost_in_usd" : living_cost,"salary_in_usd" : salary, "vacation_days" : vacation_days}
            # Append
            list_view_data.append(data)
    
    list_view_data = sorted(list_view_data, key=lambda i: i["living_cost_in_usd"])
    list_view_data = sorted(list_view_data, key=lambda i: (i["salary_in_usd"], i["vacation_days"]), reverse=True)
    
    return jsonify(list_view_data[0:5])

@app.route('/get-recomm-by-all/<categorylivingcost>/<rolefirst>/<rolelast>')
def get_recomm_by_all_using_double_role(categorylivingcost, rolefirst, rolelast):
    # GET REGION AND LIVINGCOST DATA
    list_city_livingcost = get_city_with_livingcost_in_germany()
    if categorylivingcost == "high":
        list = [d for d in list_city_livingcost if high_living_cost(d)]
    elif categorylivingcost == "low":
        list = [d for d in list_city_livingcost if low_living_cost(d)]
    else:
        return "Input salah"
    list = sorted(list, key=lambda i: i["living_cost_in_usd"])

    # GET
    list_view_data = []
    for data in list:
        # Rearrange city string
        city = data['city'].split()[0]
        living_cost = data['living_cost_in_usd']
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
        if salary != 0 and vacation_days != 0:
            data = {"job" : rolefirst, "city" : city, "living_cost_in_usd" : living_cost,"salary_in_usd" : salary, "vacation_days" : vacation_days}
            # Append
            list_view_data.append(data)
    
    list_view_data = sorted(list_view_data, key=lambda i: i["living_cost_in_usd"])
    list_view_data = sorted(list_view_data, key=lambda i: (i["salary_in_usd"], i["vacation_days"]), reverse=True)
    
    return jsonify(list_view_data[0:5])

@app.route('/get-info-city-job/')
def get_info_city_job_index():
    response = {"usage1" : "/<city>/<job_role>", "usage2" : "/<city>/<job_role_first>/<job_role_last>"}
    return jsonify(response)

@app.route('/get-info-city-job/<city>/<rolefirst>')
def get_info_city_job_using_single_role(city, rolefirst):
    list_city_livingcost = get_city_with_livingcost_in_germany()

    found = False
    i = 0
    for data in list_city_livingcost:
        if city == data['city']:
            found = True
            break
        i += 1
    
    if found:
        # Get Living Cost
        living_cost = list_city_livingcost[i]["living_cost_in_usd"]
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
        data = {"job" : rolefirst, "city" : city, "living_cost_in_usd" : living_cost, "salary_in_usd" : salary, "vacation_days" : vacation_days}
    else:
        return "ERROR"
    return jsonify(data)

@app.route('/get-info-city-job/<city>/<rolefirst>/<rolelast>')
def get_info_city_job_using_double_role(city, rolefirst, rolelast):
    list_city_livingcost = get_city_with_livingcost_in_germany()

    found = False
    i = 0
    for data in list_city_livingcost:
        if city == data['city']:
            found = True
            break
        i += 1
    
    if found:
        # Get Living Cost
        living_cost = list_city_livingcost[i]["living_cost_in_usd"]
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
        data = {"job" : rolefirst, "city" : city, "living_cost_in_usd" : living_cost, "salary_in_usd" : salary, "vacation_days" : vacation_days}
    else:
        return "ERROR"
    return jsonify(data)
