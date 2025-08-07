import streamlit as st
from gtts import gTTS
import os
from PyPDF2 import PdfReader
import docx

def extract_text(file, filetype):
    if filetype == ".txt":
        return file.read().decode("utf-8")
    elif filetype == ".pdf":
        reader = PdfReader(file)
        return " ".join([page.extract_text() or "" for page in reader.pages])
    elif filetype == ".docx":
        # Need to save uploaded file temporarily
        with open("temp.docx", "wb") as f:
            f.write(file.read())
        doc = docx.Document("temp.docx")
        os.remove("temp.docx")
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return None

st.title("🗣️ File/Text to Speech Chatbot")

st.write("This bot can convert typed text or uploaded .txt/.pdf/.docx files into speech audio (MP3).")

input_type = st.radio("Choose input method:", ("Type text", "Upload file"))

if input_type == "Type text":
    user_text = st.text_area("Enter text to convert")
    process = st.button("Convert to Speech")
    if process and user_text.strip():
        tts = gTTS(user_text)
        tts.save("output.mp3")
        st.success("Audio generated!")
        with open("output.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
        os.remove("output.mp3")
elif input_type == "Upload file":
    uploaded_file = st.file_uploader("Upload a file (.txt/.pdf/.docx)",
                                     type=["txt", "pdf", "docx"])
    process = st.button("Convert to Speech")
    if process and uploaded_file is not None:
        suffix = os.path.splitext(uploaded_file.name)[-1].lower()
        file_text = extract_text(uploaded_file, suffix)
        if not file_text or not file_text.strip():
            st.error("Could not extract text from file or file is empty.")
        else:
            tts = gTTS(file_text)
            tts.save("output.mp3")
            st.success("Audio generated!")
            with open("output.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
            os.remove("output.mp3")

