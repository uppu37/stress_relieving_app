import streamlit as st
from mood_detector import detect_mood
from quotes import get_quote
from breathing import breathing_exercise
from music import music_player

st.set_page_config(page_title="AI Stress Relief App", page_icon="💙", layout="centered")

st.title("💙 AI-Based Stress Relief App")

menu = st.sidebar.selectbox(
    "Choose Feature",
    ["Mood Detection", "Breathing Exercise", "Calm Music Player"]
)

# ---------------- Mood Detection ----------------
if menu == "Mood Detection":
    st.write("Share how you are feeling today:")

    user_input = st.text_area("Type your feelings here...")

    if st.button("Analyze Mood"):
        if user_input.strip() != "":
            mood, score = detect_mood(user_input)

            st.write(f"### Detected Mood: {mood}")
            st.write(f"Confidence Score: {round(score, 2)}")

            quote = get_quote(mood)
            st.info(quote)

        else:
            st.warning("Please enter some text first.")

# ---------------- Breathing ----------------
elif menu == "Breathing Exercise":
    breathing_exercise()

# ---------------- Music ----------------
elif menu == "Calm Music Player":
    music_player()

