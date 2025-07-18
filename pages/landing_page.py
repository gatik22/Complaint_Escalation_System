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

        # Add some top spacing
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Show logo centered on top if provided
        if self.logo_path:
            st.image(self.logo_path, width=150, use_column_width=False)

        # Title with custom style to improve visibility on background
        st.markdown(
            """
            <h1 style='text-align: center; color: white; font-family: Arial, sans-serif;'>
                Welcome to Yash InfoCity Portal
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Button container - center buttons horizontally using columns
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button("Login", key="login", use_container_width=True,type="primary"):
                st.session_state.current_page = 'login'
                st.rerun()

        with col3:
            if st.button("Sign Up", key="signup", use_container_width=True):
                st.session_state.current_page = 'signup'
                st.rerun()

        # Add some bottom spacing
        st.markdown("<br><br>", unsafe_allow_html=True)



if __name__ == "__main__":
    landing_page = LandingPage(
        background_path='images/FolSm0LWcAAGEsg.jpg',
        logo_path='images/logo.png'
    )
    landing_page.show()
