
import streamlit as st

def set_page(page_name: str):
    """Update navigation state and close menu."""
    st.session_state["nav_page"] = page_name
    st.session_state["menu_open"] = False

def render_sidebar():
    # 1. Agar Menu Open nahi hai, to yahi ruk jao
    if not st.session_state.get("menu_open", False):
        return

    # 2. CSS STYLING (Sidebar Drawer)
    st.markdown("""
    <style>
        /* --- OVERLAY (Dim Background) --- */
        .sidebar-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999990;
            backdrop-filter: blur(3px);
        }

        /* --- SIDEBAR CONTAINER --- */
        div[data-testid="stVerticalBlock"]:has(div#my-sidebar-content) {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 280px !important;
            height: 100vh !important;
            background-color: #ffffff !important;
            z-index: 999999 !important;
            padding: 20px !important;
            padding-top: 60px !important;
            box-shadow: 4px 0 15px rgba(0,0,0,0.2) !important;
            border-right: 1px solid #ddd !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
            animation: slideIn 0.3s ease-in-out;
        }

        @keyframes slideIn {
            from { left: -300px; opacity: 0; }
            to { left: 0; opacity: 1; }
        }

        /* --- BUTTON STYLING --- */
        div[data-testid="stVerticalBlock"]:has(div#my-sidebar-content) button {
            width: 100% !important;
            text-align: left !important;
            border: 1px solid #eee !important;
            background: #ffffff !important;
            color: #333 !important;
            padding: 12px !important;
            border-radius: 8px !important;
            margin-bottom: 5px !important;
            font-size: 14px !important;
        }

        div[data-testid="stVerticalBlock"]:has(div#my-sidebar-content) button:hover {
            background-color: #f1f8e9 !important;
            color: #2E7D32 !important;
            border-color: #2E7D32 !important;
        }

        /* --- CLOSE BUTTON (Red & Bottom) --- */
        div[data-testid="stVerticalBlock"]:has(div#my-sidebar-content) button:last-of-type {
            background-color: #ffebee !important;
            color: #c62828 !important;
            border: 1px solid #ffcdd2 !important;
            text-align: center !important;
            font-weight: bold !important;
            margin-top: auto !important;
            margin-bottom: 20px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 3. OVERLAY DIV
    st.markdown('<div class="sidebar-overlay"></div>', unsafe_allow_html=True)

    # 4. SIDEBAR CONTENT
    with st.container():
        # Unique ID for CSS targeting
        st.markdown('<div id="my-sidebar-content"></div>', unsafe_allow_html=True)

        st.markdown("### 📋 Navigation")

        if st.button("🏠 Home", key="sb_home"):
            set_page("Home")
            st.rerun()

        if st.button("🍽️ Meal Planner", key="sb_meal"):
            set_page("Meal Planner")
            st.rerun()

        if st.button("📏 BMI Calculator", key="sb_bmi"):
            set_page("BMI Calculator")
            st.rerun()

        if st.button("🍎 Calorie Calculator", key="sb_cal"):
            set_page("Calorie Calculator")
            st.rerun()

        # Spacer to push Close button down
        st.markdown('<div style="flex-grow: 1;"></div>', unsafe_allow_html=True)

        # Close Button
        if st.button("✖ Close Menu", key="close_sidebar_btn"):
            st.session_state["menu_open"] = False
            st.rerun()

        # Footer
        st.markdown(
            "<div style='text-align:center; color:grey; font-size:12px;'>SmartNutrition AI v1.0</div>",
            unsafe_allow_html=True
        )