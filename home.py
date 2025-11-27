import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# ✅ Gemini API configuration (Safely handled)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("❌ Gemini API key not found. Please check .streamlit/secrets.toml")

# ✅ Helper: Convert Audio Bytes to Text using Gemini
def recognize_audio(audio_bytes):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content([
            "You are a transcription expert. Convert this audio to text.",
            audio_bytes
        ])
        return response.text
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

    # ---------------- VOICE INPUT ----------------
    elif input_mode == "Voice":
        st.info("Click the microphone to speak.")

        if "voice_text" not in st.session_state:
            st.session_state.voice_text = ""

        col_mic, col_status = st.columns([0.2, 0.8])
        with col_mic:
            audio = mic_recorder(
                start_prompt="🎤 Start",
                stop_prompt="🛑 Stop",
                key='home_mic',
                just_once=True
            )

        if audio:
            transcription = recognize_audio(audio['bytes'])
            if "⚠️" not in transcription:
                st.session_state.voice_text = transcription
                st.success(f"🗣 You said: {transcription}")
            else:
                st.warning(transcription)

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