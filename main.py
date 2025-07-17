import streamlit as st

from pages.landing_page import LandingPage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.admin_dashboard import AdminDashboard
from pages.resident_dashboard import ResidentDashboard
from utils.mysql_db import UserDB, ComplaintDB  

# Initialize DB connections once
user_db = UserDB(
    host="localhost",
    user="root",
    password="root",
    database="yash_infocity"
)
complaint_db = ComplaintDB(
    host="localhost",
    user="root",
    password="root",
    database="yash_infocity"
)

# Initialize session state variables if not present
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'landing'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None

def main():
    page = None

    if st.session_state.current_page == 'landing':
        page = LandingPage(background_path='static/FolSm0LWcAAGEsg.jpg')
    elif st.session_state.current_page == 'login':
        page = LoginPage(user_db)  # Pass user_db instance
    elif st.session_state.current_page == 'signup':
        page = SignupPage(user_db)  # Pass user_db instance
    elif st.session_state.current_page == 'admin_dashboard':
        page = AdminDashboard(user_db, complaint_db, st.session_state.username)
    elif st.session_state.current_page == 'resident_dashboard':
        # ResidentDashboard expects complaint_db and username
        page = ResidentDashboard(complaint_db, st.session_state.username)
    else:
        st.session_state.current_page = 'landing'
        st.rerun()

    if page:
        page.show()

def go_to_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if __name__ == "__main__":
    try:
        main()
    finally:
        # Close DB connections on app exit
        user_db.close()
        complaint_db.close()
