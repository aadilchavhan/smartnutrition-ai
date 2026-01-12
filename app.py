
import streamlit as st
import google.generativeai as genai

# ✅ Gemini API Setup
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    MODEL_NAME = "models/gemini-2.5-flash"
    st.session_state["gemini_model"] = MODEL_NAME
except Exception as e:
    st.error("❌ Gemini API key not found or invalid.")
    st.stop()

# ✅ Custom modules
import bim_calculator
import mealplanner
import home
import calorie_calculator
import sidebar

# ✅ Page config
st.set_page_config(
    page_title="SmartNutrition",
    page_icon="assets/app_logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ Navigation state
if "nav_page" not in st.session_state:
    st.session_state["nav_page"] = "Home"
if "last_nav_page" not in st.session_state:
    st.session_state["last_nav_page"] = "Home"
if "menu_open" not in st.session_state:
    st.session_state["menu_open"] = False

def toggle_menu():
    st.session_state["menu_open"] = not st.session_state["menu_open"]

if st.session_state["nav_page"] != st.session_state["last_nav_page"]:
    st.session_state["menu_open"] = False
    st.session_state["last_nav_page"] = st.session_state["nav_page"]
    st.rerun()

# ✅ Background + UI fixes
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #d4f1c4, #c4e8f1) !important;
        min-height: 100vh;
    }

    header[data-testid="stHeader"] {
        pointer-events: none !important;
        background: transparent !important;
        z-index: 0 !important;
    }
    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] a,
    [data-testid="stToolbar"] {
        pointer-events: auto !important;
        z-index: 2147483647 !important;
    }

    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    div[data-testid="stImage"] img {
        margin: 0 auto;
        display: block;
        max-width: 140px;
    }

    h1.main-title {
        font-size: clamp(24px, 5vw, 50px) !important;
        color: #2E7D32;
        text-align: center;
        margin: 0;
        padding: 0;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 4rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ✅ Header layout
col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
with col1:
    st.markdown('<div style="padding-top: 5px;">', unsafe_allow_html=True)
    st.button("☰", key="menu_btn", on_click=toggle_menu)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    try:
        st.image("assets/logo.jpg", use_container_width=True)
    except:
        pass
with col3:
    st.write("")

# ✅ Title
st.markdown('<h1 class="main-title">SmartNutrition AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #555;">Your Intelligent Nutrition Assistant</p>', unsafe_allow_html=True)
st.write("")

# ✅ Sidebar
sidebar.render_sidebar()

# ✅ Page router
page = st.session_state["nav_page"]
if page == "Home":
    home.show()
elif page == "Meal Planner":
    mealplanner.show()
elif page == "BMI Calculator":
    bim_calculator.show()
elif page == "Calorie Calculator":
    calorie_calculator.show()
