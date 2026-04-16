import sqlite3

# Подключение к БД
conn = sqlite3.connect('inventory.db', check_same_thread=False)
cursor = conn.cursor()

# Создаём таблицу товаров
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')
conn.commit()

# Проверяем, есть ли товары в таблице
cursor.execute('SELECT COUNT(*) FROM items')
count = cursor.fetchone()[0]

# Если товаров нет — добавляем начальные
if count == 0:
    demo_items = [
        ('Ноутбук Lenovo', 15, 45000),
        ('Мышь компьютерная', 50, 1200),
        ('Клавиатура механическая', 25, 3500),
        ('Монитор 24"', 10, 18000),
        ('Наушники проводные', 40, 2500),
        ('Веб-камера HD', 8, 3200),
        ('Внешний жёсткий диск 1ТБ', 12, 5500),
        ('Флешка 64GB', 100, 800),
    ]
    cursor.executemany('INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)', demo_items)
    conn.commit()
    print(f"Добавлено {len(demo_items)} товаров на склад")

# Функции для работы со складом
def get_all_items():
    cursor.execute('SELECT * FROM items ORDER BY name')
    return cursor.fetchall()

def add_item(name, quantity, price):
    cursor.execute('INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)',
                   (name, quantity, price))
    conn.commit()

def update_item(item_id, quantity, price):
    cursor.execute('UPDATE items SET quantity = ?, price = ? WHERE id = ?',
                   (quantity, price, item_id))
    conn.commit()

def delete_item(item_id):
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()

def get_low_stock(threshold=10):
    """Получить товары с малым остатком"""
    cursor.execute('SELECT * FROM items WHERE quantity < ? ORDER BY quantity', (threshold,))
    return cursor.fetchall()

def get_total_value():
    """Общая стоимость всех товаров"""
    cursor.execute('SELECT SUM(quantity * price) FROM items')
    result = cursor.fetchone()[0]
    return result if result else 0