import streamlit as st
from app_quiz_vert import main as app1
from app_console_viz import main as app2
from app_discovery import main as app0

st.set_page_config(layout="wide")
# Create a dictionary to map menu items to their corresponding functions
apps = {
    "Chapter Discovery": app0,
    "Interactive Learning App": app1,
    "Student Performance Dashboard": app2,
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Go to:", list(apps.keys()))

# Display the selected app
if selection in apps:
    apps[selection]()
else:
    st.write("Something went wrong. Please select an app.")
