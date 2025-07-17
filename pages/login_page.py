import streamlit as st
from utils.mysql_db import UserDB

class LoginPage:
    def __init__(self, user_db=None):
        # Accept UserDB instance from outside or create one here
        if user_db is None:
            self.user_db = UserDB(
                host="localhost",
                user="root",
                password="root",
                database="yash_infocity"
            )
        else:
            self.user_db = user_db

    def authenticate_user(self, username, password, role):
        """Check if username, password, and role match"""
        users = self.user_db.load_users()  # Call method on instance
        username = username.strip().lower()
        role = role.strip().lower()
        for user in users:
            user_name = user.get('username', '').strip().lower()
            user_role = user.get('role', '').strip().lower()
            user_password = user.get('password', '')
            if user_name == username and user_password == password and user_role == role:
                return True
        return False 

    def show(self):
        """Display the login page and take credentials from user"""
        st.title("Login")
        with st.form("login_form"):
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

                    if role == 'admin':
                        st.session_state.current_page = 'admin_dashboard'  
                    else:
                        st.session_state.current_page = 'resident_dashboard'
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

# For direct execution (optional, mostly for testing)
if __name__ == "__main__":
    page = LoginPage()
    page.show()
