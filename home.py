# import streamlit as st
# import google.generativeai as genai
# from PIL import Image
# import speech_recognition as sr
# import io

# import warnings

# warnings.filterwarnings("ignore", category=DeprecationWarning)

# # ✅ Gemini API configuration
# if "GEMINI_API_KEY" not in st.secrets:
#     st.error("❌ Gemini API key not found.")
# else:
#     genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# # ✅ Analyze image with Gemini Vision
# def analyze_meal_image(image_file, custom_prompt=None):
#     model = genai.GenerativeModel("gemini-2.5-flash")
#     base_prompt = """
# You are a professional nutritionist. Analyze this image and provide:
# 1. Dish name (or best guess)
# 2. Classification: Veg, Non-Veg, or Vegan
# 3. Estimated calorie range
# 4. Visible ingredients
# 5. Health benefits or drawbacks

# Format your response in bullet points.
# """
#     full_prompt = base_prompt + f"\n\nUser context: {custom_prompt}" if custom_prompt else base_prompt
#     image = Image.open(image_file)
#     response = model.generate_content([full_prompt, image])
#     return response.text if hasattr(response, "text") else str(response)

# # ✅ Voice transcription
# def get_voice_input():
#     recognizer = sr.Recognizer()
#     try:
#         with sr.Microphone() as source:
#             st.info("🎤 Listening... speak now.")
#             recognizer.adjust_for_ambient_noise(source, duration=1)
#             audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
#         return recognizer.recognize_google(audio)
#     except sr.WaitTimeoutError:
#         return "⚠️ No speech detected."
#     except sr.UnknownValueError:
#         return "⚠️ Could not understand audio."
#     except sr.RequestError:
#         return "⚠️ Speech recognition is unavailable."
#     except OSError:
#         return "⚠️ Microphone not found."

# def show_feedback(section="this"):
#     st.markdown("---")
#     st.markdown(f"**Was {section} helpful?**")

#     # Side-by-side buttons
#     col1, col2, col3 = st.columns([1, 1, 6])

#     with col1:
#         liked = st.button("👍 Yes", key=f"{section}_like")

#     with col2:
#         disliked = st.button("👎 No", key=f"{section}_dislike")

#     if liked:
#         st.success("Thanks for your feedback!")
#     elif disliked:
#         st.info("Thanks — we’ll use your feedback to improve.")

# # ✅ Main app
# def show(_=None):
#     st.markdown("""
#         <style>
#         .stApp {
#             background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
#             min-height: 100vh;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     input_mode = st.radio("Select input mode:", ("Text", "Voice", "Image"), horizontal=True)

#     # TEXT input
#     if input_mode == "Text":
#         user_text = st.text_input("💬 What's your food or nutrition question?",
#                                   placeholder="e.g. What’s a high-protein dinner?")
#         if st.button("🔍 Analyze Text"):
#             if user_text.strip():
#                 with st.spinner("Analyzing..."):
#                     try:
#                         model = genai.GenerativeModel("gemini-2.5-flash")
#                         response = model.generate_content(user_text)
#                         result = response.text if hasattr(response, "text") else str(response)
#                         st.markdown("### 💡 Result")
#                         st.markdown(result)
#                         show_feedback("this text answer")
#                     except Exception as e:
#                         st.error(f"⚠️ Error: {e}")
#             else:
#                 st.warning("Please enter a valid query.")

#     # VOICE input
#     elif input_mode == "Voice":
#         if "voice_text" not in st.session_state:
#             st.session_state.voice_text = ""

#         if st.button("🎙 Speak Now"):
#             voice_query = get_voice_input()
#             st.session_state.voice_text = voice_query
#             if "⚠️" in voice_query:
#                 st.warning(voice_query)
#             else:
#                 st.success(f"🗣 You said: {voice_query}")

#         if st.session_state.voice_text and st.button("🔍 Analyze Voice"):
#             with st.spinner("Analyzing your voice input..."):
#                 try:
#                     model = genai.GenerativeModel("gemini-2.5-flash")
#                     response = model.generate_content(st.session_state.voice_text)
#                     result = response.text if hasattr(response, "text") else str(response)
#                     st.markdown("### 💡 Result")
#                     st.markdown(result)
#                     show_feedback("this voice input")
#                 except Exception as e:
#                     st.error(f"⚠️  Error: {e}")

#     # IMAGE input
#     elif input_mode == "Image":
#         image_file = st.file_uploader("📷 Upload a meal image", type=["jpg", "jpeg", "png"])
#         custom_prompt = st.text_input("🧠 Optional context", placeholder="e.g. Good for weight loss?")

#         if image_file:
#             st.image(image_file, caption="Uploaded Meal", use_container_width=True)

#             if st.button("🔍 Analyze Image"):
#                 with st.spinner("Analyzing image..."):
#                     try:
#                         result = analyze_meal_image(image_file, custom_prompt)
#                         st.markdown("### 🍽  Nutrition Report")
#                         st.markdown(result)
#                         show_feedback("this image result")
#                     except Exception as e:
#                         st.error(f"⚠️  Vision error: {e}")

