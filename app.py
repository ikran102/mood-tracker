import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mood Tracker", page_icon="🧠")
with st.sidebar:
    st.header("🧠 Mood Tracker")
    st.write("Log your daily mood and reflect on patterns over time.")

    if st.button("🔄 Start New Session"):
        st.session_state.clear()
        st.rerun()



st.title("🧠 Mood Tracker")
st.write("Track your mood daily and reflect on how you're feeling.")

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    st.session_state.username = st.text_input("Enter your name to start")
    if not st.session_state.username:
        st.stop()

mood = st.selectbox(
    "How are you feeling today?",
    ["😊 Happy", "😐 Neutral", "😔 Sad", "😟 Anxious", "😡 Angry"]
)

note = st.text_area("Want to add a note? (optional)")

if st.button("💾 Save mood"):
    data = {
        "User": [st.session_state.username],
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "Mood": [mood],
        "Note": [note]
    }

    df = pd.DataFrame(data)

    try:
        existing = pd.read_csv("moods.csv")
        df = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv("moods.csv", index=False)
    st.success("Mood saved 💙")

st.divider()

st.subheader("📊 Mood History")

try:
    history = pd.read_csv("moods.csv")

    history = history[history["User"] == st.session_state.username]

    if history.empty:
        st.info("No mood entries yet for you.")
    else:
        st.dataframe(history)

        mood_map = {
            "😊 Happy": 5,
            "😐 Neutral": 3,
            "😔 Sad": 2,
            "😟 Anxious": 2,
            "😡 Angry": 1
        }

        history["Mood Score"] = history["Mood"].map(mood_map)

        st.subheader("📈 Mood Trend Over Time")
        st.line_chart(history["Mood Score"])

except FileNotFoundError:
    st.info("No mood entries yet.")
