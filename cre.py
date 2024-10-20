import streamlit as st
from streamlit_option_menu import option_menu
import cohere
from api_call import get_api_key
from Section.video_upload import upload_video
from Section.summerize_content import summerize
from Section.resources import resources
from Section.quiz import quiz
from Section.final_preview import final_preview

if not get_api_key():
    st.stop()

cohere_api_key = st.session_state.api_key
co = cohere.Client(cohere_api_key)
st.session_state.co = co


def main():
    st.title("Video Tutor Assist")
    
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "transcription" not in st.session_state:
        st.session_state.transcription = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "title" not in st.session_state:
        st.session_state.title = ""
    if "notes" not in st.session_state:
        st.session_state.notes = ""
    if "mcq_easy" not in st.session_state:
        st.session_state.mcq_easy = ""
    if "mcq_med" not in st.session_state:
        st.session_state.mcq_med = ""
    if "mcq_hard" not in st.session_state:
        st.session_state.mcq_hard = ""
    if "desc_quiz" not in st.session_state:
        st.session_state.desc_quiz = ""
    if "suggested_counts" not in st.session_state:
        st.session_state.suggested_counts = ""
    if "video_file" not in st.session_state:
        st.session_state.video_file = None
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "notes_doc_path" not in st.session_state:
        st.session_state.notes_doc_path = None
    
    with st.sidebar:
        step = option_menu(
            "Steps",
            ["Video", "Summary", "Resources", "Quiz Questions", "Final JSON"],
            icons=["cloud-upload", "file-text", "book", "question-circle", "eye"],
            menu_icon="cast",
            default_index=st.session_state.step - 1,
            orientation="vertical"
        )

    if step == "Video":
        upload_video()

    if st.session_state.step >= 2 and step == "Summary":
        summerize()

    if st.session_state.step >= 3 and step == "Resources":
        resources()

    if st.session_state.step >= 4 and step == "Quiz Questions":
        quiz()

    if st.session_state.step == 5 and step == "Final JSON":
        final_preview()

if __name__ == "__main__":
    main()

