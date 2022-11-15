import yaml
import time
import vimeo
import json
import os

config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)
API_TOK = config['network']['vimeo_pasha_api']['token']
API_KEY = config['network']['vimeo_pasha_api']['id']
API_SEC = config['network']['vimeo_pasha_api']['secret']
# API_TOK = config['network']['vimeo_api']['token']
# API_KEY = config['network']['vimeo_api']['id']
# API_SEC = config['network']['vimeo_api']['secret']
downloaded_files = os.listdir("./downloads")
upload_list = []
download_dir = "./downloads/"
log = "VIMEO UPLOADS LOG:\n"
client = vimeo.VimeoClient(
    token=API_TOK,
    key=API_KEY,
    secret=API_SEC
)

def uploadQuick(video):
    global log
    uri = client.upload(download_dir+video, data={
    'name': "###TEST###"+video[:-4],
    'description': "###TEST###"
    })
    response = client.get(uri + '?fields=link').json()

    print("Video uploaded.\nYour video URI is: %s" % (uri))
    print("Your video link is: %s" % response['link'],"\n")
    
    log += "\nfile: " + video
    log += "\nVideo uploaded.\nYour video URI is: " + uri
    log += "\nYour video link is: " + response['link'] + "\n"

def uploadVideos(videos):
    for video in videos:
        print("> ",video)
        uploadQuick(video)
    print("Uploads have completed.")

def getVideosList():
    return list(filter(lambda x: x.endswith(".mp4"), downloaded_files))

def writeLog():
    fp = open(download_dir+"log_vimeoFlow.txt", 'w')
    fp.write(log)
    fp.close()

def printUploads(): # utility to print recordings for upload
    print('- - - - -')
    print(str(len(upload_list)) + " recording(s) to upload:")
    for recording in upload_list:
        print("> ",recording)
        time.sleep(0.25)
    print('- - - - -')

upload_list = getVideosList()
printUploads()
uploadVideos(upload_list)
writeLog()