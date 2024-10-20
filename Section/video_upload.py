import streamlit as st
import moviepy.editor as mp
import whisper
import tempfile

@st.cache_resource
def load_model():
    return whisper.load_model("base")

@st.cache_data
def transcribe_video(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(file.read())
        temp_video_path = temp_video_file.name
    
    video = mp.VideoFileClip(temp_video_path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_path = temp_audio_file.name
        video.audio.write_audiofile(temp_audio_path)
    
    model = load_model()
    result = model.transcribe(temp_audio_path)
    return result['text']

def upload_video():
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
        
    if uploaded_file is not None:
        st.video(uploaded_file)
        with st.spinner('Processing video...'):
            st.session_state.video_file = uploaded_file
            st.session_state.transcription = transcribe_video(uploaded_file)                
        if st.button("Submit Video"):
            st.session_state.step = 2