# app.py
import io
import streamlit as st
from gtts import gTTS
from gtts.lang import tts_langs

st.set_page_config(page_title="Text to Speech", page_icon="🎙️", layout="centered")

st.title("🎙️ Text to Speech (gTTS + Streamlit)")
st.write("Type text, choose a language, and get an audio file.")

# Fetch available languages from gTTS
available_langs = tts_langs()  # dict: {"en": "English", "hi": "Hindi", ...}
lang_names = {v: k for k, v in available_langs.items()}  # reverse for user-friendly labels

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    language_label = st.selectbox(
        "Language",
        options=list(lang_names.keys()),
        index=list(lang_names.keys()).index("English") if "English" in lang_names else 0,
        help="Choose the language for speech synthesis."
    )
    slow = st.toggle("Slow speech", value=False, help="Enable slower, more articulated speech.")

# Main input
text = st.text_area(
    "Enter text to convert",
    placeholder="Type something…",
    height=150
)

# Generate audio
if st.button("Convert to audio"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        lang_code = lang_names[language_label]

        try:
            tts = gTTS(text=text, lang=lang_code, slow=slow)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)

            st.success("Audio generated successfully.")
            st.audio(buf, format="audio/mp3")

            st.download_button(
                label="Download MP3",
                data=buf,
                file_name="speech.mp3",
                mime="audio/mpeg"
            )
        except ValueError as e:
            st.error(f"Language not supported or invalid input: {e}")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Footer info
with st.expander("Supported languages"):
    st.write("This app uses gTTS languages. A few common ones:")
    st.code(
        "English (en), Hindi (hi), Bengali (bn), Telugu (te), Tamil (ta), Kannada (kn), Marathi (mr), Gujarati (gu), Urdu (ur), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Russian (ru), Japanese (ja), Korean (ko), Chinese (zh-CN)"
    )
    st.caption("The dropdown includes the full list detected from gTTS.")
