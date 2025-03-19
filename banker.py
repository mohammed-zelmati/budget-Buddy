import hashlib
import mysql.connector

class Banker:
    def __init__(self, connect):
        self.db = connect

    def register_banker(self, nom, prenom, email, mot_de_passe):
        hashed_password = hashlib.sha256(mot_de_passe.encode()).hexdigest()
        try:
            self.db.execute_query(
                "INSERT INTO banquiers (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)",
                (nom, prenom, email, hashed_password)
            )
            print("Banquier enregistré avec succès.")
        except mysql.connector.IntegrityError:
            print("Erreur : L'email existe déjà.")

    def login_banker(self, email, mot_de_passe):
        hashed_password = hashlib.sha256(mot_de_passe.encode()).hexdigest()
        result = self.db.fetch_query(
            "SELECT * FROM banquiers WHERE email = %s AND mot_de_passe = %s",
            (email, hashed_password)
        )
        if result:
            print("Connexion réussie.")
            return result[0]
        print("Identifiants invalides.")
        return None

    def assign_account(self, banquier_id, compte_id):
        try:
            self.db.execute_query(
                "INSERT INTO portefeuille (banquier_id, compte_id) VALUES (%s, %s)",
                (banquier_id, compte_id)
            )
            print("Compte attribué au banquier avec succès.")
        except mysql.connector.Error as e:
            print("Erreur :", e)

    def view_clients(self, banquier_id):
        clients = self.db.fetch_query(
            """
            SELECT utilisateurs.nom, utilisateurs.prenom, comptes.numero_compte, comptes.solde
            FROM portefeuille
            JOIN comptes ON portefeuille.compte_id = comptes.id
            JOIN utilisateurs ON comptes.utilisateur_id = utilisateurs.id
            WHERE portefeuille.banquier_id = %s
            """,
            (banquier_id,)
        )
        for client in clients:
            print(f"Client : {client[0]} {client[1]}, Compte : {client[2]}, Solde : {client[3]}")
