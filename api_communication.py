import requests   # requests library is required to talk to the Assembly AI's API.
import json
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_LISTENNOTES
import time

transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
assemblyai_headers = {'authorization': API_KEY_ASSEMBLYAI} 

listennotes_episode_endpoint = "https://listen-api.listennotes.com/api/v2/episodes"
listennotes_headers ={'X-ListenAPI-Key': API_KEY_LISTENNOTES}

def get_episode_audio_url(episode_id):
    url = listennotes_episode_endpoint + '/' + episode_id
    response = requests.request('GET', url, headers = listennotes_headers)
    data = response.json()
    print(data)

# transcribe
def transcribe(audio_url,sentiment_analysis):
    transcript_request = { "audio_url": audio_url, 'sentiment_analysis': sentiment_analysis}
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=sentiment_analysis)
    # print(response.json())
    job_id = transcript_response.json()['id']
    return job_id

# polling 
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers = listennotes_headers)
    # print(polling_response)
    # print(polling_response.json())
    return polling_response.json()

#will check whether the polling is complete or not
def get_transcription_result_url(url,sentiment_analysis):
    transcribe_id = transcribe(url,sentiment_analysis)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        
        print('Waiting 30 seconds...')
        time.sleep(30)
        
# save transcription
def save_transcript(url,title,sentiment_analysis = False):
    data,error = get_transcription_result_url(url,sentiment_analysis)

    if data:
        filename = title + ".txt"
        with open(filename, "w") as f:
            f.write(data['text'])
        
        if sentiment_analysis:
            filename = title + '_sentiments.json'
            with open(filename,'w') as f:
                sentiments = data['sentiment_analysis_results']
                json.dump(sentiments, f, indent=4)
            print('Transcript saved')
            return True
        elif error:
            print("Error!!",error)
            return False