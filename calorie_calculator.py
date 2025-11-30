

import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# ✅ Voice transcription using Gemini directly
def recognize_audio(audio_bytes):
    try:
        model = genai.GenerativeModel(st.session_state["gemini_model"])
        response = model.generate_content([
            "You are a nutrition assistant. Transcribe this meal description clearly.",
            {"mime_type": "audio/webm", "data": audio_bytes}
        ])
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"

def show():
    st.subheader("🍎 Calorie Calculator")
    st.write("Describe your meal:")

    if "cal_input" not in st.session_state:
        st.session_state["cal_input"] = ""

    # ✅ No columns — better mobile tap area
    audio = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='cal_mic', just_once=True)

    if audio:
        transcription = recognize_audio(audio['bytes'])
        if transcription and not transcription.startswith("⚠️"):
            st.session_state["cal_input"] = transcription
            st.success(f"🗣 You said: {transcription}")
        else:
            st.warning(transcription or "No audio captured.")

    meal_input = st.text_area("Meal:", value=st.session_state["cal_input"])

    if st.button("🔍 Analyze Calories", use_container_width=True):
        if meal_input:
            with st.spinner("Calculating..."):
                try:
                    model = genai.GenerativeModel(st.session_state["gemini_model"])
                    prompt = f"Estimate calories for: {meal_input}. Format: Item - Kcal. Total at end."
                    res = model.generate_content(prompt)
                    st.markdown("### 🔢 Estimated Calories")
                    st.markdown(res.text)
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.warning("Please describe your meal first.")