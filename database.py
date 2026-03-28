import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

# --- USERS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    approved INTEGER DEFAULT 0
)
""")

# --- LINKS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    project TEXT,
    price INTEGER,
    link TEXT
)
""")

# --- SETTINGS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    user_id INTEGER PRIMARY KEY,
    tag TEXT DEFAULT '#',
    domain TEXT DEFAULT 'Общий',
    payment TEXT DEFAULT 'TRC20',
    traffic INTEGER DEFAULT 0
)
""")

# --- ROLES ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
    user_id INTEGER PRIMARY KEY,
    role TEXT,
    banned INTEGER DEFAULT 0
)
""")

# --- LOGS ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# ---------- ФУНКЦИИ ----------

def approve_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, approved) VALUES (?, 0)", (user_id,))
    cursor.execute("UPDATE users SET approved=1 WHERE user_id=?", (user_id,))
    conn.commit()


def is_approved(user_id):
    cursor.execute("SELECT approved FROM users WHERE user_id=?", (user_id,))
    r = cursor.fetchone()
    return r and r[0] == 1


def get_settings(user_id):
    cursor.execute("SELECT * FROM settings WHERE user_id=?", (user_id,))
    data = cursor.fetchone()

    if not data:
        cursor.execute("INSERT INTO settings (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return get_settings(user_id)

    return {
        "tag": data[1],
        "domain": data[2],
        "payment": data[3],
        "traffic": data[4]
    }


def get_role(user_id):
    cursor.execute("SELECT role, banned FROM roles WHERE user_id=?", (user_id,))
    r = cursor.fetchone()
    if not r:
        return "worker", 0
    return r


def set_role(user_id, role):
    cursor.execute(
        "INSERT OR REPLACE INTO roles (user_id, role, banned) VALUES (?, ?, 0)",
        (user_id, role)
    )
    conn.commit()


def ban_user(user_id):
    cursor.execute("UPDATE roles SET banned=1 WHERE user_id=?", (user_id,))
    conn.commit()


def unban_user(user_id):
    cursor.execute("UPDATE roles SET banned=0 WHERE user_id=?", (user_id,))
    conn.commit()


def log(user_id, action):
    cursor.execute("INSERT INTO logs (user_id, action) VALUES (?, ?)", (user_id, action))
    conn.commit()
