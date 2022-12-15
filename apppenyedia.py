import pymysql
from flask import jsonify

from appflask import app
from config import mysql
from clientlogin import token_required

COST_OF_LIVING_NYC = 1427.60

@app.route('/get-living-cost/<citypick>')
# @token_required
def getLivingCostFromCity(citypick):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT cost_of_living_index FROM `living_cost` WHERE city LIKE '" + citypick + ",%'")
        read_row = cursor.fetchone()
        
        living_cost = round(float(read_row["cost_of_living_index"]) * COST_OF_LIVING_NYC / 100, 2)
        data = { "living_cost_in_usd" : living_cost, "msg" : "Data berhasil ditemukan" }
    
        response = jsonify(data)
        response.status_code = 200
        return response
    
    except Exception as e:
        print(e)
        return jsonify({"msg" : "Data tidak ditemukan"})
    
    finally:
        cursor.close()
        conn.close()


@app.route('/get-rent-cost/<citypick>')
@token_required
def getRentCostFromCity(citypick):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT rent_index FROM `living_cost` WHERE city LIKE '" + citypick + ",%'")
        read_row = cursor.fetchone()
        
        rent_cost = round(float(read_row["rent_index"]) * COST_OF_LIVING_NYC / 100, 2)
        data = { "rent_cost_in_usd" : rent_cost, "msg" : "Data berhasil ditemukan" }
    
        response = jsonify(data)
        response.status_code = 200
        return response
    
    except Exception as e:
        print(e)
        return jsonify({"msg" : "Data tidak ditemukan"})
    
    finally:
        cursor.close()
        conn.close()


@app.route('/get-groceries-cost/<citypick>')
@token_required
def getGroceriesCostFromCity(citypick):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT groceries_index FROM `living_cost` WHERE city LIKE '" + citypick + ",%'")
        read_row = cursor.fetchone()
        
        groceries_cost = round(float(read_row["groceries_index"]) * COST_OF_LIVING_NYC / 100, 2)
        data = { "groceries_cost_in_usd" : groceries_cost, "msg" : "Data berhasil ditemukan" }
    
        response = jsonify(data)
        response.status_code = 200
        return response
    
    except Exception as e:
        print(e)
        return jsonify({"msg" : "Data tidak ditemukan"})
    
    finally:
        cursor.close()
        conn.close()


@app.route('/get-restaurant-cost/<citypick>')
@token_required
def getRestaurantCostFromCity(citypick):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT restaurant_price_index FROM `living_cost` WHERE city LIKE '" + citypick + ",%'")
        read_row = cursor.fetchone()
        
        restaurant_cost = round(float(read_row["restaurant_price_index"]) * COST_OF_LIVING_NYC / 100, 2)
        data = { "restaurant_cost_in_usd" : restaurant_cost, "msg" : "Data berhasil ditemukan" }
    
        response = jsonify(data)
        response.status_code = 200
        return response
    
    except Exception as e:
        print(e)
        return jsonify({"msg" : "Data tidak ditemukan"})
    
    finally:
        cursor.close()
        conn.close()


@app.route('/get-power-cost/<citypick>')
@token_required
def getPowerCostFromCity(citypick):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT local_purchasing_power_index FROM `living_cost` WHERE city LIKE '" + citypick + ",%'")
        read_row = cursor.fetchone()
        
        restaurant_cost = round(float(read_row["local_purchasing_power_index"]) * COST_OF_LIVING_NYC / 100, 2)
        data = { "local_purchasing_power_cost_in_usd" : restaurant_cost, "msg" : "Data berhasil ditemukan" }
    
        response = jsonify(data)
        response.status_code = 200
        return response
    
    except Exception as e:
        print(e)
        return jsonify({"msg" : "Data tidak ditemukan"})
    
    finally:
        cursor.close()
        conn.close()