import yaml
import time
import vimeo
import json

config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)
API_TOK = config['network']['vimeo_api']['token']
API_KEY = config['network']['vimeo_api']['id']
API_SEC = config['network']['vimeo_api']['secret']
FOLDER = "./downloads/"
file_name = "TaqwaAutomation_1.1.0_setup.mp4"

client = vimeo.VimeoClient(
    token=API_TOK,
    key=API_KEY,
    secret=API_SEC
)

uri = client.upload(FOLDER+file_name, data={
  'name': file_name[:-4],
  'description': 'Tutorial for v1.1.0'
})
print('Your video URI is: %s\n\n' % (uri))

while True:
    response = client.get(uri + '?fields=transcode.status').json()
    if response['transcode']['status'] == 'complete':
        print('Your video finished transcoding.')
        break
    elif response['transcode']['status'] == 'in_progress':
        print('Your video is still transcoding.')
    else:
        print('Your video encountered an error during transcoding.')
        break
    time.sleep(10)

response = client.get(uri + '?fields=link').json()
print("\n\nYour video link is: %s" % response['link'])