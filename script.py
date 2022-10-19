import jwt
import requests
import yaml
import os
import time
import calendar
import datetime
from tqdm import tqdm

# Extract and set API key and secret key
conf = yaml.load(open('login.yml'), Loader=yaml.FullLoader)
API_KEY = conf['zoom_api']['key']
API_SEC = conf['zoom_api']['secret']
abc_iterated = False
ark_iterated = False
quest_iterated = False
quill_iterated = False
sahih_iterated = False
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
    
    try:
        return token.decode('utf-8')
    except AttributeError:
        return token

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
    global abc_iterated
    global ark_iterated
    global quest_iterated
    global quill_iterated
    global sahih_iterated
    
    if (abc_iterated):
        conf['iterations']['abc'] += 1
        yaml.dump(conf, open('login.yml','w'))
        abc_iterated = False
    if (ark_iterated):
        conf['iterations']['ark'] += 1
        yaml.dump(conf, open('login.yml','w'))
        ark_iterated = False
    if (quest_iterated):
        conf['iterations']['quest'] += 1
        yaml.dump(conf, open('login.yml','w'))
        quest_iterated = False
    if (quill_iterated):
        conf['iterations']['quill'] += 1
        yaml.dump(conf, open('login.yml','w'))
        quill_iterated = False
    if (sahih_iterated):
        conf['iterations']['sahih'] += 1
        yaml.dump(conf, open('login.yml','w'))
        sahih_iterated = False

def parseRecordings():
    for i, recording in enumerate(recordings):
        tempDownloads = []
        if (not isWhiteListedMeeting(recording['topic'].strip())):
            continue
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
            meeting_name = getMeetingName(recording['topic'].strip())
            file_name = meeting_name + '_' + start_date_time.split('_')[0] + '.' + file_extension.lower()
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

def isWhiteListedMeeting(meeting):
    match meeting.lower():
        case "abc":
            return True
        case "ark":
            return True
        case "quill":
            return True
        case "qur`an quest":
            return True
        case "the sahih":
            return True
        case _:
            return False

def getMeetingName(meeting):
    match meeting.lower():
        case "abc":
            return conf['class_names']['abc']
        case "ark":
            return conf['class_names']['ark']
        case "quill":
            return conf['class_names']['quill']
        case "qur`an quest":
            return conf['class_names']['quest']
        case "the sahih":
            return conf['class_names']['sahih']
        case _:
            return 'Unavailable'

def copyToMaster(arr): # copy recordings for a meeting to the master list
    sortList(arr)
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
        tempname = {
            'name': download['file_name'][:-4],
            'date': download['start_date_time']
        }
        if tempname not in uniqueNames:
            uniqueNames.append(tempname)
    
    for i,unique in enumerate(uniqueNames):
        for download in temparr:
            tempname = {
                'name': download['file_name'][:-4],
                'date': download['start_date_time']
            }
            if (unique == tempname):
                splitName = download['file_name'].split('_')
                if (splitName[0] == conf['class_names']['abc']):
                    splitName[0] = splitName[0] + str(conf['iterations']['abc'])
                    global abc_iterated 
                    abc_iterated= True
                elif (splitName[0] == conf['class_names']['ark']):
                    splitName[0] = splitName[0] + str(conf['iterations']['ark'])
                    global ark_iterated 
                    ark_iterated= True
                elif (splitName[0] == conf['class_names']['quest']):
                    splitName[0] = splitName[0] + str(conf['iterations']['quest'])
                    global quest_iterated 
                    quest_iterated= True
                elif (splitName[0] == conf['class_names']['quill']):
                    splitName[0] = splitName[0] + str(conf['iterations']['quill'])
                    global quill_iterated 
                    quill_iterated= True
                elif (splitName[0] == conf['class_names']['sahih']):
                    splitName[0] = splitName[0] + str(conf['iterations']['sahih'])
                    global sahih_iterated 
                    sahih_iterated= True
                else:
                    if len(uniqueNames) > 1:
                        splitName.insert(1,"part"+str(i+1))

                download['file_name'] = ' - '.join(splitName)
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