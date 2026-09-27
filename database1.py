import sqlite3
from datetime import datetime

DB_NAME = "catalog.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            source_id TEXT,
            name TEXT NOT NULL,
            sku TEXT,
            price REAL DEFAULT 0,
            description TEXT,
            category TEXT,
            image_url TEXT,
            product_url TEXT,
            stock INTEGER DEFAULT 0,
            availability TEXT DEFAULT 'In Stock',
            updated_at TEXT
        )
    """)

    # Categories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    # Synchronization history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            added INTEGER,
            updated INTEGER,
            status TEXT,
            sync_time TEXT
        )
    """)

    # Settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_product(
    source,
    source_id,
    name,
    sku,
    price,
    description,
    category,
    image_url,
    product_url,
    stock,
    availability
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products
        (
            source,
            source_id,
            name,
            sku,
            price,
            description,
            category,
            image_url,
            product_url,
            stock,
            availability,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        source,
        source_id,
        name,
        sku,
        price,
        description,
        category,
        image_url,
        product_url,
        stock,
        availability,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_products():

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM products
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return rows


def delete_product(product_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()


def update_product(
    product_id,
    name,
    price,
    category,
    description,
    stock,
    image_url
):

    availability = "In Stock" if stock > 0 else "Out of Stock"

    conn = get_connection()

    conn.execute("""
        UPDATE products

        SET
            name = ?,
            price = ?,
            category = ?,
            description = ?,
            stock = ?,
            availability = ?,
            image_url = ?,
            updated_at = ?

        WHERE id = ?
    """, (
        name,
        price,
        category,
        description,
        stock,
        availability,
        image_url,
        datetime.now().isoformat(),
        product_id
    ))

    conn.commit()
    conn.close()


def add_category(name):

    conn = get_connection()

    try:
        conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()


def get_categories():

    conn = get_connection()

    rows = conn.execute(
        "SELECT name FROM categories ORDER BY name"
    ).fetchall()

    conn.close()

    return [row[0] for row in rows]


def save_setting(key, value):

    conn = get_connection()

    conn.execute("""
        INSERT OR REPLACE INTO settings
        (key, value)
        VALUES (?, ?)
    """, (key, value))

    conn.commit()
    conn.close()


def get_setting(key, default=""):

    conn = get_connection()

    row = conn.execute(
        "SELECT value FROM settings WHERE key = ?",
        (key,)
    ).fetchone()

    conn.close()

    if row:
        return row[0]

    return default


def add_sync_log(source, added, updated, status):

    conn = get_connection()

    conn.execute("""
        INSERT INTO sync_logs
        (source, added, updated, status, sync_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        source,
        added,
        updated,
        status,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_sync_logs():

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM sync_logs
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return rows