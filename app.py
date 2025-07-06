import streamlit as st
import bim_calculator
import mealplanner
import home
import calorie_calculator
import sidebar 

import google.generativeai as genai
import os


# ✅ Page Config
st.set_page_config(
    page_title="SmartNutrition",
    page_icon="assets/app_logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Global Styling
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(to bottom, #d4f1c4, #c4e8f1) !important;
    min-height: 100vh;
}
[data-testid="stHeader"] {
    background: linear-gradient(to bottom, #d4f1c4, #c4e8f1) !important;
}
section.main > div {
    background: transparent !important;
}
.sidebar-btn {
    display: block;
    width: 100%;
    padding: 12px 0;
    margin: 10px 0;
    background: #e0f2f1;
    color: #2E7D32;
    border: 2px solid #2E7D32;
    border-radius: 8px;
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
    text-decoration: none;
}
.sidebar-btn.selected, .sidebar-btn:hover {
    background: #2E7D32;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# ✅ Header Area: ☰ Menu + Logo + Title
col1, col2, col3 = st.columns([0.06, 0.14, 0.84])

with col1:
    st.markdown('<div style="padding-top: 18px;">', unsafe_allow_html=True)
    if st.button("☰", key="menu_btn"):
        st.session_state["menu_open"] = not st.session_state.get("menu_open", True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.image("assets/logo.jpg", width=200)

with col3:
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center; padding-top: 8px;">
        <h1 style="font-size: 60px; color: #2E7D32; margin-bottom: 5px;">SmartNutrition AI</h1>
        <p style="font-size: 27px; color: #555; margin-top: -5px;">Your Intelligent Nutrition Assistant</p>
    </div>
    """, unsafe_allow_html=True)

# ✅ Render Sidebar
sidebar.render_sidebar()

# ✅ Page Router
page = st.session_state.get("nav_page", "Home")

if page == "Home":
    home.show()
elif page == "Meal Planner":
    mealplanner.show()
elif page == "BMI Calculator":
    bim_calculator.show()
elif page == "Calorie Calculator":
    calorie_calculator.show()