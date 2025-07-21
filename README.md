Complaint Escalation System
A web-based Complaint Escalation System built with Python (using object-oriented programming concepts) and Streamlit for rapid, interactive UI development. This app enables residents and admins to file, track, and manage complaints seamlessly.

Features
Object-Oriented Python backend for code modularity and maintainability.
Streamlit-powered user interface for instant interaction.
Resident and admin panels with authentication.
Residents can submit complaints with attachments, view status, and manage profiles.
Admins can view, filter, escalate, update, and delete complaints.
Complaint photo upload and display functionality.
Sidebar navigation for a clean, user-friendly experience.

Setup Instructions
1. Clone the Repository
git clone https://github.com/yourusername/complaint-escalation-system.git
cd complaint-escalation-system

3. Install Dependencies
Before running the project, ensure you have Python 3.7+ installed.
Install required libraries using:
pip install -r requirements.txt
Note: Double-check the requirements.txt file for any additional package you might need.

4. Configure the Database
Update your database connection parameters in the relevant Python files (e.g., utils/mysql_db.py).
Make sure your MySQL database is set up with the required tables.

5. Run the Application
From your project directory:
streamlit run main.py
The app will open automatically in your browser.
