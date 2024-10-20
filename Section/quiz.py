import streamlit as st

@st.cache_data
def suggest_question_counts(summary):
    response = st.session_state.co.generate(
        model='command-light-nightly',
        prompt=f"""Based on the following summary, suggest the number of MCQ and Descriptive questions that can be generated without banality.
                For MCQs, suggest ranges for Easy, Intermediate, and Hard questions.
                For Descriptive, suggest ranges for Easy, Intermediate, and Hard questions.
                Summary: {summary}
                just give the below content alone
                For MCQ:
                Easy - (some number)
                Medium - 
                Hard - 
                For Descriptive
                Easy- 
                Medium -
                Hard -
                """,
        max_tokens=100,
        temperature=1.0,
        k=0,
        stop_sequences=["--"]
    )
    return response.generations[0].text.strip()

@st.cache_data
def generate_quiz(summary, difficulty_counts_mcq, difficulty_counts_desc):
    easy_mcq, med_mcq, hard_mcq = difficulty_counts_mcq
    easy_desc, med_desc, hard_desc = difficulty_counts_desc
    
    prompt_mcq_easy = f"""
    Generate json formart for {easy_mcq} Easy level MCQ questions based on the following summary\n\n{summary}
    \n\nThe format for Easy level MCQ questions is:
    "id": "1",
    "question": "#Question",
    "options": [
                "a) #Option 1",
                "b) #Option 2",
                "c) #Option 3",
                "d) #Option 4"
            ],
    "Answer": "#Option number alone(Ex: a)",]    
    Generate all {easy_mcq} Easy level MCQ questions perfectly and exactly like the given structure. Generate Required Quiz alone, no extra notes(dont give ```json```). start exactly with Easy: [].
    """

    prompt_mcq_med = f"""
    Generate json formart for {med_mcq} Medium level MCQ questions based on the following summary\n\n{summary}
    \n\nThe format for Medium level MCQ questions is:
    "id": "1",
    "question": "#Question",
    "options": [
                "a) #Option 1",
                "b) #Option 2",
                "c) #Option 3",
                "d) #Option 4"
            ],
    "Answer": "#Option number alone(Ex: a)",]    
    Generate all {med_mcq} Medium level MCQ questions perfectly and exactly like the given structure. Generate Required Quiz alone, no extra notes(dont give ```json```). start exactly with Medium: [].
    """

    prompt_mcq_hard = f"""
    Generate json formart for {hard_mcq} Hard level MCQ questions based on the following summary\n\n{summary}
    \n\nThe format for Hard level MCQ questions is:
    id: "1",
    question: "#Question",
    options: [
                "a) #Option 1",
                "b) #Option 2",
                "c) #Option 3",
                "d) #Option 4"
            ],
    Answer: "#Option number alone(Ex: a)",]    
    Generate all {hard_mcq} Hard level MCQ questions perfectly and exactly like the given structure. Generate Required Quiz alone, no extra notes(dont give ```json```). start exactly with Hard: [].
    """
    
    prompt_desc = f"""
    Generate json formart for {easy_desc} Easy, {med_desc} Medium, {hard_desc} Hard the Descriptive questions based on the following summary\n\n{summary}
    \n\nThe json format for Descriptive questions is:
    Easy: ["#Question1","#Question2",...],
    Medium: ["#Question1","#Question2",...],
    Hard: ["#Question1","#Question2",...],
    Generate all Descriptive questions perfectly and exactly like the given structure. Generate Required Quiz alone, no extra notes(dont give ```json```).don't start with DescQues: [] or anything.
    """
    
    with st.spinner('Generating Easy MCQ questions...'):
        response_mcq_easy = st.session_state.co.generate(
            model='command-xlarge-nightly',
            prompt=prompt_mcq_easy,
            temperature=0.75,
            k=0,
            stop_sequences=["--"]
        ) if easy_mcq > 0 else ""
        
    with st.spinner('Generating Medium MCQ questions...'):
        response_mcq_med = st.session_state.co.generate(
            model='command-xlarge-nightly',
            prompt=prompt_mcq_med,
            temperature=0.75,
            k=0,
            stop_sequences=["--"]
        ) if med_mcq > 0 else ""
        
    with st.spinner('Generating Hard MCQ questions...'):
        response_mcq_hard = st.session_state.co.generate(
            model='command-xlarge-nightly',
            prompt=prompt_mcq_hard,
            temperature=0.75,
            k=0,
            stop_sequences=["--"]
        ) if hard_mcq > 0 else ""
        
    with st.spinner('Generating Descriptive questions...'):
        response_desc = st.session_state.co.generate(
            model='command-xlarge-nightly',
            prompt=prompt_desc,
            temperature=0.75,
            k=0,
            stop_sequences=["--"]
        ) if (easy_desc + med_desc + hard_desc) > 0 else ""
    
        
    mcq_easy_text = response_mcq_easy.generations[0].text.strip() if easy_mcq > 0 else ""
    mcq_med_text = response_mcq_med.generations[0].text.strip() if med_mcq > 0 else ""
    mcq_hard_text = response_mcq_hard.generations[0].text.strip() if hard_mcq > 0 else ""
    desc_text = response_desc.generations[0].text.strip() if (easy_desc + med_desc + hard_desc) > 0 else ""
    
    return mcq_easy_text, mcq_med_text, mcq_hard_text, desc_text




def quiz():
    st.write("### Quiz Generation")

    if st.session_state.suggested_counts == "":
        with st.spinner('Generating suggestions for question counts...'):
            st.session_state.suggested_counts = suggest_question_counts(st.session_state.summary)
            
    st.write("#### Suggested Number of Questions:")
    st.write(st.session_state.suggested_counts)
            
    st.write("#### MCQ Questions")
    num_mcq_easy = st.number_input("Easy MCQs", min_value=0, value=0)
    num_mcq_medium = st.number_input("Intermediate MCQs", min_value=0, value=0)
    num_mcq_hard = st.number_input("Hard MCQs", min_value=0, value=0)

    st.write("#### Descriptive Questions")
    num_desc_easy = st.number_input("Easy Descriptive", min_value=0, value=0)
    num_desc_medium = st.number_input("Medium Descriptive", min_value=0, value=0)
    num_desc_hard = st.number_input("Hard Descriptive", min_value=0, value=0)

    if st.button("Generate Quiz"):
        with st.spinner('Generating quiz questions...'):
            difficulty_counts_mcq = (num_mcq_easy, num_mcq_medium, num_mcq_hard)
            difficulty_counts_desc = (num_desc_easy, num_desc_medium, num_desc_hard)
            mcq_easy, mcq_med, mcq_hard, desc_quiz = generate_quiz(st.session_state.summary, difficulty_counts_mcq, difficulty_counts_desc)
            st.session_state.mcq_easy = mcq_easy
            st.session_state.mcq_med = mcq_med
            st.session_state.mcq_hard = mcq_hard
            st.session_state.desc_quiz = desc_quiz
        mcqtextbox = "Easy:\n" + st.session_state.mcq_easy + "\n\nMedium:\n" + st.session_state.mcq_med + "\n\nHard:\n" + st.session_state.mcq_hard
        st.text_area("MCQ Questions:", mcqtextbox, height=300, disabled=True)
        st.text_area("Descriptive Questions:", st.session_state.desc_quiz, height=300, disabled=True)
        st.session_state.step = 5