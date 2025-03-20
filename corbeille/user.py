import hashlib
import mysql.connector

class User:
    def __init__(self, connect):
        self.db = connect

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, nom, prenom, email, mot_de_passe):
        hashed_password = self.hash_password(mot_de_passe)
        try:
            self.db.execute_query(
                "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)",
                (nom, prenom, email, hashed_password)
            )
            print("Inscription réussie.")
        except mysql.connector.IntegrityError:
            print("Erreur : L'email existe déjà.")

    def login(self, email, mot_de_passe):
        hashed_password = self.hash_password(mot_de_passe)
        result = self.db.fetch_query(
            "SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s",
            (email, hashed_password)
        )
        if result:
            print("Connexion réussie.")
            return result[0]
        print("Identifiants invalides.")
        return None
