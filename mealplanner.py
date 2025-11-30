

import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# ✅ Voice transcription using Gemini
def recognize_audio(audio_bytes):
    try:
        model = genai.GenerativeModel(st.session_state["gemini_model"])
        res = model.generate_content([
            "Convert audio to text clearly.",
            {"mime_type": "audio/webm", "data": audio_bytes}
        ])
        return res.text
    except Exception as e:
        return f"⚠️ Error: {e}"

# ✅ Image analysis using Gemini Vision
def analyze_meal_image(img, prompt=""):
    try:
        model = genai.GenerativeModel(st.session_state["gemini_model"])
        return model.generate_content([f"Analyze meal. {prompt}", img]).text
    except Exception as e:
        return f"⚠️ Vision error: {e}"

def show(_=None):
    # ✅ Main title App.py me hai, yahan sirf subheader
    st.subheader("🏠 Home & Quick Analysis")

    input_mode = st.radio("Input Mode:", ("Text", "Voice", "Image"), horizontal=True)

    # ---------------- TEXT INPUT ----------------
    if input_mode == "Text":
        q = st.text_input("Ask about nutrition:", placeholder="e.g. Is paneer healthy?")
        if st.button("🔍 Analyze", use_container_width=True):
            if q.strip():
                with st.spinner("Analyzing..."):
                    try:
                        model = genai.GenerativeModel(st.session_state["gemini_model"])
                        st.markdown(model.generate_content(q).text)
                    except Exception as e:
                        st.error(f"⚠️ Error: {e}")
            else:
                st.warning("Please enter a valid query.")

    # ---------------- VOICE INPUT ----------------
    elif input_mode == "Voice":
        st.info("Tap mic to speak.")
        audio = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='home_mic', just_once=True)

        if audio:
            text = recognize_audio(audio['bytes'])
            if text and not text.startswith("⚠️"):
                st.success(f"🗣 You said: {text}")
                if st.button("Analyze Voice", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        try:
                            model = genai.GenerativeModel(st.session_state["gemini_model"])
                            st.markdown(model.generate_content(text).text)
                        except Exception as e:
                            st.error(f"⚠️ Error: {e}")
            else:
                st.warning(text or "No audio captured.")

    # ---------------- IMAGE INPUT ----------------
    elif input_mode == "Image":
        img = st.file_uploader("Upload Image", type=["jpg", "png"])
        if img:
            st.image(img, use_container_width=True)
            if st.button("Analyze Image", use_container_width=True):
                with st.spinner("Scanning..."):
                    result = analyze_meal_image(Image.open(img))
                    st.markdown(result)