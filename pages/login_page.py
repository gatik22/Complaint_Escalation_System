import streamlit as st
from utils.mysql_db import UserDB
from utils.backgrounds import set_background

class LoginPage:
    def __init__(self, user_db=None):
        self.user_db = user_db or UserDB(
            host="localhost",
            user="root",
            password="root",
            database="yash_infocity"
        )

    def authenticate_user(self, username, password, role):
        users = self.user_db.load_users()
        for user in users:
            if (user.get('username', '').strip().lower() == username.strip().lower() and
                user.get('password', '') == password and
                user.get('role', '').strip().lower() == role.strip().lower()):
                return True
        return False

    def show(self):
        set_background("static/low-angle-shot-tall-apartment-buildings-dark-sky.jpg")

        # CSS to target the native Streamlit form container
        st.markdown("""
        <style>
            /* Center the main page contents */
            section.main > div {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                height: 100vh !important;
            }

            /* Style the Streamlit form block */
            div[data-testid="stForm"] {
                background: rgba(255, 255, 255, 0.15) !important;
                border-radius: 16px !important;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                padding: 2.5rem !important;
                width: 704px;
                margin: auto;
            }
        </style>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.title("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.radio("Login as:", ['resident', 'admin'])
            login_button = st.form_submit_button("Login")

        if login_button:
            if not username or not password:
                st.error("Please enter both Username and password")
            else:
                if self.authenticate_user(username, password, role):
                    st.session_state.logged_in = True
                    st.session_state.user_role = role
                    st.session_state.username = username
                    st.session_state.current_page = (
                        'admin_dashboard' if role == 'admin' else 'resident_dashboard'
                    )
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
# For direct execution (optional, mostly for testing)
if __name__ == "__main__":
    page = LoginPage()
    page.show()