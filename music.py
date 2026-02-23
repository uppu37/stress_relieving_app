import streamlit as st
import os

def music_player():
    st.subheader("🎵 Calm Music Player")

    music_folder = "music"

    if not os.path.exists(music_folder):
        st.error("Music folder not found!")
        return

    songs = [file for file in os.listdir(music_folder) if file.lower().endswith(".mp3")]

    if not songs:
        st.warning("No mp3 files found inside music folder.")
        return

    selected_song = st.selectbox("Choose a relaxing track:", songs)

    file_path = os.path.join(music_folder, selected_song)

    # Open file in binary mode
    try:
        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error(f"Error loading audio: {e}")