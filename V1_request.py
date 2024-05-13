import requests
import os
import json
def get_token(username, password):
    # Replace with the actual login API
    login_url = "https://data.judicial.gov.tw/jdg/api/Auth"
    headers = {"Content-Type": "application/json"}
    data = {
        "user": username,
        "password": password
    }
    response = requests.post(login_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200: 
        return response.json().get('Token')
    else:
        print("Failed to get token")
        return None

def get_data(index,token):
    # Replace with the actual login API
    login_url = "https://data.judicial.gov.tw/jdg/api/jDoc"
    headers = {"Content-Type": "application/json"}
    data = {
        "Token" : f"{token}",
        "j" : f"{index}"
    }
    response = requests.post(login_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(response.json())
    else:
        print("Failed to get data")
        return None
    
# Replace these with the actual IDs and your username and password
ids = ["CHDM,105,交訴,51,20161216,1"] #案號list
username = "#your username"
password = "#your password"

token=get_token(username, password)
for id in ids:
    get_data(id,token)
