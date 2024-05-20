from data.db_config import get_connection

def add_category(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Category (name) VALUES (%s)', (name,))
    conn.commit()
    conn.close()

def edit_category(category_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Category SET name = %s WHERE id = %s', (new_name, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Category WHERE id = %s', (category_id,))
    conn.commit()
    conn.close()

def search_categories(name=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM Category'
    if name:
        query += ' WHERE name LIKE %s'
        cursor.execute(query, ('%' + name + '%',))
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
