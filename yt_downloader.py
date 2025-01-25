import streamlit as st
from pytube import YouTube
import os

def download_video(url, output_path=".", audio_only=False):
    try:
        yt = YouTube(url)
        if audio_only:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()
        
        # Download to a temporary directory
        file_path = stream.download(output_path)
        return file_path, yt.title
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None

# Streamlit UI
st.title("YouTube Video/Audio Downloader 🎥")

# Inputs
url = st.text_input("Paste YouTube URL:")
audio_only = st.checkbox("Download audio only (MP3)")
download_path = st.text_input("Save to folder (optional):", os.getcwd())

if st.button("Download"):
    if url:
        with st.spinner("Downloading..."):
            file_path, title = download_video(url, download_path, audio_only)
            if file_path:
                st.success(f"Downloaded: **{title}**")
                # Offer the file for download
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Save to device",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4" if not audio_only else "audio/mpeg"
                    )
                # Clean up temporary file (optional)
                os.remove(file_path)
    else:
        st.warning("Please enter a URL!")