import sqlite3

DB_NAME = "crypto.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            network TEXT,
            user_id INTEGER,
            portfolio_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
        )
        ''')

        conn.commit()

def add_user(user_id, username):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()

def add_portfolio(user_id, name):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO portfolios (name, user_id) VALUES (?, ?)", (name, user_id))
        conn.commit()

def add_wallet(user_id, name, network, portfolio_id=None):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO wallets (name, network, user_id, portfolio_id) VALUES (?, ?, ?, ?)",
            (name, network, user_id, portfolio_id)
        )
        conn.commit()

def get_user_wallets(user_id, only_unassigned=False):
    with get_db() as conn:
        cursor = conn.cursor()
        if only_unassigned:
            cursor.execute("SELECT id, name, network FROM wallets WHERE user_id = ? AND portfolio_id IS NULL", (user_id,))
        else:
            cursor.execute("SELECT id, name, network, portfolio_id FROM wallets WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

def get_user_portfolios(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM portfolios WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

def assign_wallet_to_portfolio(wallet_id, portfolio_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE wallets SET portfolio_id = ? WHERE id = ?", (portfolio_id, wallet_id))
        conn.commit()