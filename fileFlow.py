import os
import shutil
import yaml
import time
import json

config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)
meetings_config = config['meetings']
downloaded_files = os.listdir("./downloads")
download_dir = "./downloads/"
log = "FILE TRANSFERS LOG:\n"

print(os.name)

def filterDownloads(file_name, data_format):
    if (file_name == meetings_config['quest']['file_name']):
        quest_downloads = list(filter(lambda x: x.find(file_name) != -1 and x.find(data_format) != -1, downloaded_files))
        filtered_downloads = list(filter(lambda x: x.find(meetings_config['quest_qna']['file_name']) == -1, quest_downloads))
    else:
        filtered_downloads = list(filter(lambda x: x.find(file_name) != -1 and x.find(data_format) != -1, downloaded_files))
    return filtered_downloads

def moveFiles(files, destination):
    global log
    if (not os.path.exists(destination)):
        log += "\nERROR: path does not exist - " + destination
        print("ERROR: path does not exist.",destination)
        return
    if len(files) == 0:
        return
    for file in files:
        log += "\nfile: " + file
        dest = shutil.move(download_dir+file, destination)
        time.sleep(2)
        log += "\nnew destination: " + dest
    log += "\n"

    print(json.dumps(files,indent=2), destination)

def writeLog():
    fp = open(download_dir+"log_fileOps.txt", 'w')
    fp.write(log)
    fp.close()

def main():
    for meeting in meetings_config:
        file_name = meetings_config[meeting]['file_name']
        filtered_downloads_audio = filterDownloads(file_name, 'm4a')
        filtered_downloads_video = filterDownloads(file_name, 'mp4')
        path_audio = meetings_config[meeting]['path_audio']
        path_video = meetings_config[meeting]['path_video']
        moveFiles(filtered_downloads_audio, path_audio)
        moveFiles(filtered_downloads_video, path_video)
    writeLog()

if __name__ == "__main__":
    main()