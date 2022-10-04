import jwt
import requests
import json
import yaml
import os
from tqdm import tqdm
from time import time

API_EP = 'https://api.zoom.us/v2' # Use for API Endpoint

# Extract and set API key and secret key
conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
API_KEY = conf['zoom_api']['key']
API_SEC = conf['zoom_api']['secret']

URL_V = 'https://us02web.zoom.us/rec/download/G2KH4yI9rP9TxBLdBQIN7bRSZbOVbdGw4ZJBvTpZjexEvr_9pZBEaf-B4niy1YCm_YIpMiWNfYRzfQpw.YIT5YbPGfmMciL3a'+'?access_token='
URL_A = 'https://us02web.zoom.us/rec/download/vITOPrJIipcWIruoqq6TCuPWcTnJztA48RI47Nr-3GsALbCeUHALnfbpyqNq7OlQwlgZNYoYDOyLwhOm.JIhVgqyaBvd3nkn-'+'?access_token='
FILE_TO_SAVE_AS_V = 'downloads/QUILL_041022.mp4'
FILE_TO_SAVE_AS_A = 'downloads/QUILL_041022.m4a'

conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
API_KEY = conf['zoom_api']['key']
API_SEC = conf['zoom_api']['secret']
if not os.path.exists('downloads'):
    os.makedirs('downloads')

def generateToken():
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time() + 5000},
        API_SEC,
        algorithm='HS256'
    )
    return token.decode('utf-8')

def download_animation(res, name):
    print('Downloading '+name+' ...')
    # total size in bytes.
    total_size = int(res.headers.get('content-length', 0))
    block_size = 32 * 1024  # 32 Kibibytes

    # create TQDM progress bar
    t = tqdm(total=total_size, unit='iB', unit_scale=True, colour='#fcba03')
    try:
        with open(name, 'wb') as fd:
            # with open(os.devnull, 'wb') as fd:  # write to dev/null when testing
            for chunk in res.iter_content(block_size):
                t.update(len(chunk))
                fd.write(chunk)  # write video chunk to disk
        t.close()
        print('Download Complete.')
        return True
    except Exception as e:
        # if there was some exception, print the error and return False
        print(e)
        return False

def getVideoRecordings():
    response = requests.get(URL_V+generateToken(), stream=True)
    download_animation(response, FILE_TO_SAVE_AS_V)
    # with open(FILE_TO_SAVE_AS_V, 'wb') as f:
    #     f.write(response.content)

def getAudioRecordings():
    response = requests.get(URL_A+generateToken(), stream=True)
    download_animation(response, FILE_TO_SAVE_AS_A)
    # with open(FILE_TO_SAVE_AS_A, 'wb') as f:
    #     f.write(response.content)

getAudioRecordings()
getVideoRecordings()