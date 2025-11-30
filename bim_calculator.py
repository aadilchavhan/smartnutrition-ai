


import streamlit as st

def inches_to_cm(inches):
    return inches * 2.54

def calculate_bmi(weight_kg, height_cm):
    if height_cm == 0:
        return 0, "Invalid"
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
        color = "orange"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
        color = "green"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        color = "amber"
    else:
        category = "Obese"
        color = "red"
    return round(bmi, 2), category, color

def show():
    st.subheader("📏 BMI Calculator")

    col1, col2 = st.columns(2)
    with col1:
        unit = st.selectbox("Height Unit", ("Centimeters (cm)", "Inches (in)"))

    with col2:
        if unit == "Centimeters (cm)":
            height = st.number_input("Height (cm)", 100, 250, 170)
        else:
            height_in = st.number_input("Height (in)", 40, 100, 67)
            height = inches_to_cm(height_in)

    weight = st.number_input("Weight (kg)", 20, 200, 65)

    if st.button("🧮 Calculate BMI", use_container_width=True):
        bmi, category, color = calculate_bmi(weight, height)
        st.markdown(f"<div style='color:{color}; font-size:1.2rem;'>✅ BMI: {bmi} ({category})</div>", unsafe_allow_html=True)