# # ✅ Run app
# if __name__ == "__main__":
#     show(None)








import streamlit as st
import google.generativeai as genai
from PIL import Image
import speech_recognition as sr
import io
from streamlit_mic_recorder import mic_recorder

# ✅ Gemini API configuration (Safely handled)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("❌ Gemini API key not found. Please check .streamlit/secrets.toml")

# ✅ Helper: Convert Audio Bytes to Text
def recognize_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_data = io.BytesIO(audio_bytes)
    audio_data.name = 'audio.wav'
    
    try:
        with sr.AudioFile(audio_data) as source:
            audio_content = recognizer.record(source)
        return recognizer.recognize_google(audio_content)
    except sr.UnknownValueError:
        return "⚠️ Could not understand audio."
    except sr.RequestError:
        return "⚠️ Speech service unavailable."
    except Exception as e:
        return f"⚠️ Error: {e}"

# ✅ Analyze image with Gemini Vision
def analyze_meal_image(image_file, custom_prompt=None):
    model = genai.GenerativeModel("gemini-2.5-flash")
    base_prompt = """
    You are a professional nutritionist. Analyze this image and provide:
    1. Dish name (or best guess)
    2. Classification: Veg, Non-Veg, or Vegan
    3. Estimated calorie range
    4. Visible ingredients
    5. Health benefits or drawbacks

    Format your response in bullet points.
    """
    full_prompt = base_prompt + f"\n\nUser context: {custom_prompt}" if custom_prompt else base_prompt
    image = Image.open(image_file)
    response = model.generate_content([full_prompt, image])
    return response.text

# ✅ Feedback Widget
def show_feedback(section="this"):
    st.markdown("---")
    st.markdown(f"**Was {section} helpful?**")
    col1, col2, col3 = st.columns([1, 1, 6])
    with col1:
        if st.button("👍 Yes", key=f"{section}_like"):
            st.success("Thanks for your feedback!")
    with col2:
        if st.button("👎 No", key=f"{section}_dislike"):
            st.info("Thanks — we’ll use your feedback to improve.")

# ✅ Main app
def show(_=None):
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
            min-height: 100vh;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("🏠 Home & Quick Analysis")
    input_mode = st.radio("Select input mode:", ("Text", "Voice", "Image"), horizontal=True)

    # ---------------- TEXT INPUT ----------------
    if input_mode == "Text":
        user_text = st.text_input("💬 What's your food or nutrition question?",
                                placeholder="e.g. What’s a high-protein dinner?")
        if st.button("🔍 Analyze Text"):
            if user_text.strip():
                with st.spinner("Analyzing..."):
                    try:
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(user_text)
                        st.markdown("### 💡 Result")
                        st.markdown(response.text)
                        show_feedback("this text answer")
                    except Exception as e:
                        st.error(f"⚠️ Error: {e}")
            else:
                st.warning("Please enter a valid query.")

    # ---------------- VOICE INPUT (WEB COMPATIBLE) ----------------
    elif input_mode == "Voice":
        st.info("Click the microphone to speak.")
        
        # Initialize session state for voice text
        if "voice_text" not in st.session_state:
            st.session_state.voice_text = ""

        # Web-compatible Microphone Recorder
        col_mic, col_status = st.columns([0.2, 0.8])
        with col_mic:
            audio = mic_recorder(
                start_prompt="🎤 Start",
                stop_prompt="🛑 Stop",
                key='home_mic',
                just_once=True
            )
        
        # Process Audio if captured
        if audio:
            transcription = recognize_audio(audio['bytes'])
            if "⚠️" not in transcription:
                st.session_state.voice_text = transcription
                st.success(f"🗣 You said: {transcription}")
            else:
                st.warning(transcription)

        # Show the analyze button if we have text
        if st.session_state.voice_text:
            if st.button("🔍 Analyze Voice Query"):
                with st.spinner("Asking AI..."):
                    try:
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(st.session_state.voice_text)
                        st.markdown("### 💡 Result")
                        st.markdown(response.text)
                        show_feedback("this voice input")
                    except Exception as e:
                        st.error(f"⚠️ Error: {e}")

    # ---------------- IMAGE INPUT ----------------
    elif input_mode == "Image":
        image_file = st.file_uploader("📷 Upload a meal image", type=["jpg", "jpeg", "png"])
        custom_prompt = st.text_input("🧠 Optional context", placeholder="e.g. Good for weight loss?")

        if image_file:
            st.image(image_file, caption="Uploaded Meal", width=300)

            if st.button("🔍 Analyze Image"):
                with st.spinner("Analyzing image..."):
                    try:
                        result = analyze_meal_image(image_file, custom_prompt)
                        st.markdown("### 🍽 Nutrition Report")
                        st.markdown(result)
                        show_feedback("this image result")
                    except Exception as e:
                        st.error(f"⚠️ Vision error: {e}")

# ✅ Run app logic
if __name__ == "__main__":
    show(None)