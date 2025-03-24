import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import re
from datetime import datetime
import hashlib
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from decimal import Decimal


class GestionFinanciere:
    def __init__(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("green")
        
        self.root = ctk.CTk()
        self.root.title("Gestion Financière - Banque LMR")
        self.root.geometry("800x600")
        
        # Initialize attributes
        self.task_ids = []
        self.canvas = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Load logo
        try:
            image = Image.open("logo.png")
            self.logo = ctk.CTkImage(image, size=(100, 100))
            self.logo_label = ctk.CTkLabel(self.root, image=self.logo, text="")
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"Erreur chargement logo: {e}")
            self.logo = None
        
        # Database connection
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="357321zM@.",
                database="base1"
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Connexion à la base de données échouée: {err}")
            self.root.destroy()
            return
            
        self.utilisateur_id = None
        self.show_login()

    def on_closing(self):
        try:
            for task_id in self.task_ids:
                self.root.after_cancel(task_id)
            if self.db and self.db.is_connected():
                self.cursor.close()
                self.db.close()
        except Exception as e:
            print(f"Erreur fermeture: {e}")
        finally:
            self.root.destroy()

    def clear_window(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            plt.close('all')
            self.canvas = None
        for widget in self.root.winfo_children():
            widget.destroy()
        if self.logo:
            self.logo_label = ctk.CTkLabel(self.root, image=self.logo, text="")
            self.logo_label.pack(pady=10)

    def run(self):
        self.root.mainloop()

    def show_login(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.pack(pady=20, padx=20)

        ctk.CTkLabel(frame, text="Connexion", font=("Arial", 20)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Email:").pack(pady=5)
        self.email_entry = ctk.CTkEntry(frame, width=250)
        self.email_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Mot de passe:").pack(pady=5)
        self.password_entry = ctk.CTkEntry(frame, show="*", width=250)
        self.password_entry.pack(pady=5)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="Connexion", command=self.login).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="S'inscrire", command=self.show_register).pack(side="left", padx=10)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_password(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.;])[A-Za-z\d@$!%*?&.;]{10,}$"
        return re.match(pattern, password) is not None

    def login(self):
        email = self.email_entry.get().strip()
        password = self.hash_password(self.password_entry.get())
        
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
            
        try:
            query = "SELECT id FROM utilisateurs WHERE email = %s AND mot_de_passe = %s"
            self.cursor.execute(query, (email, password))
            result = self.cursor.fetchone()
            
            if result:
                self.utilisateur_id = result[0]
                self.show_main_menu()
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur de connexion: {err}")

    def show_register(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.pack(pady=20, padx=20)

        ctk.CTkLabel(frame, text="Inscription", font=("Arial", 20)).pack(pady=10)

        fields = [
            ("Nom:", "nom_entry"),
            ("Prénom:", "prenom_entry"),
            ("Email:", "email_reg_entry"),
            ("Mot de passe:", "password_reg_entry", True)
        ]
        
        for label, attr, *args in fields:
            ctk.CTkLabel(frame, text=label).pack(pady=5)
            setattr(self, attr, ctk.CTkEntry(frame, width=250, show="*" if args else ""))
            getattr(self, attr).pack(pady=5)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="S'inscrire", command=self.register).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Retour", command=self.show_login).pack(side="left", padx=10)

    def register(self):
        fields = {
            'nom': self.nom_entry.get().strip(),
            'prenom': self.prenom_entry.get().strip(),
            'email': self.email_reg_entry.get().strip(),
            'password': self.password_reg_entry.get()
        }

        if not all(fields.values()):
            messagebox.showerror("Erreur", "Tous les champs sont requis")
            return

        if not self.validate_password(fields['password']):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 10 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial")
            return

        try:
            query = "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (fields['nom'], fields['prenom'], fields['email'], self.hash_password(fields['password'])))
            self.db.commit()
            
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            utilisateur_id = self.cursor.fetchone()[0]
            numero_compte = f"FR{utilisateur_id:06d}{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.cursor.execute("INSERT INTO comptes (utilisateur_id, numero_compte) VALUES (%s, %s)", 
                              (utilisateur_id, numero_compte))
            self.db.commit()
            
            messagebox.showinfo("Succès", "Inscription réussie")
            self.show_login()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur d'inscription: {err}")

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
        frame.pack(pady=20, padx=20)

        fields = [
            ("Montant:", "montant_entry"),
            ("Description:", "desc_entry"),
            ("Catégorie:", "cat_entry")
        ]
        
        for label, attr in fields:
            ctk.CTkLabel(frame, text=label).pack(pady=5)
            setattr(self, attr, ctk.CTkEntry(frame, width=250))
            getattr(self, attr).pack(pady=5)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="Confirmer", command=self.effectuer_depot).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Retour", command=self.show_main_menu).pack(side="left", padx=10)

    def effectuer_depot(self):
        try:
            montant = Decimal(self.montant_entry.get())
            if montant <= 0:
                raise ValueError("Montant doit être positif")
                
            description = self.desc_entry.get().strip()
            categorie = self.cat_entry.get().strip()
            
            self.cursor.execute("SELECT id, solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
            compte = self.cursor.fetchone()
            if not compte:
                raise ValueError("Compte non trouvé")
                
            reference = f"DEP{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            self.cursor.execute("""
                INSERT INTO transactions (compte_id, reference_transaction, description, montant, type_transaction, categorie)
                VALUES (%s, %s, %s, %s, 'dépôt', %s)
            """, (compte[0], reference, description, montant, categorie))
            
            nouveau_solde = Decimal(compte[1]) + montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde, compte[0]))
            
            self.db.commit()
            messagebox.showinfo("Succès", "Dépôt effectué")
            self.show_main_menu()
        except (ValueError, mysql.connector.Error) as e:
            messagebox.showerror("Erreur", str(e))

    def show_historique(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        fields = [
            ("Date début (YYYY-MM-DD):", "date_debut"),
            ("Date fin (YYYY-MM-DD):", "date_fin"),
            ("Catégorie:", "cat_filter")
        ]
        
        for i, (label, attr) in enumerate(fields):
            ctk.CTkLabel(frame, text=label).grid(row=i, column=0, pady=5, padx=5)
            setattr(self, attr, ctk.CTkEntry(frame))
            getattr(self, attr).grid(row=i, column=1, pady=5, padx=5)

        ctk.CTkLabel(frame, text="Type:").grid(row=3, column=0, pady=5, padx=5)
        self.type_filter = ctk.CTkOptionMenu(frame, values=['Tous', 'retrait', 'dépôt', 'transfert'])
        self.type_filter.grid(row=3, column=1, pady=5, padx=5)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ctk.CTkButton(btn_frame, text="Rechercher", command=self.afficher_transactions).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Retour", command=self.show_main_menu).pack(side="left", padx=10)

        from tkinter import ttk
        self.tree = ttk.Treeview(frame, columns=('Ref', 'Desc', 'Montant', 'Date', 'Type', 'Cat'), show='headings')
        self.tree.grid(row=5, column=0, columnspan=2, pady=5, sticky="nsew")
        
        headings = {'Ref': 'Référence', 'Desc': 'Description', 'Montant': 'Montant', 
                   'Date': 'Date', 'Type': 'Type', 'Cat': 'Catégorie'}
        for col, text in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=120)

        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(1, weight=1)

    def afficher_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = """
            SELECT t.reference_transaction, t.description, t.montant, t.date_transaction, 
                   t.type_transaction, t.categorie
            FROM transactions t
            JOIN comptes c ON t.compte_id = c.id
            WHERE c.utilisateur_id = %s
        """
        params = [self.utilisateur_id]
        conditions = []
        
        try:
            if self.date_debut.get():
                datetime.strptime(self.date_debut.get(), '%Y-%m-%d')
                conditions.append("t.date_transaction >= %s")
                params.append(self.date_debut.get())
            
            if self.date_fin.get():
                datetime.strptime(self.date_fin.get(), '%Y-%m-%d')
                conditions.append("t.date_transaction <= %s")
                params.append(self.date_fin.get())
            
            if self.cat_filter.get():
                conditions.append("t.categorie = %s")
                params.append(self.cat_filter.get())
            
            if self.type_filter.get() != 'Tous':
                conditions.append("t.type_transaction = %s")
                params.append(self.type_filter.get())
            
            if conditions:
                query += " AND " + " AND ".join(conditions)
                
            self.cursor.execute(query, params)
            
            for row in self.cursor.fetchall():
                self.tree.insert('', 'end', values=row)
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide (YYYY-MM-DD)")

    def show_vue_globale(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.cursor.execute("SELECT solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
        solde = self.cursor.fetchone()[0]
        ctk.CTkLabel(frame, text=f"Solde actuel: {solde:.2f}€", font=("Arial", 16)).pack(pady=10)

        self.cursor.execute("""
            SELECT DATE_FORMAT(date_transaction, '%Y-%m-%d') AS jour, SUM(montant) AS total
            FROM transactions t
            JOIN comptes c ON t.compte_id = c.id
            WHERE c.utilisateur_id = %s AND t.type_transaction = 'retrait'
            GROUP BY jour
            ORDER BY jour
        """, (self.utilisateur_id,))

        resultats = self.cursor.fetchall()
        if resultats:
            mois, montants = zip(*resultats)
            montants = [float(m) for m in montants]

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(mois, montants, marker='o', color='blue')
            ax.set_title("Dépenses par mois")
            ax.set_xlabel("Mois")
            ax.set_ylabel("Montant (€)")
            ax.set_xticks(mois)
            ax.set_xticklabels(mois, rotation=45, ha='right')
            plt.tight_layout()

            self.canvas = FigureCanvasTkAgg(fig, master=frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)
        else:
            ctk.CTkLabel(frame, text="Aucune dépense enregistrée.").pack(pady=10)

        if solde < 0:
            self.cursor.execute("""
                INSERT INTO alertes (utilisateur_id, type_alert, message)
                SELECT %s, 'découvert', 'Attention: Votre compte est en négatif'
                WHERE NOT EXISTS (
                    SELECT 1 FROM alertes 
                    WHERE utilisateur_id = %s 
                    AND type_alert = 'découvert' 
                    AND date_alert > DATE_SUB(NOW(), INTERVAL 24 HOUR)
                )
            """, (self.utilisateur_id, self.utilisateur_id))
            self.db.commit()

        ctk.CTkButton(frame, text="Retour", command=self.show_main_menu).pack(pady=10)

    def show_retrait(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.pack(pady=20, padx=20)

        fields = [
            ("Montant:", "montant_retrait_entry"),
            ("Description:", "desc_retrait_entry")
        ]
        
        for label, attr in fields:
            ctk.CTkLabel(frame, text=label).pack(pady=5)
            setattr(self, attr, ctk.CTkEntry(frame, width=250))
            getattr(self, attr).pack(pady=5)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="Confirmer", command=self.effectuer_retrait).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Retour", command=self.show_main_menu).pack(side="left", padx=10)

    def effectuer_retrait(self):
        try:
            montant = Decimal(self.montant_retrait_entry.get())
            description = self.desc_retrait_entry.get().strip()
            
            if montant <= 0:
                raise ValueError("Le montant doit être positif")
            
            self.cursor.execute("SELECT id, solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
            compte = self.cursor.fetchone()
            
            if Decimal(compte[1]) < montant:
                raise ValueError("Solde insuffisant")
            
            reference = f"RET{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            self.cursor.execute("""
                INSERT INTO transactions (compte_id, reference_transaction, description, montant, type_transaction)
                VALUES (%s, %s, %s, %s, 'retrait')
            """, (compte[0], reference, description, montant))
            
            nouveau_solde = Decimal(compte[1]) - montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde, compte[0]))
            
            self.db.commit()
            messagebox.showinfo("Succès", "Retrait effectué")
            self.show_main_menu()
        except (ValueError, mysql.connector.Error) as e:
            messagebox.showerror("Erreur", str(e))

    def show_transfert(self):
        self.clear_window()
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.pack(pady=20, padx=20)

        fields = [
            ("Montant:", "montant_transfert_entry"),
            ("Compte destinataire:", "compte_dest_entry")
        ]
        
        for label, attr in fields:
            ctk.CTkLabel(frame, text=label).pack(pady=5)
            setattr(self, attr, ctk.CTkEntry(frame, width=250))
            getattr(self, attr).pack(pady=5)

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="Confirmer", command=self.effectuer_transfert).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Retour", command=self.show_main_menu).pack(side="left", padx=10)

    def effectuer_transfert(self):
        try:
            montant = Decimal(self.montant_transfert_entry.get())
            compte_dest = self.compte_dest_entry.get().strip()

            if montant <= 0:
                raise ValueError("Le montant doit être positif")

            self.cursor.execute("SELECT id, solde FROM comptes WHERE utilisateur_id = %s", (self.utilisateur_id,))
            compte_source = self.cursor.fetchone()

            if Decimal(compte_source[1]) < montant:
                raise ValueError("Solde insuffisant")

            self.cursor.execute("SELECT id, solde FROM comptes WHERE numero_compte = %s", (compte_dest,))
            compte_dest_id = self.cursor.fetchone()

            if not compte_dest_id:
                raise ValueError("Compte destinataire non trouvé")

            if compte_source[0] == compte_dest_id[0]:
                raise ValueError("Impossible de transférer vers le même compte")

            reference = f"TRF{datetime.now().strftime('%Y%m%d%H%M%S')}"

            self.cursor.execute("""
                INSERT INTO transferts (compte_source_id, compte_dest_id, montant)
                VALUES (%s, %s, %s)
            """, (compte_source[0], compte_dest_id[0], montant))
            
            self.cursor.execute("""
                INSERT INTO transactions (compte_id, reference_transaction, description, montant, type_transaction)
                VALUES (%s, %s, %s, %s, 'transfert')
            """, (compte_source[0], reference, f"Transfert vers {compte_dest}", montant))

            nouveau_solde_source = Decimal(compte_source[1]) - montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde_source, compte_source[0]))

            nouveau_solde_dest = Decimal(compte_dest_id[1]) + montant
            self.cursor.execute("UPDATE comptes SET solde = %s WHERE id = %s", (nouveau_solde_dest, compte_dest_id[0]))

            self.db.commit()
            messagebox.showinfo("Succès", "Transfert effectué")
            self.show_main_menu()

        except (ValueError, mysql.connector.Error) as e:
            messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
       
    app = GestionFinanciere()
    app.run()