import streamlit as st

def render_sidebar():
    if st.session_state.get("menu_open", True):
        with st.sidebar:
            st.markdown("""
            <style>
            [data-testid="stSidebar"] > div:first-child {
                background: linear-gradient(to bottom, #c4e8f1, #d4f1c4) !important;
                height: 100%;
                padding: 0 12px;
                border: 2px solid #ffffff !important;
                
            }
            .custom-nav-button {
                display: block;
                width: 100%;
                
                
                border-radius: 0px;
                background-color: #ffffff10;
                color: #2E7D32;
                font-size: 17px;
                font-weight: 600;
                border: true;
                text-align: left;
                transition: all 0.2s ease-in-out;
                cursor: pointer;
            }
            .custom-nav-button:hover,
            .custom-nav-button.active {
                background-color: #2E7D32;
                color: #ffffff;
            }
            </style>
            """, unsafe_allow_html=True)

            # Remove top margin too (or adjust if desired)
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

            nav_options = {
                "🏠 Home": "Home",
                "🍽️ Meal Planner": "Meal Planner",
                "📏 BMI Calculator": "BMI Calculator",
                "📊 Calorie Calculator": "Calorie Calculator"
            }

            if "nav_page" not in st.session_state:
                st.session_state["nav_page"] = "Home"

            for label, page_key in nav_options.items():
                selected = st.session_state["nav_page"] == page_key
                btn_class = "custom-nav-button active" if selected else "custom-nav-button"

                st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
                if st.button(label, key=f"nav_{page_key}"):
                    st.session_state["nav_page"] = page_key
                st.markdown('</div>', unsafe_allow_html=True)