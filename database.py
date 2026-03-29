import psycopg2
import os

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# --- INIT DB ---

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        approved INTEGER DEFAULT 0
    );
    """)

    # LINKS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        project TEXT,
        price INTEGER,
        link TEXT
    );
    """)

    conn.commit()
    conn.close()


# --- USERS ---

def approve_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users (user_id, approved)
    VALUES (%s, 1)
    ON CONFLICT (user_id)
    DO UPDATE SET approved = 1;
    """, (user_id,))

    conn.commit()
    conn.close()


def is_approved(user_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT approved FROM users WHERE user_id = %s", (user_id,))
    res = cur.fetchone()

    conn.close()
    return res and res[0] == 1


# --- LINKS ---

def create_link(user_id, project, price, link):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
    "INSERT INTO links (user_id, project, price, link) VALUES (%s, %s, %s, %s)",
    (user_id, project, price, link)
)

    conn.commit()
    conn.close()


def get_user_links(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT project, link FROM links WHERE user_id = %s",
        (user_id,)
    )

    data = cur.fetchall()
    conn.close()
    return data
