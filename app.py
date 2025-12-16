import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mood Tracker", page_icon="🧠")

st.title("🧠 Mood Tracker")
st.write("Track your mood daily and reflect on how you're feeling.")

mood = st.selectbox(
    "How are you feeling today?",
    ["😊 Happy", "😐 Neutral", "😔 Sad", "😟 Anxious", "😡 Angry"]
)

note = st.text_area("Want to add a note? (optional)")

if st.button("Save mood"):
    data = {
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
    st.dataframe(history)
except FileNotFoundError:
    st.info("No mood entries yet.")
