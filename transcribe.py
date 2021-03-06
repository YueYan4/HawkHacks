"""
    TODO:Get YT url from user input
    TODO: Download YT audio and save locally
    TODO: Send YT audio to AssemblyAI API for transcription
    
"""
from urllib import request
from config import auth_key
import youtube_dl, requests

ydl_opts = {
   'format': 'bestaudio/best',
   'postprocessors': [{
       'key': 'FFmpegExtractAudio',
       'preferredcodec': 'mp3',
       'preferredquality': '192',
   }],
   'ffmpeg-location': './',
   'outtmpl': "./%(id)s.%(ext)s",
   'nocheckcertificate': True

}

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'

headers_auth_only = {'authorization': auth_key}
headers = {
   "authorization": auth_key,
   "content-type": "application/json"
}
CHUNK_SIZE = 5242880


polling_endpoint = ""

 

def transcribe_from_link(link, categories):
    _id = link.strip()
    def download_video(_id):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(_id)

    # download audio of YT video locally
    meta = download_video(_id)
    save_location = meta['id'] + ".mp3"

    print(f"Saved mp3 to {save_location}")

    def read_file(filename):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    # Upload audio file to AssemblyAI
    upload_response = requests.post(
        upload_endpoint,
        headers=headers_auth_only, data=read_file(save_location)
    )
    audio_url = upload_response.json()['upload_url']
    print(f'Uploaded to {audio_url}')

    transcript_request = {
        'audio_url': audio_url,
        'iab_categories': 'True' if categories else 'False',
    }
    
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)

    transcript_id = transcript_response.json()['id']
    polling_endpoint = transcript_endpoint + "/" + transcript_id

    print(f"Transcribing at {polling_endpoint}")

    return polling_endpoint


def check_transcript_status(polling_point):
    response = requests.get(polling_point, headers=headers)
    print(response.json()['text'])
    return response.json()['text']

# transcribe_from_link("https://www.youtube.com/watch?v=pAgnJDJN4VA", False)