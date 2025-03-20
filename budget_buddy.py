import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu
from tkinter import messagebox, ttk
import tkinter as tk
from user_manager import UserManager
from transaction_manager import TransactionManager
import matplotlib.pyplot as plt

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BudgetBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Buddy")
        self.root.geometry("800x600")
        self.user_manager = UserManager()
        self.transaction_manager = TransactionManager()
        self.current_user = None
        
        # Close database connections on exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_login()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_closing(self):
        self.user_manager.close()
        self.transaction_manager.close()
        self.root.destroy()

    def show_login(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Login", font=("Arial", 24)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Email").pack()
        self.entry_email = ctk.CTkEntry(frame, width=200)
        self.entry_email.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Password").pack()
        self.entry_password = ctk.CTkEntry(frame, show="*", width=200)
        self.entry_password.pack(pady=5)
        
        ctk.CTkButton(frame, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(frame, text="Register", command=self.show_register).pack()

    def show_register(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Register", font=("Arial", 24)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Nom").pack()
        self.entry_nom = ctk.CTkEntry(frame, width=200)
        self.entry_nom.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Prénom").pack()
        self.entry_prenom = ctk.CTkEntry(frame, width=200)
        self.entry_prenom.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Email").pack()
        self.entry_email_reg = ctk.CTkEntry(frame, width=200)
        self.entry_email_reg.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Password").pack()
        self.entry_password_reg = ctk.CTkEntry(frame, show="*", width=200)
        self.entry_password_reg.pack(pady=5)
        
        ctk.CTkButton(frame, text="Register", command=self.register).pack(pady=10)
        ctk.CTkButton(frame, text="Back", command=self.show_login).pack()

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        user_id = self.user_manager.login(email, password)
        if user_id:
            self.current_user = user_id
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email_reg.get()
        password = self.entry_password_reg.get()
        result = self.user_manager.register(nom, prenom, email, password)
        messagebox.showinfo("Result", result)
        if "successful" in result:
            self.show_login()

    def show_dashboard(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        balance = self.transaction_manager.get_balance(self.current_user)
        ctk.CTkLabel(frame, text=f"Current Balance: {balance:.2f} €", font=("Arial", 20)).pack(pady=20)
        if balance < 0:
            messagebox.showwarning("Alert", "Your balance is negative!")
        
        ctk.CTkButton(frame, text="Add Transaction", command=self.show_add_transaction).pack(pady=10)
        ctk.CTkButton(frame, text="View History", command=self.show_history).pack(pady=10)
        ctk.CTkButton(frame, text="Spending by Category", command=self.show_spending_graph).pack(pady=10)

    def show_add_transaction(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Add Transaction", font=("Arial", 24)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Reference").pack()
        ref = ctk.CTkEntry(frame, width=200)
        ref.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Description").pack()
        desc = ctk.CTkEntry(frame, width=200)
        desc.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Amount").pack()
        amount = ctk.CTkEntry(frame, width=200)
        amount.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Date (YYYY-MM-DD)").pack()
        date = ctk.CTkEntry(frame, width=200)
        date.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Type").pack()
        type_var = tk.StringVar(value="deposit")
        type_menu = ctk.CTkOptionMenu(frame, variable=type_var, values=["deposit", "withdrawal", "transfer"])
        type_menu.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Category").pack()
        categories = self.transaction_manager.get_categories()
        category_names = [cat[1] for cat in categories]
        cat_var = tk.StringVar(value=category_names[0] if category_names else "No categories")
        cat_menu = ctk.CTkOptionMenu(frame, variable=cat_var, values=category_names)
        cat_menu.pack(pady=5)
        
        def save_transaction():
            try:
                cat_id = next(cat[0] for cat in categories if cat[1] == cat_var.get())
                self.transaction_manager.add_transaction(
                    ref.get(), desc.get(), float(amount.get()), date.get(), type_var.get(), self.current_user, cat_id
                )
                messagebox.showinfo("Success", "Transaction added")
                self.show_dashboard()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount or date format")
        
        ctk.CTkButton(frame, text="Save", command=save_transaction).pack(pady=10)
        ctk.CTkButton(frame, text="Back", command=self.show_dashboard).pack()

    def show_history(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Transaction History", font=("Arial", 24)).pack(pady=10)
        
        # Filter section
        filter_frame = ctk.CTkFrame(frame)
        filter_frame.pack(pady=10)
        
        ctk.CTkLabel(filter_frame, text="Date From").grid(row=0, column=0, padx=5)
        date_from = ctk.CTkEntry(filter_frame, width=120)
        date_from.grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(filter_frame, text="Date To").grid(row=0, column=2, padx=5)
        date_to = ctk.CTkEntry(filter_frame, width=120)
        date_to.grid(row=0, column=3, padx=5)
        
        ctk.CTkLabel(filter_frame, text="Category").grid(row=1, column=0, padx=5)
        categories = self.transaction_manager.get_categories()
        category_names = ["All"] + [cat[1] for cat in categories]
        cat_var = tk.StringVar(value="All")
        cat_menu = ctk.CTkOptionMenu(filter_frame, variable=cat_var, values=category_names)
        cat_menu.grid(row=1, column=1, padx=5)
        
        ctk.CTkLabel(filter_frame, text="Type").grid(row=1, column=2, padx=5)
        type_var = tk.StringVar(value="All")
        type_menu = ctk.CTkOptionMenu(filter_frame, variable=type_var, values=["All", "deposit", "withdrawal", "transfer"])
        type_menu.grid(row=1, column=3, padx=5)
        
        ctk.CTkLabel(filter_frame, text="Order by Amount").grid(row=2, column=0, padx=5)
        order_var = tk.StringVar(value="ASC")
        order_menu = ctk.CTkOptionMenu(filter_frame, variable=order_var, values=["ASC", "DESC"])
        order_menu.grid(row=2, column=1, padx=5)
        
        # Transaction table
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.pack(pady=10, fill="both", expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Ref", "Desc", "Amount", "Date", "Type", "Cat"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Ref", text="Reference")
        tree.heading("Desc", text="Description")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")
        tree.heading("Type", text="Type")
        tree.heading("Cat", text="Category")
        tree.pack(fill="both", expand=True)
        
        def apply_filters():
            filters = {}
            if date_from.get():
                filters['min_date'] = date_from.get()
            if date_to.get():
                filters['max_date'] = date_to.get()
            if cat_var.get() != "All":
                cat_id = next(cat[0] for cat in categories if cat[1] == cat_var.get())
                filters['category'] = cat_id
            if type_var.get() != "All":
                filters['type'] = type_var.get()
            filters['order'] = order_var.get()
            
            transactions = self.transaction_manager.get_transactions(self.current_user, filters)
            tree.delete(*tree.get_children())
            for trans in transactions:
                tree.insert("", "end", values=trans)
        
        ctk.CTkButton(filter_frame, text="Apply Filters", command=apply_filters).grid(row=3, column=0, columnspan=4, pady=10)
        ctk.CTkButton(frame, text="Back", command=self.show_dashboard).pack(pady=10)
        
        # Initial load
        apply_filters()

    def show_spending_graph(self):
        data = self.transaction_manager.get_spending_by_category(self.current_user)
        if data:
            categories, amounts = zip(*data)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title("Spending by Category")
            plt.show()
        else:
            messagebox.showinfo("Info", "No spending data available")

if __name__ == "__main__":
    root = ctk.CTk()
    app = BudgetBuddyApp(root)
    root.mainloop()