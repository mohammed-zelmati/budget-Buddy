import mysql.connector
import bcrypt
from config import DB_CONFIG

class UserManager:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def register(self, nom, prenom, email, password):
        # Check password complexity
        if not (len(password) >= 10 and any(c.isupper() for c in password) and
                any(c.islower() for c in password) and any(c.isdigit() for c in password) and
                any(not c.isalnum() for c in password)):
            return "Password must be 10+ chars with upper, lower, digit, and special char."
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            self.cursor.execute(
                "INSERT INTO users (nom, prenom, email, password) VALUES (%s, %s, %s, %s)",
                (nom, prenom, email, hashed_password)
            )
            self.conn.commit()
            return "Registration successful."
        except mysql.connector.IntegrityError:
            return "This email is already in use."

    def login(self, email, password):
        self.cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = self.cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            return user[0]  # Return user ID
        return None

    def close(self):
        self.cursor.close()
        self.conn.close()