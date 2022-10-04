import jwt
import requests
import json
import yaml
import os
from tqdm import tqdm
import time
import calendar

# Extract and set API key and secret key
conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
API_KEY = conf['zoom_api']['key']
API_SEC = conf['zoom_api']['secret']
if not os.path.exists('downloads'):
    os.makedirs('downloads')

API_EP = 'https://api.zoom.us/v2' # Use for API Endpoint
FOLDER = 'downloads/'
recordings = []
downloads = []

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
    response = requests.get(API_EP+'/users/me/recordings', headers=headers)
    recordings_data = response.json()
    recordings.extend(recordings_data['meetings'])
    # print(json.dumps(recordings_data, indent=2))
    download_animation(response, FOLDER+'response.txt')
    print('- - - - -')
    # print(len(recordings))
    parseRecordings()
    print(str(len(downloads)) + " file(s) to download:")
    for download in downloads:
        print(download['file_name'])
    print("- - - - -")

def parseRecordings():
    for i, recording in enumerate(recordings):
        for download in recording['recording_files']:
            file_type = download['file_type']
            file_extension = download['file_extension']
            recording_id = download['id']
            if file_type == "":
                recording_type = 'incomplete'
            elif file_type != "TIMELINE":
                recording_type = download['recording_type']
            else:
                recording_type = download['file_type']
            download_url = download['download_url'] + "?access_token=" + generateToken()
            start_date_time = convertGMT(recording['start_time'])
            file_name = recording['topic'].strip() + '_' + start_date_time + '.' + file_extension.lower()
            downloads.append({
                'recording_id': recording_id,
                'recording_type': recording_type, 
                'file_type': file_type, 
                'file_extentsion': file_extension, 
                'file_name': file_name, 
                'download_url': download_url
            })

def convertGMT(recordTime):
    gmt = time.strptime(recordTime,"%Y-%m-%dT%H:%M:%SZ")
    localTime = time.strftime('%d%b%Y_%I%M%p',time.localtime(calendar.timegm(gmt)))
    return localTime

def download_animation(res, name):
    print('Downloading '+name+' ...')
    # total size in bytes.
    total_size = int(res.headers.get('content-length', 0))
    block_size = 32 * 1024  # 32 Kibibytes

    # create TQDM progress bar
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    try:
        with open(name, 'wb') as fd:
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

def download_files():
    for download in downloads:
        response = requests.get(download['download_url'], stream=True)
        download_animation(response, FOLDER+download['file_name'])

def deleteRecordings():
    headers = {
        'authorization': 'Bearer ' + generateToken(),
        'content-type': 'application/json',
    }

    print('- - - - -')
    print(str(len(recordings)) + " cloud recording(s) to delete:")
    for recording in recordings:
        print("meet: " + str(recording['id']))
    print('- - - - -')


    for i, recording in enumerate(recordings):
        meetingId = str(recording['id'])
        file_name = recording['topic'].strip() + "_" + convertGMT(recording['start_time'])
        response = requests.delete(API_EP + "/meetings/" + meetingId + "/recordings", headers=headers)
        if (response.status_code == 200 or response.status_code == 204):
            print("meet: " + meetingId + " | response: " + str(response.status_code))
            print(file_name + " | meet:" + meetingId + " | cloud recording moved to trash.")
        else:
            print("meet: " + meetingId + " | response: " + str(response.status_code))
            response.raise_for_status()

getRecordings()
download_files()
deleteRecordings()