import streamlit as st

def music_player():
    st.subheader("🎵 Calm Music - Spotify")

    playlist_url = "https://open.spotify.com/embed/playlist/37i9dQZF1DX3Ogo9pFvBkY"

    st.components.v1.iframe(
        playlist_url,
        height=380,
    )