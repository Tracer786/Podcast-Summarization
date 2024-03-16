from api_communication import *
import streamlit as st
import json

st.title('Podcast Summarization')
episode_id = st.sidebar.text_input('Episode ID')
button = st.sidebar.button('Get Summary!',on_click=save_transcript, args=(episode_id,))

if button:
    filename =episode_id + '_chapters.json'
    with open(filename,'r') as f:
        data = json.load(f)
        
        chapters = data['chapters']
        podcast_title = data['podcast_title']
        episode_title = data['episode_title']
        thumbnail = data['episode_thumbnail']
        
    st.header(f'{podcast_title} - {episode_title}')
    st.image(thumbnail)

    for chp in chapters:
        with st.expander(chp['gist']):
            chp['summary']

# save_transcript('3638f68447ea4b75a937a661a60c3f5f')