# import streamlit as st

# def render_sidebar():
#     if st.session_state.get("menu_open", True):
#         with st.sidebar:
#             st.markdown("""
#             <style>
#             [data-testid="stSidebar"] > div:first-child {
#                 background: linear-gradient(to bottom, #c4e8f1, #d4f1c4) !important;
#                 height: 100%;
#                 padding: 0 12px;
#                 border: 2px solid #ffffff !important;
                
#             }
#             .custom-nav-button {
#                 display: block;
#                 width: 100%;
                
                
#                 border-radius: 0px;
#                 background-color: #ffffff10;
#                 color: #2E7D32;
#                 font-size: 17px;
#                 font-weight: 600;
#                 border: true;
#                 text-align: left;
#                 transition: all 0.2s ease-in-out;
#                 cursor: pointer;
#             }
#             .custom-nav-button:hover,
#             .custom-nav-button.active {
#                 background-color: #2E7D32;
#                 color: #ffffff;
#             }
#             </style>
#             """, unsafe_allow_html=True)

#             # Remove top margin too (or adjust if desired)
#             st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

#             nav_options = {
#                 "🏠 Home": "Home",
#                 "🍽️ Meal Planner": "Meal Planner",
#                 "📏 BMI Calculator": "BMI Calculator",
#                 "📊 Calorie Calculator": "Calorie Calculator"
#             }

#             if "nav_page" not in st.session_state:
#                 st.session_state["nav_page"] = "Home"

#             for label, page_key in nav_options.items():
#                 selected = st.session_state["nav_page"] == page_key
#                 btn_class = "custom-nav-button active" if selected else "custom-nav-button"

#                 st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
#                 if st.button(label, key=f"nav_{page_key}"):
#                     st.session_state["nav_page"] = page_key
#                 st.markdown('</div>', unsafe_allow_html=True)









import streamlit as st

def render_sidebar():
    # Only show sidebar if menu is open
    if st.session_state.get("menu_open", True):
        with st.sidebar:
            # ✅ Custom CSS for Sidebar Background & Buttons
            st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(to bottom, #c4e8f1, #d4f1c4) !important;
                border-right: 2px solid #ffffff;
            }
            /* Style for the buttons to look like menu items */
            div[data-testid="stVerticalBlock"] button {
                background-color: rgba(255, 255, 255, 0.5);
                border: 1px solid #2E7D32;
                color: #2E7D32;
                font-weight: 600;
                transition: all 0.2s;
            }
            div[data-testid="stVerticalBlock"] button:hover {
                background-color: #2E7D32;
                color: white;
                border-color: #2E7D32;
            }
            /* Highlight the active button */
            div[data-testid="stVerticalBlock"] button:focus {
                background-color: #2E7D32;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True)

            # Spacer
            st.write("")
            st.write("")

            # ✅ Navigation Options
            nav_options = {
                "🏠 Home": "Home",
                "🍽️ Meal Planner": "Meal Planner",
                "📏 BMI Calculator": "BMI Calculator",
                "📊 Calorie Calculator": "Calorie Calculator"
            }

            if "nav_page" not in st.session_state:
                st.session_state["nav_page"] = "Home"

            # ✅ Render Buttons
            for label, page_key in nav_options.items():
                # Highlight logic (Visual only, functional logic handles the rest)
                if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                    st.session_state["nav_page"] = page_key
                    st.rerun()  # 🔄 This forces the page to update immediately