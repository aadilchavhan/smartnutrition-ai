import streamlit as st

# ✅ Convert inches to centimeters
def inches_to_cm(inches):
    return inches * 2.54

# ✅ Inline unit, height & weight input block
def get_inputs_inline():
    col1, col2, col3 = st.columns([1.2, 1, 1.2])

    with col1:
        unit = st.selectbox("Height Unit", ("Centimeters (cm)", "Inches (in)"))

    with col2:
        if unit == "Centimeters (cm)":
            heights_cm = list(range(100, 221))  # 100–220 cm
            height = st.selectbox("Height", heights_cm, index=70)
        else:
            heights_in = list(range(40, 88))  # 40–87 in
            height_in = st.selectbox("Height", heights_in, index=27)
            height = inches_to_cm(height_in)

    with col3:
        weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=65.0)

    return height, weight

# ✅ BMI Calculation & Classification
def calculate_bmi(weight_kg, height_cm):
    if height_cm == 0:
        return 0, "Invalid"
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    return round(bmi, 2), category

# ✅ Feedback widget
def show_feedback(section="this section"):
    st.markdown("---")
    st.markdown(f"**Was {section} helpful?**")
    col1, col2, _ = st.columns([1, 1, 6])
    with col1:
        liked = st.button("👍 Yes", key=f"{section}_like")
    with col2:
        disliked = st.button("👎 No", key=f"{section}_dislike")

    if liked:
        st.success("Thanks for your feedback!")
    elif disliked:
        st.info("Thanks — we’ll use your feedback to improve.")

# ✅ Main BMI Calculator UI
def show():
    st.title("📏 BMI Calculator")

    height, weight = get_inputs_inline()

    if st.button("🧮 Calculate BMI"):
        bmi, category = calculate_bmi(weight, height)

        st.subheader("📊 Result")
        st.markdown(f"**BMI:** `{bmi}`")
        st.markdown(f"**Category:** `{category}`")

        emoji = {
            "Underweight": "🍃",
            "Normal weight": "✅",
            "Overweight": "⚠️",
            "Obese": "🔥"
        }
        st.markdown(f"{emoji.get(category, '')} You are classified as **{category}**.")

        show_feedback("BMI calculator")

# ✅ Run if standalone
if __name__ == "__main__":
    show()