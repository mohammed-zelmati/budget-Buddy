import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import re
from datetime import datetime
import hashlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from decimal import Decimal

class GestionFinanciere:
    def __init__(self):
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
        
        self.root = ctk.CTk()
        self.root.title("Gestion Financière")
        self.root.geometry("800x600")
        
        # Connexion à la base de données
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="357321zM@.",
            database="base1"
        )
        self.cursor = self.db.cursor()
        
        self.utilisateur_id = None
        self.show_login()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.;])[A-Za-z\d@$!%*?&.;]{10,}$"
        return re.match(pattern, password) is not None

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()
    
    def show_login(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Email:").grid(row=0, column=0, pady=10, padx=10)
        self.email_entry = ctk.CTkEntry(frame, width=200)
        self.email_entry.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Mot de passe:").grid(row=1, column=0, pady=10, padx=10)
        self.password_entry = ctk.CTkEntry(frame, show="*", width=200)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkButton(frame, text="Connexion", command=self.login).grid(row=2, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="S'inscrire", command=self.show_register).grid(row=2, column=1, pady=10, padx=10)

    def show_register(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Nom:").grid(row=0, column=0, pady=10, padx=10)
        self.nom_entry = ctk.CTkEntry(frame, width=200)
        self.nom_entry.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Prénom:").grid(row=1, column=0, pady=10, padx=10)
        self.prenom_entry = ctk.CTkEntry(frame, width=200)
        self.prenom_entry.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Email:").grid(row=2, column=0, pady=10, padx=10)
        self.email_reg_entry = ctk.CTkEntry(frame, width=200)
        self.email_reg_entry.grid(row=2, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Mot de passe:").grid(row=3, column=0, pady=10, padx=10)
        self.password_reg_entry = ctk.CTkEntry(frame, show="*", width=200)
        self.password_reg_entry.grid(row=3, column=1, pady=10, padx=10)

        ctk.CTkButton(frame, text="S'inscrire", command=self.register).grid(row=4, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="Retour", command=self.show_login).grid(row=4, column=1, pady=10, padx=10)

    def login(self):
        email = self.email_entry.get()
        password = self.hash_password(self.password_entry.get())
        
        query = "SELECT id FROM utilisateurs WHERE email = %s AND mot_de_passe = %s"
        self.cursor.execute(query, (email, password))
        result = self.cursor.fetchone()
        
        if result:
            self.utilisateur_id = result[0]
            self.show_main_menu()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    def register(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_reg_entry.get()
        password = self.password_reg_entry.get()

        if not all([nom, prenom, email, password]):
            messagebox.showerror("Erreur", "Tous les champs sont requis")
            return

        if not self.validate_password(password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 10 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial")
            return

        try:
            query = "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (nom, prenom, email, self.hash_password(password)))
            self.db.commit()
            
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            utilisateur_id = self.cursor.fetchone()[0]
            numero_compte = f"FR{utilisateur_id}{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.cursor.execute("INSERT INTO comptes (utilisateur_id, numero_compte) VALUES (%s, %s)", 
                              (utilisateur_id, numero_compte))
            self.db.commit()
            
            messagebox.showinfo("Succès", "Inscription réussie")
            self.show_login()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur: {err}")

    def show_main_menu(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(frame, text="Déposer", command=self.show_depot).grid(row=0, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="Retirer", command=self.show_retrait).grid(row=0, column=1, pady=10, padx=10)
        ctk.CTkButton(frame, text="Transférer", command=self.show_transfert).grid(row=1, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="Historique", command=self.show_historique).grid(row=1, column=1, pady=10, padx=10)
        ctk.CTkButton(frame, text="Vue globale", command=self.show_vue_globale).grid(row=2, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="Déconnexion", command=self.show_login).grid(row=2, column=1, pady=10, padx=10)

    def show_depot(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Montant:").grid(row=0, column=0, pady=10, padx=10)
        self.montant_entry = ctk.CTkEntry(frame, width=200)
        self.montant_entry.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Description:").grid(row=1, column=0, pady=10, padx=10)
        self.desc_entry = ctk.CTkEntry(frame, width=200)
        self.desc_entry.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Catégorie:").grid(row=2, column=0, pady=10, padx=10)
        self.cat_entry = ctk.CTkEntry(frame, width=200)
        self.cat_entry.grid(row=2, column=1, pady=10, padx=10)

        ctk.CTkButton(frame, text="Confirmer", command=self.effectuer_depot).grid(row=3, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="Retour", command=self.show_main_menu).grid(row=3, column=1, pady=10, padx=10)

    def effectuer_depot(self):
        try:
            montant = float(self.montant_entry.get())
            description = self.desc_entry.get()
            categorie = self.cat_entry.get()
            
            self.cursor.execute("SELECT id, solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
            compte = self.cursor.fetchone()
            
            reference = f"DEP{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            self.cursor.execute("""
                INSERT INTO transactions (compte_id, reference_transaction, description, montant, type_transaction, categorie)
                VALUES (%s, %s, %s, %s, 'dépôt', %s)
            """, (compte[0], reference, description, montant, categorie))
            
            nouveau_solde = float(compte[1]) + montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde, compte[0]))
            
            self.db.commit()
            messagebox.showinfo("Succès", "Dépôt effectué")
            self.show_main_menu()
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide")

    def show_historique(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Date début:").grid(row=0, column=0, pady=5, padx=5)
        self.date_debut = ctk.CTkEntry(frame)
        self.date_debut.grid(row=0, column=1, pady=5, padx=5)

        ctk.CTkLabel(frame, text="Date fin:").grid(row=1, column=0, pady=5, padx=5)
        self.date_fin = ctk.CTkEntry(frame)
        self.date_fin.grid(row=1, column=1, pady=5, padx=5)

        ctk.CTkLabel(frame, text="Catégorie:").grid(row=2, column=0, pady=5, padx=5)
        self.cat_filter = ctk.CTkEntry(frame)
        self.cat_filter.grid(row=2, column=1, pady=5, padx=5)

        ctk.CTkLabel(frame, text="Type:").grid(row=3, column=0, pady=5, padx=5)
        self.type_filter = ctk.CTkOptionMenu(frame, values=['retrait', 'dépôt', 'transfert'])
        self.type_filter.grid(row=3, column=1, pady=5, padx=5)

        ctk.CTkButton(frame, text="Rechercher", command=self.afficher_transactions).grid(row=4, column=0, pady=5, padx=5)
        ctk.CTkButton(frame, text="Retour", command=self.show_main_menu).grid(row=4, column=1, pady=5, padx=5)

        # Note: Customtkinter n'a pas d'équivalent direct à Treeview, on garde ttk.Treeview
        from tkinter import ttk
        self.tree = ttk.Treeview(frame, columns=('Ref', 'Desc', 'Montant', 'Date', 'Type', 'Cat'), show='headings')
        self.tree.grid(row=5, column=0, columnspan=2, pady=5, sticky="nsew")
        
        for col in ('Ref', 'Desc', 'Montant', 'Date', 'Type', 'Cat'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

    def afficher_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = """
            SELECT t.reference_transaction, t.description, t.montant, t.date_transaction, t.type_transaction, t.categorie
            FROM transactions t
            JOIN comptes c ON t.compte_id = c.id
            WHERE c.utilisateur_id = %s
        """
        params = [self.utilisateur_id]
        conditions = []
        
        # Filtrage sur la date de début
        if self.date_debut.get():
            conditions.append("t.date_transaction >= %s")
            params.append(self.date_debut.get())
        
        # Filtrage sur la date de fin
        if self.date_fin.get():
            conditions.append("t.date_transaction <= %s")
            params.append(self.date_fin.get())
        
        # Filtrage sur la catégorie
        if self.cat_filter.get():
            conditions.append("t.categorie = %s")
            params.append(self.cat_filter.get())
        
        # Filtrage sur le type de transaction (retrait, dépôt, transfert)
        if self.type_filter.get():
            conditions.append("t.type_transaction = %s")
            params.append(self.type_filter.get())
        
        # Ajouter les conditions à la requête si elles existent
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        # Exécuter la requête
        self.cursor.execute(query, params)
        
        # Insérer les résultats dans le Treeview
        for row in self.cursor.fetchall():
            self.tree.insert('', 'end', values=row)


    def show_vue_globale(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.cursor.execute("SELECT solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
        solde = self.cursor.fetchone()[0]
        ctk.CTkLabel(frame, text=f"Solde actuel: {solde}€", font=("Arial", 16)).pack(pady=10)

        self.cursor.execute("""
            SELECT DATE_FORMAT(date_transaction, '%Y-%m') as mois, SUM(montant) as total
            FROM transactions t
            JOIN comptes c ON t.compte_id = c.id
            WHERE c.utilisateur_id = %s AND t.type_transaction = 'retrait'
            GROUP BY mois
            ORDER BY mois
        """, (self.utilisateur_id,))
        
        mois, montants = zip(*self.cursor.fetchall()) if self.cursor.rowcount > 0 else ([], [])
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(mois, montants)
        ax.set_title("Dépenses par mois")
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        if solde < 0:
            self.cursor.execute("""
                INSERT INTO alertes (utilisateur_id, type_alert, message)
                VALUES (%s, 'découvert', 'Attention: Votre compte est en négatif')
            """, (self.utilisateur_id,))
            self.db.commit()

        ctk.CTkButton(frame, text="Retour", command=self.show_main_menu).pack(pady=10)

    def show_retrait(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Montant:").grid(row=0, column=0, pady=10, padx=10)
        self.montant_retrait_entry = ctk.CTkEntry(frame, width=200)
        self.montant_retrait_entry.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Description:").grid(row=1, column=0, pady=10, padx=10)
        self.desc_retrait_entry = ctk.CTkEntry(frame, width=200)
        self.desc_retrait_entry.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkButton(frame, text="Confirmer", command=self.effectuer_retrait).grid(row=2, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="Retour", command=self.show_main_menu).grid(row=2, column=1, pady=10, padx=10)

    def effectuer_retrait(self):
        try:
            montant = float(self.montant_retrait_entry.get())
            description = self.desc_retrait_entry.get()
            
            if montant <= 0:
                messagebox.showerror("Erreur", "Le montant doit être positif")
                return
            
            # Récupérer le compte de l'utilisateur
            self.cursor.execute("SELECT id, solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
            compte = self.cursor.fetchone()
            
            # Vérifier si le solde est suffisant
            if compte[1] < montant:
                messagebox.showerror("Erreur", "Solde insuffisant")
                return
            
            # Créer une référence de retrait unique
            reference = f"RET{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Insérer la transaction de retrait dans la base de données
            self.cursor.execute("""
                INSERT INTO transactions (compte_id, reference_transaction, description, montant, type_transaction)
                VALUES (%s, %s, %s, %s, 'retrait')
            """, (compte[0], reference, description, montant))
            
            # Mettre à jour le solde du compte
            nouveau_solde = float(compte[1]) - montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde, compte[0]))
            
            # Valider la transaction
            self.db.commit()
            messagebox.showinfo("Succès", "Retrait effectué avec succès")
            
            self.show_main_menu()
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide")


    def show_transfert(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Montant:").grid(row=0, column=0, pady=10, padx=10)
        self.montant_transfert_entry = ctk.CTkEntry(frame, width=200)
        self.montant_transfert_entry.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame, text="Compte destinataire:").grid(row=1, column=0, pady=10, padx=10)
        self.compte_dest_entry = ctk.CTkEntry(frame, width=200)
        self.compte_dest_entry.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkButton(frame, text="Confirmer", command=self.effectuer_transfert).grid(row=2, column=0, pady=10, padx=10)
        ctk.CTkButton(frame, text="Retour", command=self.show_main_menu).grid(row=2, column=1, pady=10, padx=10)

    def effectuer_transfert(self):
        try:
            montant = Decimal(self.montant_transfert_entry.get())
            compte_dest = self.compte_dest_entry.get()

            if montant <= 0:
                messagebox.showerror("Erreur", "Le montant doit être positif")
                return

            # Récupérer le compte source
            self.cursor.execute("SELECT id, solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
            compte_source = self.cursor.fetchone()

            # Vérifier si le solde est suffisant
            if compte_source[1] < montant:
                messagebox.showerror("Erreur", "Solde insuffisant")
                return

            # Récupérer le compte destinataire avec son solde
            self.cursor.execute("SELECT id, solde FROM comptes WHERE numero_compte = %s", (compte_dest,))
            compte_dest_id = self.cursor.fetchone()

            if not compte_dest_id:
                messagebox.showerror("Erreur", "Compte destinataire non trouvé")
                return

            # Créer une référence de transfert unique
            reference = f"TRF{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Insérer la transaction de transfert dans la base de données
            self.cursor.execute("""
                INSERT INTO transferts (compte_source_id, compte_dest_id, montant)
                VALUES (%s, %s, %s)
            """, (compte_source[0], compte_dest_id[0], montant))
            
            # Insérer une transaction de type "transfert" dans la table transactions
            self.cursor.execute("""
                INSERT INTO transactions (compte_id, reference_transaction, description, montant, type_transaction)
                VALUES (%s, %s, %s, %s, 'transfert')
            """, (compte_source[0], reference, f"Transfert vers {compte_dest}", montant))

            # Mettre à jour les soldes des deux comptes
            nouveau_solde_source = Decimal(compte_source[1]) - montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde_source, compte_source[0]))

            # Mettre à jour le solde du compte destinataire
            nouveau_solde_dest = Decimal(compte_dest_id[1]) + montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde_dest, compte_dest_id[0]))

            # Valider la transaction
            self.db.commit()

            messagebox.showinfo("Succès", "Transfert effectué avec succès")
            self.show_main_menu()

        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide")


if __name__ == "__main__":
    app = GestionFinanciere()
    app.run()