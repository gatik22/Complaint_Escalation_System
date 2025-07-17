import streamlit as st
from components.complaints_form import ComplaintForm
from components.profile_management import ProfileManagement
from utils.mysql_db import ComplaintDB

class ResidentDashboard:
    def __init__(self, db: ComplaintDB, username):
        self.db = db
        self.username = username

    def load_user_complaints(self):
        """Fetch complaints for the logged-in user from the database."""
        if not self.username:
            return []
        with self.db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM complaints WHERE username=%s ORDER BY created_at DESC",
                (self.username,)
            )
            return cursor.fetchall()

    def show(self):
        st.title("Resident Portal")

        if not self.username:
            st.error("You must be logged in to submit a complaint.")
            return

    # Navigation radio to switch views
        choice = st.radio("Select Option", ["Submit Complaint", "View Past Complaints", "My Profile"])

        if choice == "Submit Complaint":
            form = ComplaintForm(self.username, self.db)
            form.show()

        elif choice == "View Past Complaints":
            st.subheader("Your Past Complaints")
            complaints = self.load_user_complaints()
            if complaints:
                for idx, complaint in enumerate(complaints, 1):
                    st.markdown(f"**Complaint #{idx}:**")
                    st.write(f"- **Date:** {complaint.get('created_at', 'N/A')}")
                    st.write(f"- **Status:** {complaint.get('status', 'N/A')}")
                    st.write(f"- **Issue:** {complaint.get('complaint', 'N/A')}")
                    st.write("---")
            else:
                st.info("You have no past complaints.")

        elif choice == "My Profile":
        # Here integrate profile management
        # Initialize UserDB — assuming you have a separate user DB connection & class
            from utils.mysql_db import UserDB

        # You must create/connect a UserDB instance; example placeholder:
            user_db = UserDB(
                host="localhost",
                user="root",
                password="root",
                database="yash_infocity"
            )
            profile = ProfileManagement(user_db, self.username)
            profile.show()
            user_db.close()


if __name__ == "__main__":
    # Instantiate DB connection (update credentials accordingly)
    db = ComplaintDB(
        host="localhost",
        user="root",
        password="root",
        database="yash_infocity"
    )
    # Example username for testing
    username = "testuser"
    dashboard = ResidentDashboard(db, username)
    dashboard.show()
    db.close()
