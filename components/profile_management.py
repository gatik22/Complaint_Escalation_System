import streamlit as st

class ProfileManagement:
    def __init__(self, user_db, username):
        self.user_db = user_db
        self.username = username

    def show(self):
        st.header("My Profile")

        user = self.user_db.get_user_by_username(self.username)
        if not user:
            st.error("Unable to load your profile.")
            return

        # Show only name (assuming at least name exists)
        name = st.text_input("Name", value=user.get("name", ""))

        if st.button("Update Profile"):
            success = self.user_db.update_user_profile(self.username, name)
            if success:
                st.success("Your profile was updated.")
            else:
                st.error("Update failed.")

        st.markdown("---")
        st.subheader("Change Password")

        current_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password", type="password")
        confirm_pw = st.text_input("Confirm New Password", type="password")

        if st.button("Update Password"):
            if not all([current_pw, new_pw, confirm_pw]):
                st.warning("Please fill in all password fields.")
            elif new_pw != confirm_pw:
                st.error("New passwords do not match.")
            elif current_pw != user.get('password'):
                st.error("Incorrect current password.")
            else:
                updated = self.user_db.update_user_password(self.username, new_pw)
                if updated:
                    st.success("Password updated successfully.")
                else:
                    st.error("Error updating password.")
