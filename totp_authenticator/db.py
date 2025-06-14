import sqlite3
import os
from typing import Optional

class Database:
    def __init__(self, db_path: str = "totp_auth.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    totp_secret TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_user(self, username: str, totp_secret: str) -> bool:
        """Add a new user with their TOTP secret"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, totp_secret) VALUES (?, ?)",
                    (username, totp_secret)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
    
    def get_user_secret(self, username: str) -> Optional[str]:
        """Retrieve the TOTP secret for a user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT totp_secret FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    
    def user_exists(self, username: str) -> bool:
        """Check if a user exists in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM users WHERE username = ?",
                (username,)
            )
            return cursor.fetchone() is not None
    
    def get_all_users(self) -> list:
        """Get all usernames (for testing purposes)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users")
            return [row[0] for row in cursor.fetchall()]