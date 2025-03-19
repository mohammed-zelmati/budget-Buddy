from accountBank import AccountBank
from user import User
from connect import Connect
from transaction import Transaction
from gui import GUI
from banker import Banker

class Main:
    def __init__(self):
        # Initialiser la connexion à la base de données
        self.db = Connect(
            host="localhost",  
            user="root",      
            password="357321zM@.",      
            database="base1"  
        )
        self.banker = Banker(self.db)
        self.run()

    def run(self):
        try:
            # Initialiser les composants du programme
            print("Démarrage de l'application...")
            self.user = User(self.db)
            self.account_bank = AccountBank(self.db)
            self.transaction = Transaction(self.db)

            # Lancer l'interface graphique (GUI)
            GUI(self.db)

        except Exception as e:
            print("Une erreur s'est produite :", str(e))
        finally:
            # Fermer la connexion à la base de données proprement
            self.db.close_connection()
            print("Connexion à la base de données fermée.")

# Lancer le programme
if __name__ == "__main__":
    Main()
