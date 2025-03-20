import mysql.connector
from config import DB_CONFIG

class TransactionManager:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def add_transaction(self, reference, description, montant, date, type, user_id, category_id):
        self.cursor.execute(
            "INSERT INTO transactions (reference, description, montant, date, type, user_id, category_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (reference, description, montant, date, type, user_id, category_id)
        )
        self.conn.commit()

    def get_transactions(self, user_id, filters=None):
        if filters is None:
            filters = {}
        query = "SELECT t.id, t.reference, t.description, t.montant, t.date, t.type, c.name " \
                "FROM transactions t JOIN categories c ON t.category_id = c.id WHERE t.user_id = %s"
        params = [user_id]
        
        if 'min_date' in filters:
            query += " AND t.date >= %s"
            params.append(filters['min_date'])
        if 'max_date' in filters:
            query += " AND t.date <= %s"
            params.append(filters['max_date'])
        if 'category' in filters:
            query += " AND t.category_id = %s"
            params.append(filters['category'])
        if 'type' in filters:
            query += " AND t.type = %s"
            params.append(filters['type'])
        
        order = filters.get('order', 'ASC')
        query += f" ORDER BY t.montant {order}"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_balance(self, user_id):
        self.cursor.execute(
            "SELECT SUM(CASE WHEN type = 'deposit' THEN montant ELSE -montant END) "
            "FROM transactions WHERE user_id = %s", (user_id,)
        )
        balance = self.cursor.fetchone()[0]
        return balance if balance else 0.0

    def get_categories(self):
        self.cursor.execute("SELECT id, name FROM categories")
        return self.cursor.fetchall()

    def get_spending_by_category(self, user_id):
        self.cursor.execute(
            "SELECT c.name, SUM(t.montant) FROM transactions t "
            "JOIN categories c ON t.category_id = c.id "
            "WHERE t.user_id = %s AND t.type = 'withdrawal' "
            "GROUP BY c.name", (user_id,)
        )
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()