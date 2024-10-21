import streamlit as st
import base64
import json

def encode_file_to_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

def final_preview():   
    # st.write("### Video:")
    # st.video(st.session_state.video_file)
        
    # st.write("### Title:")
    # st.text_input("", st.session_state.title, disabled=True)
        
    # st.write("### Summary:")
    # st.text_area("", st.session_state.summary, height=300, disabled=True)
        
    # st.write("### Notes:")
    # st.text_area("", st.session_state.notes, height=300, disabled=True)

    # st.write("### Download Notes as Word Document:")
    # if st.session_state.notes_doc_path:
    #     with open(st.session_state.notes_doc_path, "rb") as file:
    #         btn = st.download_button(
    #             label="Download Notes",
    #             data=file,
    #             file_name="generated_notes.docx",
    #             mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    #         )
    # if st.session_state.uploaded_files:
    #     st.write("### Uploaded Files:")
    #     if st.session_state.uploaded_files:
    #         for file in st.session_state.uploaded_files:
    #             st.write(file.name)
        
    # st.write("### MCQ Questions (Easy):")
    # st.text_area("", st.session_state.mcq_easy, height=300, disabled=True)

    # st.write("### MCQ Questions (Medium):")
    # st.text_area("", st.session_state.mcq_med, height=300, disabled=True)

    # st.write("### MCQ Questions (Hard):")
    # st.text_area("", st.session_state.mcq_hard, height=300, disabled=True)

    # st.write("### Descriptive Questions:")
    # st.text_area("", st.session_state.desc_quiz, height=300, disabled=True)

    data = {
        "vta_file" : True,
        "title": st.session_state.title,
        "transcript":st.session_state.transcription,
        "summary": st.session_state.summary,
        "notes": st.session_state.notes,
        "quiz": {
            "MCQ": [st.session_state.mcq_easy, st.session_state.mcq_med, st.session_state.mcq_hard],
            "Desc": [st.session_state.desc_quiz],
        },
        "video": encode_file_to_base64(st.session_state.video_file) if st.session_state.video_file else None,
        "uploaded_files": [
            {"name": file.name, "content": encode_file_to_base64(file)} for file in st.session_state.uploaded_files
        ] if st.session_state.uploaded_files else []            
    }
    json_data = json.dumps(data, indent=4)
        
    st.write("### Download JSON:")
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="VTA_content.json",
        mime="application/json"
    )
    
    st.markdown("To view the Result, [Click here](https://sjy-video-tutor-assist-student-side.streamlit.app/), and upload this VTA output file")