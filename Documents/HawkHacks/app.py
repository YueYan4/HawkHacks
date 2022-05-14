#Authentication header
# curl --request GET \
#   --url https://api.assemblyai.com/v2/ \
#   --header 'authorization: YOUR-API-TOKEN'

import requests
from selenium import webdriver

auth_key = 'a30b0d235ea04ce5946b07f391afd504'

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'

driver = webdriver.Chrome()
get_url = driver.current_url

if "youtube.com" not in get_url:
    print("Invalid URL")

json = {
    "audio_url": get_url
}

headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}

headers_auth_only = {'authorization': auth_key}

response = requests.post(transcript_endpoint, json=json, headers=headers)

while (response.status_code != "completed" or response.status_code != "error"):
    response = requests.post(transcript_endpoint, json=json, headers=headers)


