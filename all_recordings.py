import jwt
import requests
import json
import yaml
import time
import calendar
import datetime
import os

API_EP = 'https://api.zoom.us/v2' # Use for API Endpoint

# Extract and set API key and secret key
conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
print(conf)
API_KEY = conf['zoom_api']['key']
API_SEC = conf['zoom_api']['secret']
QUEST = conf['iterations']['quest']
conf['iterations']['quest'] += 1
print(QUEST)

documents = yaml.dump(conf,open('login.yml', 'w'))
print(documents)

if not os.path.exists('downloads'):
    os.makedirs('downloads')

def generateToken():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time.time() + 5000},
        API_SEC,
        algorithm='HS256'
    )
    return token.decode('utf-8')

def getRecordingsDef():
    headers = {
        'authorization': 'Bearer ' + generateToken(),
        'content-type': 'application/json',
    }
    r = requests.get(API_EP+'/users/me/recordings', headers=headers)
    print(json.dumps(r.json(), indent=2))
    # open("response.txt", "wb").write(r.content)

def getRecordingsMonth():
    headers = {
        'authorization': 'Bearer ' + generateToken(),
        'content-type': 'application/json',
    }
    fromdate = datetime.date.today() - datetime.timedelta(days=30)
    r = requests.get(API_EP+'/users/me/recordings', headers=headers, params={'from':fromdate})
    print(json.dumps(r.json(), indent=2))
    open("downloads/month_response.txt", "wb").write(r.content)

getRecordingsDef()
getRecordingsMonth()