import json
import os

USERS_FILE = os.path.join('data', 'users.json')
COMPLAINTS_FILE = os.path.join('data', 'complaints.json')

def load_users():
    """Load users from JSON file with exception handling."""
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
        
def load_user_complaints(username):
    try:
        with open(COMPLAINTS_FILE, 'r') as f:
            all_complaints = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return [c for c in all_complaints if c.get('username', '').lower() == username.lower()]

def load_all_complaints():
    try:
        with open(COMPLAINTS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_complaints(complaints):
    with open(COMPLAINTS_FILE, "w") as f:
        json.dump(complaints, f, indent=4)
