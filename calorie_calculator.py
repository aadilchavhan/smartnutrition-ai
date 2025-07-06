import streamlit as st
import google.generativeai as genai
import re

# ✅ Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

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

# ✅ Main Page UI — no header/branding here, handled by app.py
def show():
    st.markdown("# Calorie Calculator")
    st.markdown("Describe your meal below")

    meal_input = st.text_area("",  placeholder=" e.g. 2 boiled eggs, 1 cup rice, grilled chicken.", height=150)

    if st.button("🔍 Analyze Calories"):
        if meal_input.strip():
            with st.spinner("Analyzing your meal and estimating calories..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = f"""
Estimate the calories for the following meal. Respond in this format only:

Food Item - xxx kcal

Meal: {meal_input}
"""
                    response = model.generate_content(prompt)
                    text = response.text.strip()
                except Exception as e:
                    st.error(f" error: {e}")
                    return

            st.subheader("🧾 Calorie Estimate")
            st.code(text, language="markdown")

            total_kcal, breakdown = summarize_calories(text)
            st.subheader("🔍 Meal Breakdown")
            for item in breakdown:
                st.markdown(f"• {item}")

            st.markdown(f"### 🔢 Total Calories: `{total_kcal}` kcal")

            # ✅ Feedback
            st.markdown("---")
            st.markdown("**Was this calorie estimate helpful?**")
            col1, col2, _ = st.columns([1, 1, 4])
            with col1:
                if st.button("👍 Yes", key="cal_fb_like"):
                    st.success("Thanks for your feedback!")
            with col2:
                if st.button("👎 No", key="cal_fb_dislike"):
                    st.info("Thanks — we'll use your feedback to improve.")
        else:
            st.warning("Please enter a meal description first.")