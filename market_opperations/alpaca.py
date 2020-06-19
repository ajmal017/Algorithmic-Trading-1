import requests
import json
from config import *

API_ENDPOINT = 'https://paper-api.alpaca.markets'
API_KEY = 'PKDRD9AH48G37RDKGW36'
API_SECRET = 'YLx3e2Tu0fYPHNE0Uad/bezNOybP0RbQICyBYOu8'
ACCOUNT_URL = "{}/v2/account".format(API_ENDPOINT)
ORDERS_URL = "{}/v2/orders".format(API_ENDPOINT)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}

def get_account():
	r = requests.get(ACCOUNT_URL, headers=HEADERS)
	return json.loads(r.content)

def create_order(symbol, typ, quantity, side, time_in_force):
	data = {
		"symbol":symbol, 
		"type": typ, 
		"qty":quantity, 
		"side":side, 
		"time_in_force":time_in_force
	}
	r = requests.post(ORDERS_URL, json=data ,headers=HEADERS)
	return json.loads(r.content)

