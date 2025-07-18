import streamlit as st
from utils.backgrounds import set_background

class SignupPage:
    def __init__(self, user_db):
        self.user_db = user_db
    
    def show(self):
        set_background("static/vertical-shot-modern-white-building-with-light-coming-out-from-one-big-balcony-windows.jpg")  # 
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-title {
            text-align: center;
            color: #ffffff;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #f0f0f0;
            font-size: 1.1rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
        }
        .home-button-container {
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 999;
        }
        
        .stButton > button {
            width: 100%;
            background-color: #2E86AB;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #1a5a7a;
        }
        .home-btn {
            background-color: rgba(108, 117, 125, 0.9) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 0.3rem 1rem !important;
            font-size: 0.9rem !important;
            backdrop-filter: blur(5px) !important;
        }
        .home-btn:hover {
            background-color: rgba(90, 98, 104, 0.9) !important;
        }
        /* Form content styling for better visibility */
        .signup-container h3 {
            color: #2E86AB;
            margin-bottom: 1.5rem;
            font-weight: bold;
        }
        .signup-container label {
            color: #333;
            font-weight: 500;
        }
        .signup-container .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.8);
            border: 1px solid #ddd;
            color: #333;
        }
        .signup-container .stSelectbox > div > div > div {
            background-color: rgba(255, 255, 255, 0.8);
            border: 1px solid #ddd;
            color: #333;
        }
        
        </style>
        """, unsafe_allow_html=True)
        
        # Home button positioned in top-left corner
        with st.container():
            st.markdown('<div class="home-button-container">', unsafe_allow_html=True)
            if st.button("← Home", key="home_btn", help="Go back to homepage"):
                st.session_state.current_page = 'landing'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Header section
        st.markdown('<h1 class="main-title">Welcome to Yash Info City</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Please fill correct details for hassle-free access to services</p>', unsafe_allow_html=True)
        
        
        # Center the form with increased width
        col1, col2, col3 = st.columns([0.5, 3, 0.5])
        
        with col2:
            with st.container():
                st.markdown('<div class="signup-container">', unsafe_allow_html=True)
                
                with st.form("signup_form", clear_on_submit=True):
                    st.markdown("### Create Your Account")
                    
                    # Form fields with better spacing
                    name = st.text_input("Full Name", placeholder="Enter your full name", help="Your display name")
                    username = st.text_input("Username", placeholder="Choose a unique username", help="This will be used for login")
                    password = st.text_input("Password", type="password", placeholder="Create a secure password", help="Minimum 6 characters recommended")
                    role = st.selectbox("Role", ['admin', 'resident'], help="Select your role in the community")
                    
                    # Add some spacing before button
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Registration button (full width)
                    register = st.form_submit_button("Create Account", type="primary")
                    
                    # Handle registration
                    if register:
                        if not name or not username or not password:
                            st.error("All fields are required.")
                        elif len(password) < 6:
                            st.error("Password must be at least 6 characters long.")
                        else:
                            # Show loading spinner
                            with st.spinner('Creating your account...'):
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
                                        # Optional: Add a slight delay before redirecting
                                        st.balloons()
                                    else:
                                        st.error("Error saving user. Please try again.")
                
                st.markdown('</div>', unsafe_allow_html=True)

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