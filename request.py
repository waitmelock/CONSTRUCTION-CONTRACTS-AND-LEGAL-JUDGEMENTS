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

def download_file(id, token):
    url = f"https://opendata.judicial.gov.tw/api/FilesetLists/{id}/file"
    headers = {"Content-Type": "application/json",
                "Token" : f"{token}"
               }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(f"{id}.file", 'wb') as f:
            f.write(response.content)
    else:
        print(response.status_code)
        print(f"Failed to download file with id {id}")

# Replace these with the actual IDs and your username and password
ids = [47180, 47181, 47182]
username = "andym901106"
password = "andym901106"

token = get_token(username, password)
if token:
    for id in ids:
        download_file(id, token)