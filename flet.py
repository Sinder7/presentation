import sqlite3

# Подключаемся к базе данных (или создаем новую)
conn = sqlite3.connect('bicycle_shop.db')
cursor = conn.cursor()

# Создаем таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    price REAL,
    stock INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total REAL,
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(order_id) REFERENCES Orders(order_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
