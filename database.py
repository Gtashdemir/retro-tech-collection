import sqlite3


DB_NAME = "collection.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            date_added TEXT NOT NULL,
            date_made TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_item(name, item_type, description, date_added, date_made):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO items (
            name,
            type,
            description,
            date_added,
            date_made
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        item_type,
        description,
        date_added,
        date_made
    ))

    connection.commit()
    connection.close()

def count_items():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM items
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_items_by_type(item_type, limit=20, offset=0):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, type, description, date_added, date_made
        FROM items
        WHERE type = ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (item_type, limit, offset))

    items = cursor.fetchall()

    connection.close()

    return items


def get_item_by_id(item_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, type, description, date_added, date_made
        FROM items
        WHERE id = ?
    """, (item_id,))

    item = cursor.fetchone()

    connection.close()

    return item

def count_items_by_type(item_type):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM items
        WHERE type = ?
    """, (item_type,))

    count = cursor.fetchone()[0]

    connection.close()

    return count

def search_items_by_name(item_type, search_text, limit=20, offset=0):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, type, description, date_added, date_made
        FROM items
        WHERE type = ?
        AND name LIKE ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (
        item_type,
        "%" + search_text + "%",
        limit,
        offset
    ))

    items = cursor.fetchall()

    connection.close()

    return items

def count_search_results(item_type, search_text):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM items
        WHERE type = ?
        AND name LIKE ?
    """, (
        item_type,
        "%" + search_text + "%"
    ))

    count = cursor.fetchone()[0]

    connection.close()

    return count

def search_all_items_by_name(search_text, limit=20, offset=0):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, type, description, date_added, date_made
        FROM items
        WHERE name LIKE ?
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (
        "%" + search_text + "%",
        limit,
        offset
    ))

    items = cursor.fetchall()

    connection.close()

    return items

def update_item_date_made(item_id, new_date_made):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET date_made = ?
        WHERE id = ?
    """, (
        new_date_made,
        item_id
    ))

    connection.commit()

    connection.close()

def update_item_name(item_id, new_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET name = ?
        WHERE id = ?
    """, (
        new_name,
        item_id
    ))

    connection.commit()
    connection.close()

def update_item_description(item_id, new_description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET description = ?
        WHERE id = ?
    """, (
        new_description,
        item_id
    ))

    connection.commit()
    connection.close()

def update_item_type(item_id, new_type):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE items
        SET type = ?
        WHERE id = ?
    """, (
        new_type,
        item_id
    ))

    connection.commit()
    connection.close()

def delete_item(item_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM items
        WHERE id = ?
    """, (item_id,))

    connection.commit()
    connection.close()