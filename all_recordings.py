import jwt
import requests
import json
import yaml
import time
import calendar

API_EP = 'https://api.zoom.us/v2' # Use for API Endpoint

# Extract and set API key and secret key
conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
API_KEY = conf['zoom_api']['key']
API_SEC = conf['zoom_api']['secret']

def generateToken():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time.time() + 5000},
        API_SEC,
        algorithm='HS256'
    )
    return token.decode('utf-8')

def getRecordings():
    headers = {
        'authorization': 'Bearer ' + generateToken(),
        'content-type': 'application/json',
    }
    r = requests.get(API_EP+'/users/me/recordings', headers=headers)
    print(json.dumps(r.json(), indent=2))
    # open("response.txt", "wb").write(r.content)

getRecordings()