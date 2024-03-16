from api_communication import *
import streamlit as st

st.title('Welcome to my application that creates podcast summaries.')
st.sidebar.text_input('Please input an episode id')
st.sidebar.button('Get podcast summary!')

save_transcript('3638f68447ea4b75a937a661a60c3f5f')