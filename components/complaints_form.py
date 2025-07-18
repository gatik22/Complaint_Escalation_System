import streamlit as st
from datetime import datetime, timezone
import os

class ComplaintForm:
    def __init__(self, username, db):
        self.username = username
        self.db = db
        self.upload_folder = "uploads"
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def show(self):
        if not self.username:
            st.error("You must be logged in to submit a complaint.")
            return

        with st.form("complaint_form", clear_on_submit=True):
            complaint_text = st.text_area("Describe your complaint")
            urgency = st.selectbox("Urgency", ["Low", "Medium", "High", "Critical"])
            department = st.selectbox("Department", [
                "Electricity", "Plumbing", "Pest Control", "Security",
                "Housekeeping", "Water Supply", "Other"
            ])
            uploaded_file = st.file_uploader("Upload a photo (optional)", type=["png", "jpg", "jpeg"])

            # Create two columns for the buttons
            col1, col2, col3 = st.columns([2, 6, 2])  # Adjust ratios as needed
            with col1:
                submitted = st.form_submit_button("Submit")
            with col2:
                st.write("")  # Empty column for spacing
            
        # Handle Submit button click
        if submitted:
            if not complaint_text.strip():
                st.warning("Please enter your complaint details.")
                return

            # Default photo_path to None
            photo_path = None
            if uploaded_file is not None:
                # Create a unique filename to avoid overwriting
                file_name = f"{self.username}_{int(datetime.now().timestamp())}_{uploaded_file.name}"
                save_path = os.path.join(self.upload_folder, file_name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                photo_path = save_path  # Path to be saved with complaint

            complaint = {
                "username": self.username,
                "complaint": complaint_text.strip(),
                "urgency": urgency,
                "department": department,
                "photo_path": photo_path,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "status": "Open"
            }

            try:
                with st.spinner("Registering your complaint..."):
                    success = self.db.save_complaint(complaint)  # Make sure this method supports photo_path now
                if success:
                    st.success("Complaint registered successfully!")
                else:
                    st.error("Failed to register complaint. Please try again.")
            except Exception as e:
                st.error(f"Failed to submit complaint: {e}")

        # Handle Logout button click
        
