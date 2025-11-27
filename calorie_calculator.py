# import streamlit as st
# import google.generativeai as genai
# import re

# # ✅ Configure Gemini
# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# # ✅ Extract calories from Gemini response
# def summarize_calories(response_text):
#     lines = response_text.strip().split('\n')
#     total_calories = 0
#     breakdown = []

#     for line in lines:
#         if '-' in line:
#             parts = line.split('-', 1)
#             food = parts[0].strip()
#             cal_info = parts[1].strip()
#             breakdown.append(f"{food}: {cal_info}")
#             match = re.search(r'(\d+)\s*kcal', cal_info, re.IGNORECASE)
#             if match:
#                 total_calories += int(match.group(1))

#     return total_calories, breakdown

# # ✅ Main Page UI — no header/branding here, handled by app.py
# def show():
#     st.markdown("# Calorie Calculator")
#     st.markdown("Describe your meal below")

#     meal_input = st.text_area("",  placeholder=" e.g. 2 boiled eggs, 1 cup rice, grilled chicken.", height=150)

#     if st.button("🔍 Analyze Calories"):
#         if meal_input.strip():
#             with st.spinner("Analyzing your meal and estimating calories..."):
#                 try:
#                     model = genai.GenerativeModel("gemini-2.5-flash")
#                     prompt = f"""
# Estimate the calories for the following meal. Respond in this format only:

# Food Item - xxx kcal

# Meal: {meal_input}
# """
#                     response = model.generate_content(prompt)
#                     text = response.text.strip()
#                 except Exception as e:
#                     st.error(f" error: {e}")
#                     return

#             st.subheader("🧾 Calorie Estimate")
#             st.code(text, language="markdown")

#             total_kcal, breakdown = summarize_calories(text)
#             st.subheader("🔍 Meal Breakdown")
#             for item in breakdown:
#                 st.markdown(f"• {item}")

#             st.markdown(f"### 🔢 Total Calories: `{total_kcal}` kcal")

#             # ✅ Feedback
#             st.markdown("---")
#             st.markdown("**Was this calorie estimate helpful?**")
#             col1, col2, _ = st.columns([1, 1, 4])
#             with col1:
#                 if st.button("👍 Yes", key="cal_fb_like"):
#                     st.success("Thanks for your feedback!")
#             with col2:
#                 if st.button("👎 No", key="cal_fb_dislike"):
#                     st.info("Thanks — we'll use your feedback to improve.")
#         else:
#             st.warning("Please enter a meal description first.")




import streamlit as st
import google.generativeai as genai
import re
import io
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

# ✅ Configure Gemini (Safely)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.warning("⚠️ GEMINI_API_KEY not found in secrets. Please set it up in .streamlit/secrets.toml")

# ✅ Function to convert Audio to Text
def recognize_audio(audio_bytes):
    r = sr.Recognizer()
    audio_data = io.BytesIO(audio_bytes)
    audio_data.name = 'audio.wav'
    
    with sr.AudioFile(audio_data) as source:
        audio_content = r.record(source)
        try:
            return r.recognize_google(audio_content)
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
            return ""
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return ""

# ✅ Extract calories from Gemini response
def summarize_calories(response_text):
    lines = response_text.strip().split('\n')
    total_calories = 0
    breakdown = []

    for line in lines:
        if '-' in line:
            parts = line.split('-', 1)
            food = parts[0].strip()
            cal_info = parts[1].strip()
            breakdown.append(f"{food}: {cal_info}")
            match = re.search(r'(\d+)\s*kcal', cal_info, re.IGNORECASE)
            if match:
                total_calories += int(match.group(1))

    return total_calories, breakdown

# ✅ Main Page UI
def show():
    st.markdown("# 🍎 Calorie Calculator")
    st.markdown("Describe your meal below (Type or Speak)")

    # Initialize session state for text input if not exists
    if "cal_input" not in st.session_state:
        st.session_state["cal_input"] = ""

    # 🎙️ Voice Input Section
    col_audio, col_text = st.columns([0.2, 0.8])
    with col_audio:
        st.write("Voice:")
        audio = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='cal_mic', just_once=True)
    
    # Process audio if recorded
    if audio:
        text = recognize_audio(audio['bytes'])
        if text:
            st.session_state["cal_input"] = text
            st.rerun() # Refresh to show text in box

    # Text Input Area (Synced with Voice)
    meal_input = st.text_area(
        "Meal Description", 
        value=st.session_state["cal_input"],
        placeholder="e.g. 2 boiled eggs, 1 cup rice, grilled chicken.", 
        height=150
    )
    
    # Update session state if user types manually
    if meal_input != st.session_state["cal_input"]:
        st.session_state["cal_input"] = meal_input

    # 🔍 Analyze Button
    if st.button("🔍 Analyze Calories"):
        if meal_input.strip():
            with st.spinner("Analyzing your meal and estimating calories..."):
                try:
                    # Using the latest Flash model
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    prompt = f"""
                    Estimate the calories for the following meal. Respond in this format only:

                    Food Item - xxx kcal

                    Meal: {meal_input}
                    """
                    response = model.generate_content(prompt)
                    text = response.text.strip()

                    st.subheader("🧾 Calorie Estimate")
                    st.code(text, language="markdown")

                    total_kcal, breakdown = summarize_calories(text)
                    
                    st.subheader("🔍 Meal Breakdown")
                    for item in breakdown:
                        st.markdown(f"• {item}")

                    st.markdown(f"### 🔢 Total Calories: `{total_kcal}` kcal")

                    # ✅ Feedback
                    st.markdown("---")
                    st.markdown("**Was this helpful?**")
                    c1, c2, _ = st.columns([1, 1, 4])
                    with c1:
                        if st.button("👍 Yes", key="cal_like"): st.success("Thanks!")
                    with c2:
                        if st.button("👎 No", key="cal_dislike"): st.info("Noted.")

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter or speak a meal description first.")

