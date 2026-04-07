import psycopg2
import os

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        approved INTEGER DEFAULT 0,
        banned BOOLEAN DEFAULT FALSE
    );
    """)

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
def add_user(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users (user_id)
    VALUES (%s)
    ON CONFLICT (user_id) DO NOTHING
    """, (user_id,))

    conn.commit()
    conn.close()


def approve_user(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users (user_id, approved)
    VALUES (%s, 1)
    ON CONFLICT (user_id)
    DO UPDATE SET approved = 1
    """, (user_id,))

    conn.commit()
    conn.close()


def is_approved(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT approved FROM users WHERE user_id = %s", (user_id,))
    res = cur.fetchone()

    conn.close()
    return res and res[0] == 1


def ban_user(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("UPDATE users SET banned = TRUE WHERE user_id = %s", (user_id,))
    conn.commit()
    conn.close()


def is_banned(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT banned FROM users WHERE user_id = %s", (user_id,))
    res = cur.fetchone()

    conn.close()
    return res and res[0]


# --- LINKS ---
def create_link(user_id, project, price):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO links (user_id, project, price) VALUES (%s, %s, %s) RETURNING id",
        (user_id, project, price)
    )

    link_id = cur.fetchone()[0]

    link = f"https://web-production-0572a.up.railway.app/link/{link_id}"

    cur.execute("UPDATE links SET link = %s WHERE id = %s", (link, link_id))

    conn.commit()
    conn.close()

    return link_id


def get_user_links(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT project, price, link FROM links WHERE user_id = %s",
        (user_id,)
    )

    data = cur.fetchall()
    conn.close()
    return data


def delete_link(user_id, link):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM links WHERE user_id = %s AND link = %s",
        (user_id, link)
    )

    conn.commit()
    conn.close()
