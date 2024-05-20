from data.db_config import get_connection


def add_product(name, price, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Product (name, price, category_id) VALUES (%s, %s, %s)', (name, price, category_id))
    conn.commit()
    conn.close()

def edit_product(product_id, new_name, new_price, new_category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE Product 
    SET name = %s, price = %s, category_id = %s 
    WHERE id = %s
    ''', (new_name, new_price, new_category_id, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Product WHERE id = %s', (product_id,))
    conn.commit()
    conn.close()

def search_products(name=None, category_id=None, price_range=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM Product WHERE 1=1'
    params = []
    if name:
        query += ' AND name LIKE %s'
        params.append('%' + name + '%')
    if category_id:
        query += ' AND category_id = %s'
        params.append(category_id)
    if price_range:
        query += ' AND price BETWEEN %s AND %s'
        params.append(price_range[0])
        params.append(price_range[1])
    cursor.execute(query, tuple(params))
    result = cursor.fetchall()
    conn.close()
    return result
