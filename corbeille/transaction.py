from datetime import datetime

class Transaction:
    def __init__(self, connect):
        self.db = connect

    def add_transaction(self, compte_id, reference, description, montant, type, categorie):
        date = datetime.now().strftime("%Y-%m-%d")
        self.db.execute_query(
            "INSERT INTO transactions (compte_id, reference_transaction, description, montant, date_transaction, type_transaction, categorie) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (compte_id, reference, description, montant, date, type, categorie)
        )
        print("Transaction ajoutée avec succès.")

    def get_transactions(self, compte_id):
        return self.db.fetch_query(
            "SELECT * FROM transactions WHERE compte_id = %s ORDER BY date_transaction DESC",
            (compte_id,)
        )
