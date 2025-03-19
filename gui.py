import tkinter as tk
from tkinter import messagebox
# from connect import Connect
from user import User

class GUI:
    def __init__(self, connect):
        self.db = connect
        self.user = User(connect)
        self.window = tk.Tk()
        self.window.title("Gestion Financière")
        self.window.geometry("800x600")  # Définit une taille de 800px par 600px
        self.window.resizable(True, True)  # Permet le redimensionnement de la fenêtre
        self.login_page()

    def login_page(self):
        tk.Label(self.window, text="Email").pack()
        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack()

        tk.Label(self.window, text="Mot de passe").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        tk.Button(self.window, text="Se connecter", command=self.login).pack()
        tk.Button(self.window, text="S'inscrire", command=self.register_page).pack()

        self.window.mainloop()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = self.user.login(email, password)
        if user:
            messagebox.showinfo("Succès", "Connexion réussie !")

    def register_page(self):
        self.window.destroy()
        self.window = tk.Tk()
        self.window.title("Inscription")

        tk.Label(self.window, text="Nom").pack()
        self.nom_entry = tk.Entry(self.window)
        self.nom_entry.pack()

        tk.Label(self.window, text="Prénom").pack()
        self.prenom_entry = tk.Entry(self.window)
        self.prenom_entry.pack()

        tk.Label(self.window, text="Email").pack()
        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack()

        tk.Label(self.window, text="Mot de passe").pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        tk.Button(self.window, text="S'inscrire", command=self.register).pack()

    def register(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.user.register(nom, prenom, email, password)
        messagebox.showinfo("Succès", "Inscription réussie !")
        
        # Fermer l'ancienne fenêtre et recréer une nouvelle instance avant de revenir à la page de connexion
        self.window.destroy()
        self.window = tk.Tk()  # Crée une nouvelle instance de Tk
        self.login_page()
