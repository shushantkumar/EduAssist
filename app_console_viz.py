import streamlit as st
import hydralit_components as hc
import json
import plotly.express as px
import pandas as pd

# st.set_page_config(layout="wide")

reverse_mapping = {
    "TF": "True or False",
    "MCQ": "Multiple Choice Questions",
    "MAQ": "Multiple Answer Questions",
    "FITB": "Fill in the Blanks",
    "NUMERICAL": "Numerical Questions"
}

# Sample data
data = json.load(open("console_questions.json"))


def resolve_playbook(title, avg_val):
    if avg_val < 0.15:
            hc.info_card(title=f"{title}",
                        title_text_size="1.2rem",
                        content_text_size="1.0rem",
                        icon_size="1.5rem",
                        content=avg_val,
                        bar_value=avg_val*100,
                        sentiment="bad" )
    elif avg_val <= 0.4:
        hc.info_card(title=f"{title}",
                    title_text_size="1.2rem",
                    content_text_size="1.0rem",
                    icon_size="1.5rem",
                    content=avg_val,
                    bar_value=avg_val*100,
                    sentiment="neutral")
    else:
        hc.info_card(title=f"{title}",
                    title_text_size="1.2rem",
                    content_text_size="1.0rem",
                    icon_size="1.5rem",
                    content=avg_val,
                    bar_value=avg_val*100,
                    sentiment="good")
    

# Function to calculate scores
def calculate_scores(data):
    scores = {
        "overall": 0,
        "category": {"TF": 0, "MCQ": 0, "MAQ": 0, "FITB": 0, "NUMERICAL": 0},
        "difficulty": {"Easy": 0, "Medium": 0, "Hard": 0},
        "topic": {},
        "consistency": {}
    }
    total_questions = 0

    for chapter in data:
        chapter_name = chapter["chapter"]
        chapter_score = 0
        chapter_questions = 0

        if chapter_name not in scores["topic"]:
            scores["topic"][chapter_name] = 0

        for question in chapter["content"]:
            correct = "Incorrect"
            if question["type"] == "MAQ":
                # Check if any of the student's answers is in the correct answers list
                correct = "Correct" if any(ans in question["answer"] for ans in question["students_answer"]) else "Incorrect"
            else:
                # Check if the student's answer is in the correct answers list
                if question["students_answer"] in question["answer"]:
                    correct = "Correct"
                elif correct == "Incorrect":
                    # Check if any correct answer contains the student's answer
                    for _q in question['answer']:
                        if question["students_answer"] in _q:
                            correct = "Correct"
                            break

            # Update scores based on correctness
            if correct == "Correct":
                scores["category"][question["type"]] += 1
                scores["difficulty"][question["difficulty"]] += 1
                scores["topic"][chapter_name] += 1
                chapter_score += 1
                scores["overall"] += 1

            chapter_questions += 1
            total_questions += 1

        # Calculate consistency as the ratio of correct answers to total questions in the chapter
        scores["consistency"][chapter_name] = chapter_score / chapter_questions if chapter_questions > 0 else 0

    # Normalize scores by the number of questions in each category, difficulty, and overall
    for key in scores["category"]:
        scores["category"][key] /= total_questions
    for key in scores["difficulty"]:
        scores["difficulty"][key] /= total_questions
    scores["overall"] /= total_questions

    return scores

import time

def main():
# Load data and calculate scores
    scores = calculate_scores(data)
    
    # Streamlit app
    st.title('Student Performance Dashboard')

    with hc.HyLoader("Generating Students Score...", loader_name=hc.Loaders.pacman):
        time.sleep(2)
        st.header("Overall Score")
        st.header(f":green[{scores['overall']*100}%]")

    with hc.HyLoader("Loading...", loader_name=hc.Loaders.showcase_pretty):
        time.sleep(2)
        st.header("Score Distribution by Category")
        coles = st.columns([0.5, 0.5])
        with coles[0]:
            cols = st.columns(3)
            cols_idx = 0
            dif_score = []
            for category, score in scores["category"].items():
                with cols[cols_idx]:
                    resolve_playbook(reverse_mapping[category], score)
                    dif_score.append((reverse_mapping[category], score*100))
                    cols_idx += 1
                    cols_idx = cols_idx % 3
        with coles[1]:
            df = pd.DataFrame(dif_score, columns=["Category", "Score"])
            fig = px.bar(df, x="Category", y="Score", color="Category")
            # fig.update_layout(yaxis_range=[0, 100]) 
            st.plotly_chart(fig)
                
    with hc.HyLoader("Loading...", loader_name=hc.Loaders.showcase_pretty):
        time.sleep(2)
        st.header("Score Distribution by Difficulty")
        coles = st.columns([0.5, 0.5])
        with coles[0]:
            cols = st.columns(len(scores["difficulty"]))
            cols_idx = 0
            dif_score = []
            for difficulty, score in scores["difficulty"].items():
                with cols[cols_idx]:
                    dif_score.append((difficulty, score*100))
                    resolve_playbook(difficulty, score)
                    cols_idx += 1
        with coles[1]:
            df = pd.DataFrame(dif_score, columns=["Difficulty", "Score"])
            fig = px.bar(df, x="Difficulty", y="Score", color="Difficulty")
            # fig.update_layout(yaxis_range=[0, 100]) 
            st.plotly_chart(fig)
        

    with hc.HyLoader("Loading...", loader_name=hc.Loaders.showcase_pretty):
        time.sleep(2)
        st.header("Topic-wise Performance")
        coles = st.columns([0.5, 0.5])
        with coles[0]:
            cols = st.columns(len(scores["topic"]))
            cols_idx = 0
            dif_score = []
            for topic, score in scores["topic"].items():
                with cols[cols_idx]:
                    resolve_playbook(topic, score)
                    cols_idx += 1
                    dif_score.append((topic, score))
        with coles[1]:
            df = pd.DataFrame(dif_score, columns=["Topic", "Score"])
            fig = px.bar(df, x="Topic", y="Score", color="Topic")
            # fig.update_layout(yaxis_range=[0, 100]) 
            st.plotly_chart(fig)

    with hc.HyLoader("Loading...", loader_name=hc.Loaders.showcase_pretty):
        time.sleep(2)
        st.header("Consistency Across Different Sections")
        coles = st.columns([0.5, 0.5])
        with coles[0]:
            cols = st.columns(len(scores["topic"]))
            cols_idx = 0
            dif_score = []
            for section, consistency in scores["consistency"].items():
                with cols[cols_idx]:
                    resolve_playbook(section, consistency)
                    cols_idx += 1
                    dif_score.append((section, consistency*100))
        with coles[1]:
            df = pd.DataFrame(dif_score, columns=["Section", "Score"])
            fig = px.bar(df, x="Section", y="Score", color="Section")
            st.plotly_chart(fig)



# Run the app
if __name__ == "__main__":
    main()
