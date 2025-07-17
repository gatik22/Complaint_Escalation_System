import streamlit as st
from utils.mysql_db import UserDB, ComplaintDB
from components.profile_management import ProfileManagement
import os

class AdminDashboard:
    def __init__(self, user_db: UserDB, complaint_db: ComplaintDB, username: str):
        self.user_db = user_db
        self.complaint_db = complaint_db
        self.username = username

    def logout(self):
        st.session_state.logged_in = False if 'logged_in' in st.session_state else None
        st.session_state.username = None if 'username' in st.session_state else None
        st.session_state.user_role = None if 'user_role' in st.session_state else None
        st.session_state.current_page = 'landing'  # Or your landing page name
        st.success("Logged out successfully.")
        st.rerun()

    def show_complaints(self):
        st.subheader("All Complaints")
        complaints = self.complaint_db.fetch_complaints()
        if not complaints:
            st.info("No complaints found.")
            return

        # Get unique departments for filter dropdown
        departments = sorted({c['department'] for c in complaints if c.get('department')})
        departments.insert(0, "All")
        selected_dept = st.selectbox("Filter by Department", departments)

        if selected_dept != "All":
            filtered_complaints = [c for c in complaints if c.get('department') == selected_dept]
        else:
            filtered_complaints = complaints

        for c in filtered_complaints:
            with st.expander(f"Complaint #{c.get('id')} from {c.get('username', 'Unknown')}"):
                st.write(f"**Complaint:** {c.get('complaint', 'No details')}")
                st.write(f"**Urgency:** {c.get('urgency', 'N/A')}")
                st.write(f"**Department:** {c.get('department', 'N/A')}")
                st.write(f"**Status:** {c.get('status', 'Open')}")
                st.write(f"**Filed At:** {str(c.get('created_at', 'N/A'))}")

                # === Display attached photo if exists ===
                photo_path = c.get('photo_path')
                if photo_path:
                    st.write(f"Photo path: `{photo_path}`")  # Debug info to confirm path
                    if os.path.isfile(photo_path):
                        st.image(photo_path, caption="Attached Photo", use_container_width=True)
                    else:
                        st.warning(f"Image file not found: {photo_path}")
                else:
                    st.write("_No photo attached to this complaint._")

                # Status update logic
                status_options = ["Open", "In Process", "Resolved", "Closed"]
                current_status = c.get('status', 'Open')
                if current_status not in status_options:
                    current_status = "Open"

                status = st.selectbox(
                    "Set Status",
                    status_options,
                    index=status_options.index(current_status),
                    key=f"status_{c.get('id')}"
                )
                if status != current_status:
                    if self.complaint_db.update_status(c.get('id'), status):
                        st.success("Status updated.")
                        st.rerun()
                    else:
                        st.error("Failed to update status.")

                # Delete button
                if st.button("Delete Complaint", key=f"del_{c.get('id')}"):
                    if self.complaint_db.delete_complaint(c.get('id')):
                        st.warning("Complaint deleted.")
                        st.rerun()
                    else:
                        st.error("Failed to delete complaint.")

        st.markdown("---")

    def show_profile(self):
        st.subheader("My Profile")
        profile = ProfileManagement(self.user_db, self.username)
        profile.show()

    def show(self):
        # Header and logout button layout
        col1, col2 = st.columns([9, 4])
        with col1:
            st.title("Admin Dashboard")
        with col2:
            if st.button("Logout"):
                self.logout()

        # Tab for switching views
        tab = st.radio("Select View", ["Complaints", "My Profile"])

        if tab == "Complaints":
            self.show_complaints()
        elif tab == "My Profile":
            self.show_profile()

def main():
    st.title("Login Simulation for Admin")

    # Simulate login inputs
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        # Simple dummy credential check — replace with real authentication
        if username_input == "admin1" and password_input == "root":
            st.success("Logged in successfully as admin!")

            # Create DB instances with your connection params
            user_db = UserDB(host="localhost", user="root", password="root", database="yash_infocity")
            complaint_db = ComplaintDB(host="localhost", user="root", password="root", database="yash_infocity")

            # Show admin dashboard passing logged-in username
            admin_dashboard = AdminDashboard(user_db, complaint_db, username_input)
            admin_dashboard.show()
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()
