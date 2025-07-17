import pymysql
import streamlit as st

class MySQLConnection:
    def __init__(self, host='127.0.0.1', user='root', password='root', database='yash_infocity'):
        try:
            self.conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            st.error(f"Error connecting to MySQL: {e}")
            self.conn = None

    def close(self):
        if self.conn:
            self.conn.close()

class UserDB(MySQLConnection):
    def load_users(self):
        if not self.conn:
            return []
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT name, username, password, role FROM users")
            return cursor.fetchall()

    def save_user(self, user):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cursor:
                query = "INSERT INTO users (name, username, password, role) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (user['name'], user['username'], user['password'], user['role']))
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            st.error(f"Error saving user: {e}")
            return False

    def get_user_by_username(self, username):
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                return user
        except pymysql.MySQLError as e:
            st.error(f"Error fetching user: {e}")
            return None

    def update_user_profile(self, username, name):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET name=%s WHERE username=%s",
                    (name, username)
                )
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            st.error(f"Error updating user profile: {e}")
            return False

    def update_user_password(self, username, new_password):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET password=%s WHERE username=%s",
                    (new_password, username)
                )
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            st.error(f"Error updating user password: {e}")
            return False

class ComplaintDB(MySQLConnection):
    def fetch_complaints(self):
        if not self.conn:
            return []
        with self.conn.cursor() as cursor:
            # Fetch essential columns only
            cursor.execute("""
                SELECT id, username, complaint, urgency, department, status, photo_path, created_at 
                FROM complaints 
                ORDER BY created_at DESC
            """)
            return cursor.fetchall()  # pymysql cursors with DictCursor return dicts

    def fetch_complaints_by_user(self, username):
        if not self.conn:
            return []
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, complaint, urgency, department, status, photo_path, created_at 
                FROM complaints 
                WHERE username=%s
                ORDER BY created_at DESC
            """, (username,))
            return cursor.fetchall()

    def save_complaint(self, complaint: dict):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cursor:
                query = """
                    INSERT INTO complaints 
                    (username, complaint, urgency, department, photo_path, created_at, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    complaint["username"],
                    complaint["complaint"],
                    complaint["urgency"],
                    complaint["department"],
                    complaint.get("photo_path"),  # optional, None if no photo
                    complaint["created_at"],
                    complaint["status"]
                )
                cursor.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving complaint: {e}")
            return False

    def update_status(self, complaint_id, new_status):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE complaints SET status=%s WHERE id=%s", (new_status, complaint_id)
                )
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            st.error(f"Error updating complaint status: {e}")
            return False

    def delete_complaint(self, complaint_id):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM complaints WHERE id=%s", (complaint_id,)
                )
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            st.error(f"Error deleting complaint: {e}")
            return False

