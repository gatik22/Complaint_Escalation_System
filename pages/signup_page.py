import streamlit as st

class SignupPage:
    def __init__(self, user_db):
        self.user_db = user_db

    def show(self):
        st.title("Welcome to Yash Info City")
        st.markdown("Please fill correct details for hassle-free access to services")

        with st.form("signup_form"):
            name = st.text_input("Enter name")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ['admin', 'resident'])

            # Create two columns for buttons side by side
            col1, col2 = st.columns(2)
            with col1:
                register = st.form_submit_button("Register")
            with col2:
                home = st.form_submit_button("Home")

        if register:
            if not name or not username or not password:
                st.error("All fields are required.")
            else:
                users = self.user_db.load_users()
                if any(u["username"].lower() == username.lower() for u in users):
                    st.error("Username already exists. Please choose another.")
                else:
                    new_user = {
                        "name": name,
                        "username": username,
                        "password": password,  # Hashing handled in save_user
                        "role": role
                    }
                    if self.user_db.save_user(new_user):
                        st.success("Registration successful! You can now log in.")
                    else:
                        st.error("Error saving user. Please try again.")

        if home:
            st.session_state.current_page = 'landing'
            st.rerun()

# For direct execution (optional)
if __name__ == "__main__":
    from utils.mysql_db import UserDB
    user_db = UserDB(
        host="localhost",
        user="root",
        password="root",
        database="yash_infocity"
    )
    page = SignupPage(user_db)
    page.show()
