import streamlit as st
import hydralit_components as hc
import json
import time

questions = json.load(open("questions.json"))
# Sample data
# questions = 

def main():
    st.title("Interactive Learning App")

    # Select chapter
    chapter_names = [q["chapter"] for q in questions]
    selected_chapter = st.selectbox("Select a Chapter", chapter_names)
    selected_questions = [q for q in questions if q["chapter"] == selected_chapter][0]["content"]

    # Session state to keep track of current question index and answers
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = -1
        st.session_state.user_answers = [None] * len(selected_questions)
        st.session_state.question_type = [None] * len(selected_questions)

    if st.button("Start Quiz") or st.session_state.current_question_index >= 0:
        if st.session_state.current_question_index < len(selected_questions) - 1:
            st.session_state.current_question_index += 1
        current_index = st.session_state.current_question_index
        for i in range(current_index + 1):
            with hc.HyLoader("", loader_name=hc.Loaders.standard_loaders):
                time.sleep(1)
                current_question = selected_questions[i]
                with st.container():
                    st.markdown("---")  # Adds a horizontal line for better separation
                    st.markdown(f"### Question {i + 1}: {current_question['question']}")
                    answer = None
                    if current_question['type'] == 'TF':
                        answer = st.radio("Select True or False:", ["True", "False"], key=f"question_{i}")
                    elif current_question['type'] == 'MCQ':
                        answer = st.radio("Choose one:", current_question['options'], key=f"question_{i}")
                    elif current_question['type'] == 'MAQ':
                        answer = st.multiselect("Select all that apply:", current_question['options'], key=f"question_{i}")
                    elif current_question['type'] == 'FITB':
                        answer = st.text_input("Fill in the blank:", key=f"question_{i}")
                    elif current_question['type'] == 'NUMERICAL':
                        answer = st.text_input("Enter your answer:", key=f"question_{i}")
    
                    st.session_state.user_answers[i] = answer
                    st.session_state.question_type[i] = current_question['type']

        if current_index < len(selected_questions) - 1:
            if st.button("Next", key=f"next_{current_index}"):
                pass  # Just a trigger for the next question

        else:
            if st.button("Submit"):
                st.write("You've completed all questions in this chapter.")
                st.write("Your answers and correct answers:")
                for idx, q in enumerate(selected_questions):
                    if st.session_state.question_type[idx] == "MAQ":
                        correct = "Correct" if st.session_state.user_answers[idx] in q['answer'] else "Incorrect"
                    else:
                        correct = "Incorrect"
                        if st.session_state.user_answers[idx] in q['answer']:
                            correct = "Correct"
                        elif correct == "Incorrect":
                            for _q in q['answer']:
                                if st.session_state.user_answers[idx] in _q:
                                   correct = "Correct" 
                            
                    # 
                    color = "green" if correct == "Correct" else "red"
                    st.markdown(f"Q{idx+1}: Your answer: `{st.session_state.user_answers[idx]}` Correct answer: `{q['answer']}` - **{correct}**", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: {color};'>{correct}</span>", unsafe_allow_html=True)
                # Reset for a new round
                st.session_state.current_question_index = -1
                st.session_state.user_answers = [None] * len(selected_questions)

if __name__ == "__main__":
    main()
