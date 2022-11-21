import requests
import json
from time import sleep
import time
import summarizer
import writeToWord
start_time = time.time()
API_key = "12dc709ba55f4823b712bee3534a0bf2" 

headers = headers = {
    'authorization': API_key, 
    'content-type': 'application/json',
}

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

def read_audio(file_path):
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(5_242_880)
            if not data:
                break
            yield data


def upload(file_path):
    upload_response =  requests.post(upload_endpoint, 
                                     headers=headers, 
                                     data=read_audio(file_path))

    return upload_response.json().get('upload_url')

def transcribe(upload_url): 

    json = {"audio_url": upload_url, "auto_chapters":True}
    
    response = requests.post(transcription_endpoint, json=json, headers=headers)
    transcription_id = response.json()['id']

    return transcription_id

def get_result(transcription_id): 
    
    current_status = "queued"

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"

    while current_status not in ("completed", "error"):
        
        response = requests.get(endpoint, headers=headers)
        current_status = response.json()['status']
        
        if current_status in ("completed", "error"):
            return response.json()
        else:
            sleep(60)
upload_url = upload("test2.mp3")
transcription_id = transcribe(upload_url)
response = get_result(transcription_id)
#print("hello")
print(response["text"])
#print(response['chapters'])

data=response["text"]
data=summarizer.toSummarize(data)

writeToWord.writeToDoc(data)

print("--- %s seconds ---" % (time.time() - start_time))