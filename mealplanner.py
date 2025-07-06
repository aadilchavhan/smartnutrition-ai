import streamlit as st
import speech_recognition as sr
import google.generativeai as genai

# ✅ Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ Voice Recognition
def get_voice_input():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... please speak clearly.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
    except sr.WaitTimeoutError:
        return "No speech detected."
    except OSError:
        return "Microphone unavailable or not found."

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, could not understand your voice."
    except sr.RequestError:
        return "Speech recognition service error."

# ✅ Main Page Logic
def show():
    st.title("🍽️ SmartNutrition Meal Planner")

    # 📝 Text Input Only
    st.markdown("### Describe your goal or concern:")

    if 'user_text' not in st.session_state:
        st.session_state.user_text = ""

    st.session_state.user_text = st.text_area(" ", value=st.session_state.user_text, height=150, key="user_text_area",placeholder="e.g. I want to build muscle and avoid sugary foods.")

    # ✅ Goal and Calorie Preference
    goal = st.radio("Select your goal:", ["Gain Weight", "Lose Weight", "Balanced Diet"], horizontal=True)

    calorie_option = st.selectbox(
        "Calorie Preference:",
        ["None", "Low Calorie", "Moderate Calorie", "High Calorie"]
    )

    # ✅ Age, Height, Weight
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.selectbox("Age", list(range(10, 81)), index=20)
    with col2:
        height = st.selectbox("Height (cm)", list(range(120, 221)), index=30)
    with col3:
        weight = st.selectbox("Weight (kg)", list(range(30, 151)), index=20)

    # ✅ Diet + Allergy Preferences
    diet_pref = st.selectbox("Diet Preference:", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    restriction = st.selectbox("Allergies or Restrictions:", ["None", "Lactose Intolerance", "Gluten-Free"])

    # ✅ Analyze Button
    if st.button("🔍 Analyze"):
        st.subheader("📊 Your Personalized Meal Plan")
        st.markdown(f"**Goal:** {goal}")
        st.markdown(f"**Calorie Preference:** {calorie_option}")
        st.markdown(f"**Age:** {age} years")
        st.markdown(f"**Height:** {height} cm")
        st.markdown(f"**Weight:** {weight} kg")
        st.markdown(f"**Diet Preference:** {diet_pref}")
        st.markdown(f"**Restriction:** {restriction}")
        st.markdown(f"**Concern:** {st.session_state.user_text.strip() or 'None'}")

        prompt = f"""
Create a 7-day Indian meal plan in markdown table format.
Goal: {goal}
Calorie Preference: {calorie_option}
Age: {age}, Height: {height} cm, Weight: {weight} kg
Diet: {diet_pref}, Restriction: {restriction}
Concern: {st.session_state.user_text.strip() or "None"}

Format the response as a markdown table with columns: Day, Breakfast, Lunch, Dinner.
"""

        with st.spinner("Generating your meal plan..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                st.markdown(response.text)

                # ✅ Feedback Widget
                st.markdown("---")
                st.markdown("**Was this meal plan helpful?**")
                fb1, fb2, _ = st.columns([1, 1, 6])
                with fb1:
                    if st.button("👍 Yes", key="mealplan_like"):
                        st.success("Thanks for your feedback!")
                with fb2:
                    if st.button("👎 No", key="mealplan_dislike"):
                        st.info("Thanks — we'll use your feedback to improve.")
            except Exception as e:
                st.error(f"Gemini error: {e}")

# ✅ Standalone run
if __name__ == "__main__":
    show()