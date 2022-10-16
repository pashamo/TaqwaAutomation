"""
TODO
fix parseRecordings: too many cascading redundancies
fix sort functions: too many redundancies
"""

import jwt
import requests
import json
import yaml
import os
from tqdm import tqdm
import time
import calendar
import datetime

# Extract and set API key and secret key
conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
API_KEY = conf['zoom_api']['key']
API_SEC = conf['zoom_api']['secret']
quest_iterated = False
if not os.path.exists('downloads'):
    os.makedirs('downloads')

API_EP = 'https://api.zoom.us/v2' # Use for API Endpoint
FOLDER = 'downloads/'
recordings = []
downloads = []


def generateToken(): # generate JWT with HS256 algorithm, as per zoom api docs
    token = jwt.encode(
        {'iss': API_KEY, 'exp': time.time() + 5000},
        API_SEC,
        algorithm='HS256'
    )
    return token.decode('utf-8')

def getRecordings(): # access list of recordings using zoom recordings api
    headers = {
        'authorization': 'Bearer ' + generateToken(),
        'content-type': 'application/json',
    }
    fromdate = datetime.date.today() - datetime.timedelta(days=30)
    response = requests.get(API_EP+'/users/me/recordings', headers=headers, params={'from':fromdate})
    recordings_data = response.json()
    recordings.extend(recordings_data['meetings'])
    sortListByTime2(recordings)
    # print(json.dumps(recordings_data, indent=2))
    download_animation(response, FOLDER+'response.txt')
    parseRecordings()
    printDownloads()

def incrementCounter(): # increment QUEST counter and update yml
    global quest_iterated
    if (quest_iterated):
        conf['iterations']['quest'] += 1
        yaml.dump(conf, open('login.yml','w'))
        quest_iterated = False

def parseRecordings():
    for i, recording in enumerate(recordings):
        tempDownloads = []
        for download in recording['recording_files']:
            if (download['file_type'] == "CHAT"): # Avoid .txt files
                continue
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
            start_date_time = convertGMT(download['recording_start'])
            file_name = recording['topic'].strip() + '_' + start_date_time + '.' + file_extension.lower()
            tempDownloads.append({
                'recording_id': recording_id,
                'recording_type': recording_type, 
                'file_type': file_type, 
                'file_extentsion': file_extension, 
                'file_name': file_name, 
                'start_date_time': start_date_time,
                'download_url': download_url
            })
        copyToMaster(tempDownloads)
    sortList(downloads)

def copyToMaster(arr): # copy recordings for a meeting to the master list
    sortList(arr)
    if (len(arr) >= 4):
        appendParts(arr)
    for download in arr:
        downloads.append(download)

def sortList(arr): # -
    arr.sort(key=lambda x: x['file_name'], reverse=False)

def sortListByTime(arr): # - Use these after downloads are extracted
    arr.sort(key=lambda x: time.strptime(x['start_date_time'], '%d%b%Y_%I%M%p'), reverse=False)

def sortListByTime2(arr): # - Use this after recordings are extracted
    arr.sort(key=lambda x: time.strptime(x['start_time'],"%Y-%m-%dT%H:%M:%SZ"), reverse=False)
    
def appendParts(temparr): # append parts for a subset of downloads
    uniqueNames = []
    for download in temparr:
        tempname = download['file_name'][:-4]
        if tempname not in uniqueNames:
            uniqueNames.append(tempname)
    
    if len(uniqueNames) > 1:
        for i,unique in enumerate(uniqueNames):
            for download in temparr:
                tempname = download['file_name'][:-4]
                if (unique == tempname):
                    splitName = download['file_name'].split('_')
                    match splitName[0]:
                        case "Qur`an Quest":
                            splitName.insert(1,str(conf['iterations']['quest']))
                            splitName.insert(2,"part"+str(i+1))
                            global quest_iterated 
                            quest_iterated= True
                        case _:
                            splitName.insert(1,"part"+str(i+1))
                    download['file_name'] = '_'.join(splitName)
        incrementCounter()

def convertGMT(recordTime): # convert GMT to local(eastern) time
    gmt = time.strptime(recordTime,"%Y-%m-%dT%H:%M:%SZ")
    localTime = time.strftime('%d%b%Y_%I%M%p',time.localtime(calendar.timegm(gmt)))
    return localTime

def download_animation(res, name): # -
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

def download_files(): # -
    for download in downloads:
        response = requests.get(download['download_url'], stream=True)
        download_animation(response, FOLDER+download['file_name'])

def deleteRecordings(): # Delete(move to trash) all cloud recordings
    headers = {
        'authorization': 'Bearer ' + generateToken(),
        'content-type': 'application/json',
    }

    printRecordings()

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
        time.sleep(5)

def printDownloads(): # utility to print filenames for downloading
    print('- - - - -')
    print(str(len(downloads)) + " file(s) to download:")
    for download in downloads:
        print(download['file_name'])
        time.sleep(0.25)
    print("- - - - -")

def printRecordings(): # utility to print cloud recordings for deletion
    print('- - - - -')
    print(str(len(recordings)) + " cloud recording(s) to delete:")
    for recording in recordings:
        print("meet: " + str(recording['id']))
        time.sleep(0.25)
    print('- - - - -')

def main():
    getRecordings()
    download_files()
    deleteRecordings()

if __name__ == "__main__":
    main()