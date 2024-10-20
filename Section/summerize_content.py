import streamlit as st

@st.cache_data
def summarize_text(text):
    response = st.session_state.co.generate(
        model='command-light-nightly',
        prompt=f"Summarize the following text into an essay:\n\n{text}",
        temperature=0.5,
        k=0,
        stop_sequences=["--"]
    )
    return response.generations[0].text.strip()

def summerize():
    st.session_state.summary = summarize_text(st.session_state.transcription)
    editable_summary = st.text_area("Editable Summary:", st.session_state.summary, height=300)
    st.session_state.summary = editable_summary
    if st.button("Submit Summary"):
        st.session_state.step = 3