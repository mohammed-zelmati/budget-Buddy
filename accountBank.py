class AccountBank:
    def __init__(self, connect):
        self.db = connect

    def create_account(self, utilisateur_id, numero_compte):
        self.db.execute_query(
            "INSERT INTO comptes (utilisateur_id, numero_compte) VALUES (%s, %s)",
            (utilisateur_id, numero_compte)
        )
        print("Compte créé avec succès.")

    def deposit(self, compte_id, montant):
        self.db.execute_query(
            "UPDATE comptes SET solde = solde + %s WHERE id = %s",
            (montant, compte_id)
        )
        print("Dépôt effectué.")

    def withdraw(self, compte_id, montant):
        solde = self.db.fetch_query("SELECT solde FROM comptes WHERE id = %s", (compte_id,))
        if solde and solde[0][0] >= montant:
            self.db.execute_query(
                "UPDATE comptes SET solde = solde - %s WHERE id = %s",
                (montant, compte_id)
            )
            print("Retrait effectué.")
        else:
            print("Fonds insuffisants.")
