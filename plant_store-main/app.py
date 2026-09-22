from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret"

os.makedirs('static/uploads', exist_ok=True)

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            quantity INTEGER,
            category TEXT,
            image TEXT
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        phone TEXT,
        total REAL,
        payment TEXT
    )
    ''')


    conn.commit()
    conn.close()

    

# ---------------- HOME ----------------
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    category = request.args.get('category')

    if category:
        cursor.execute("SELECT * FROM plants WHERE category=?", (category,))
    else:
        cursor.execute("SELECT * FROM plants")

    plants = cursor.fetchall()
    conn.close()

    return render_template('index.html', plants=plants)

# ---------------- ADD ----------------
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    category = request.form['category']
    image = request.files['image']

    filename = secure_filename(image.filename)
    image.save(os.path.join('static/uploads', filename))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO plants (name, price, quantity, category, image) VALUES (?, ?, ?, ?, ?)",
        (name, price, quantity, category, filename)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM plants")
    plants = cursor.fetchall()

    conn.close()

    return render_template('admin.html', plants=plants)

# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM plants WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/admin')

# ---------------- CART ----------------
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(id)
    session.modified = True

    return redirect('/')

@app.route('/cart')
def cart():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cart_items = session.get('cart', [])
    plants = []
    total = 0

    for item in cart_items:
        cursor.execute("SELECT * FROM plants WHERE id=?", (item,))
        plant = cursor.fetchone()

        if plant:
            plants.append(plant)
            total += plant[2]   # ✅ correct total

    conn.close()

    return render_template('cart.html', plants=plants, total=total)

@app.route('/orders')
def orders():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()

    conn.close()

    return render_template('orders.html', orders=orders)

@app.route('/recommend')
def recommend():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cart = session.get('cart', [])
    max_price = request.args.get('price')

    if max_price:
        max_price = int(max_price)   # 🔥 FIX HERE

    if cart:
        last_id = cart[-1]

        cursor.execute("SELECT category, price FROM plants WHERE id=?", (last_id,))
        result = cursor.fetchone()

        if result:
            category, price = result

            if max_price:
                cursor.execute("""
                    SELECT * FROM plants 
                    WHERE category=? AND price<=?
                    ORDER BY RANDOM() LIMIT 6
                """, (category, max_price))
            else:
                cursor.execute("""
                    SELECT * FROM plants 
                    WHERE category=?
                    ORDER BY RANDOM() LIMIT 6
                """, (category,))
        else:
            cursor.execute("SELECT * FROM plants ORDER BY RANDOM() LIMIT 6")

    else:
        if max_price:
            cursor.execute("SELECT * FROM plants WHERE price<=?", (max_price,))
        else:
            cursor.execute("SELECT * FROM plants ORDER BY RANDOM() LIMIT 6")

    plants = cursor.fetchall()
    conn.close()

    return render_template('recommend.html', plants=plants)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    payment = request.form['payment']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    total = 0
    cart_items = session.get('cart', [])

    # ✅ CALCULATE TOTAL BEFORE closing DB
    for item in cart_items:
        cursor.execute("SELECT price FROM plants WHERE id=?", (item,))
        result = cursor.fetchone()

        if result:
            total += result[0]

    # ✅ INSERT ORDER
    cursor.execute(
        "INSERT INTO orders (name, address, phone, total, payment) VALUES (?, ?, ?, ?, ?)",
        (name, address, phone, total, payment)
    )

    conn.commit()
    conn.close()   # ✅ CLOSE ONLY AT END

    session['cart'] = []

    return redirect('/orders')

@app.route('/delete_order/<int:id>')
def delete_order(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/orders')

@app.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    if 'cart' in session:
        if id in session['cart']:
            session['cart'].remove(id)
            session.modified = True

    return redirect('/cart')

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    category = request.form['category']

    file = request.files['image']
    filename = secure_filename(file.filename)
    file.save('static/uploads/' + filename)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO plants (name, price, quantity, category, image) VALUES (?, ?, ?, ?, ?)",
        (name, price, quantity, category, filename)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')

@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM plants WHERE id=?", (id,))
    plant = cursor.fetchone()

    conn.close()

    return render_template('edit.html', plant=plant)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    category = request.form['category']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE plants 
        SET name=?, price=?, quantity=?, category=? 
        WHERE id=?
    """, (name, price, quantity, category, id))

    conn.commit()
    conn.close()

    return redirect('/admin')

# ---------------- RUN ----------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)