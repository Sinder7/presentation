Отлично! Начнем разработку MVP системы учета товаров на Flask. Разобьем процесс на этапы и реализуем ключевые функции шаг за шагом. Вот план:

---

### **1. Настройка окружения**
1. Установите Python (рекомендуется версия 3.10+).
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows
   ```
3. Установите Flask и необходимые расширения:
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-wtf python-dotenv
   ```

---

### **2. Структура проекта**
Создайте папки и файлы:
```
your_project/
├── app/
│   ├── __init__.py
│   ├── models.py       # Модели данных
│   ├── routes.py       # Маршруты (роуты)
│   ├── forms.py        # Формы (WTForms)
│   ├── templates/      # HTML-шаблоны
│   │   ├── base.html   # Базовый шаблон
│   │   ├── products/   # Шаблоны для товаров
│   │   └── sales/      # Шаблоны для продаж
│   └── static/         # CSS, JS, изображения
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
└── run.py              # Точка входа
```

---

### **3. Базовая конфигурация**
**config.py**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///shop.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

**app/__init__.py**:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Регистрация роутов
    from app.routes import main, products, sales
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(sales)

    return app
```

**run.py**:
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

---

### **4. Модели данных (app/models.py)**
Реализуем базовые сущности:
```python
from app import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='cashier')  # admin или cashier

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    article = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

---

### **5. Роуты (app/routes.py)**
Разделим на модули:
- **main.py** – главная страница и аутентификация.
- **products.py** – управление товарами.
- **sales.py** – оформление продаж.

**Пример для products.py**:
```python
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import Product
from app.forms import ProductForm

products = Blueprint('products', __name__)

@products.route('/products')
@login_required
def product_list():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@products.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            article=form.article.data,
            price=form.price.data,
            quantity=form.quantity.data,
            category=form.category.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Товар добавлен!', 'success')
        return redirect(url_for('products.product_list'))
    return render_template('products/add.html', form=form)
```

---

### **6. Формы (app/forms.py)**
Используем Flask-WTF для валидации:
```python
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    article = StringField('Артикул', validators=[DataRequired(), Length(min=3)])
    price = FloatField('Цена', validators=[DataRequired()])
    quantity = IntegerField('Количество', default=0)
    category = SelectField('Категория', choices=[('electronics', 'Электроника'), ('food', 'Продукты')])
```

---

### **7. Шаблоны (templates/)**
**base.html** (основной макет):
```html
<!DOCTYPE html>
<html>
<head>
    <title>Магазин – {% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('main.index') }}">Главная</a>
        <a href="{{ url_for('products.product_list') }}">Товары</a>
        <a href="{{ url_for('sales.new_sale') }}">Продажи</a>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**products/list.html**:
```html
{% extends "base.html" %}
{% block title %}Товары{% endblock %}
{% block content %}
<h1>Список товаров</h1>
<a href="{{ url_for('products.add_product') }}">Добавить товар</a>
<table>
    <tr>
        <th>Название</th>
        <th>Артикул</th>
        <th>Цена</th>
        <th>Количество</th>
    </tr>
    {% for product in products %}
    <tr>
        <td>{{ product.name }}</td>
        <td>{{ product.article }}</td>
        <td>{{ product.price }}</td>
        <td>{{ product.quantity }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
```

---

### **8. Реализация MVP-функций**
#### Основные этапы:
1. **Аутентификация**:
   - Форма входа (`/login`).
   - Разграничение прав: админ может добавлять товары, кассир — только продажи.

2. **Управление товарами**:
   - CRUD (создание, чтение, обновление, удаление).
   - Поиск по названию/артикулу.

3. **Продажи**:
   - POS-интерфейс с выборкой товаров.
   - Расчет суммы, обновление остатков.

4. **Отчеты**:
   - Ежедневная выручка (`/reports/daily`).
   - Остатки на складе (`/reports/stock`).

---

### **9. Запуск и тестирование**
1. Создайте базу данных:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   ```
2. Запустите приложение:
   ```bash
   flask run
   ```
3. Проверьте основные сценарии:
   - Добавление товара.
   - Оформление продажи.
   - Просмотр отчетов.

---

### **10. Дополнительные улучшения**
- Добавьте валидацию форм (например, запрет отрицательного количества).
- Реализуйте экспорт данных в Excel (используйте `pandas`).
- Настройте простой CI/CD для деплоя на Heroku/VPS.

---

### Итог
Вы разработали MVP за 10 шагов! Теперь у вас есть базовая система учета с:
- Управлением товарами.
- Оформлением продаж.
- Отчетами.
- Аутентификацией пользователей.

Далее можно добавлять функции из списка полного функционала, например, интеграцию со сканером штрих-кодов или CRM.
