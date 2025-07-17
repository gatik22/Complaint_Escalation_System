import streamlit as st
from utils.backgrounds import set_background

class LandingPage:
    def __init__(self, background_path, logo_path=None):
        self.background_path = background_path
        self.logo_path = logo_path

    def set_background(self):
        set_background(self.background_path)

    def show(self):
        self.set_background()
        # If you want to show a logo, uncomment the next line and implement st.logo accordingly
        # st.logo(self.logo_path, size="large", width="20px")
        st.title("Welcome to Yash InfoCity Portal")
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                st.session_state.current_page = 'login'
                st.rerun()

        with col3:
            if st.button("Sign Up", type="secondary", use_container_width=True):
                st.session_state.current_page = 'signup'
                st.rerun()

if __name__ == "__main__":
    landing_page = LandingPage(
        background_path='images/FolSm0LWcAAGEsg.jpg',
        logo_path='images/logo.png'
    )
    landing_page.show()
