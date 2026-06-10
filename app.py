from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector
import os
from flask import send_from_directory
from flask import flash

app = Flask(__name__)
app.secret_key = 'myfortunes_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect('/login')

        if session['role'] != 'admin':
            return "Akses ditolak!"

        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect('/login')

        if session['role'] != 'admin':
            return "Akses ditolak!"

        return f(*args, **kwargs)

    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' not in session:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cursor = db.cursor()

        sql = """
        INSERT INTO users
        (nama,email,password,role)
        VALUES (%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (nama,email,hashed_password, 'user')
        )

        db.commit()

        return "Register Berhasil!"

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user:

            if check_password_hash(
                user['password'],
                password
            ):

                session['user_id'] = user['id']
                session['nama'] = user['nama']
                session['role'] = user['role']

                return redirect(url_for('dashboard'))

        flash('Email atau Password Salah', 'danger')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'dashboard.html'
    )


@app.route('/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():

    cursor = db.cursor()

    if request.method == 'POST':

        nama_produk = request.form['nama_produk']
        category_id = request.form['category_id']
        harga = request.form['harga']
        stok = request.form['stok']
        deskripsi = request.form['deskripsi']

        gambar = request.files['gambar']

        filename = ''

        if gambar:
            filename = secure_filename(gambar.filename)

            gambar.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

        sql = """
        INSERT INTO products
        (
            category_id,
            nama_produk,
            harga,
            stok,
            deskripsi,
            gambar
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                category_id,
                nama_produk,
                harga,
                stok,
                deskripsi,
                filename
            )
        )

        db.commit()
        flash('Produk berhasil ditambahkan!')
        return redirect('/products')

    cursor.execute(
        "SELECT * FROM categories"
    )

    categories = cursor.fetchall()

    return render_template(
        'add_product.html',
        categories=categories
    )


@app.route('/products')
@admin_required
def products():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM products
    """)

    products = cursor.fetchall()

    return render_template(
        'products.html',
        products=products
    )

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):

    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':

        nama_produk = request.form['nama_produk']
        harga = request.form['harga']
        stok = request.form['stok']
        deskripsi = request.form['deskripsi']

        sql = """
        UPDATE products
        SET
            nama_produk=%s,
            harga=%s,
            stok=%s,
            deskripsi=%s
        WHERE id=%s
        """

        cursor.execute(
            sql,
            (
                nama_produk,
                harga,
                stok,
                deskripsi,
                id
            )
        )

        db.commit()

        return redirect('/products')

    cursor.execute(
        "SELECT * FROM products WHERE id=%s",
        (id,)
    )

    product = cursor.fetchone()

    return render_template(
        'edit_product.html',
        product=product
    )


@app.route('/delete_product/<int:id>')
@admin_required
def delete_product(id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect('/products')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )


@app.route('/catalog')
def catalog():

    category_id = request.args.get('category')

    cursor = db.cursor(dictionary=True)

    if category_id:
        cursor.execute("""
            SELECT *
            FROM products
            WHERE category_id = %s
        """, (category_id,))
    else:
        cursor.execute("""
            SELECT *
            FROM products
        """)

    products = cursor.fetchall()

    cursor.execute("""
        SELECT *
        FROM categories
    """)

    categories = cursor.fetchall()

    return render_template(
        'catalog.html',
        products=products,
        categories=categories,
        selected_category=category_id
    )

@app.route('/product/<int:id>')
def product_detail(id):

    cursor = db.cursor(dictionary=True)

    # Ambil produk
    cursor.execute(
        "SELECT * FROM products WHERE id=%s",
        (id,)
    )

    product = cursor.fetchone()

    # Ambil review
    cursor.execute(
        "SELECT * FROM reviews WHERE product_id=%s",
        (id,)
    )

    reviews = cursor.fetchall()

    return render_template(
        'product_detail.html',
        product=product,
        reviews=reviews
    )

@app.route('/custom-cake', methods=['GET', 'POST'])
@login_required
def custom_cake():

    cursor = db.cursor()

    if request.method == 'POST':

        user_id = session['user_id']

        ukuran = request.form['ukuran']
        rasa = request.form['rasa']
        tema = request.form['tema']
        tanggal_ambil = request.form['tanggal_ambil']
        catatan = request.form['catatan']

        gambar = request.files['gambar_referensi']

        filename = ''

        if gambar:
            filename = secure_filename(gambar.filename)

            gambar.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

        sql = """
        INSERT INTO custom_cakes
        (
            user_id,
            ukuran,
            rasa,
            tema,
            tanggal_ambil,
            catatan,
            gambar_referensi
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                user_id,
                ukuran,
                rasa,
                tema,
                tanggal_ambil,
                catatan,
                filename
            )
        )

        db.commit()

        return redirect('/custom-cake')

    return render_template('custom_cake.html')

@app.route('/order/<int:id>', methods=['POST'])
@login_required
def order_product(id):

    qty = int(request.form['qty'])

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM products WHERE id=%s",
        (id,)
    )

    product = cursor.fetchone()

    total = product['harga'] * qty

    # simpan ke orders
    user_id = session['user_id']
    sql_order = """
    INSERT INTO orders
    (user_id, total_harga)
    VALUES (%s, %s)
    """

    cursor.execute(
        sql_order, 
        (
            user_id,
            total
        )
    )

    order_id = cursor.lastrowid

    # simpan ke order_items
    sql_item = """
    INSERT INTO order_items
    (order_id, product_id, qty, subtotal)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(
        sql_item,
        (
            order_id,
            id,
            qty,
            total
        )
    )

    db.commit()

    return redirect('/orders')

@app.route('/orders')
@admin_required
def orders():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
        orders.id,
        orders.total_harga,
        orders.status,
        products.nama_produk,
        order_items.qty,
        users.nama
    FROM orders
    JOIN users
        ON orders.user_id = users.id
    JOIN order_items
        ON orders.id = order_items.order_id
    JOIN products
        ON order_items.product_id = products.id
    ORDER BY orders.id DESC
    """)

    orders = cursor.fetchall()

    return render_template(
        'orders.html',
        orders=orders
    )

@app.route('/update_order/<int:id>/<status>')
@admin_required
def update_order(id, status):

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status=%s
        WHERE id=%s
        """,
        (status, id)
    )

    db.commit()

    return redirect('/orders')

@app.route('/my-orders')
@login_required
def my_orders():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT DISTINCT
            orders.id,
            orders.total_harga,
            orders.status,
            orders.tanggal_order
        FROM orders
        WHERE orders.user_id = %s
        ORDER BY orders.id DESC
    """, (session['user_id'],))

    orders = cursor.fetchall()

    return render_template(
        'my_orders.html',
        orders=orders
    )

@app.route('/my-custom-cakes')
@login_required
def my_custom_cakes():

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM custom_cakes
        WHERE user_id=%s
        ORDER BY id DESC
        """,
        (session['user_id'],)
    )

    custom_cakes = cursor.fetchall()

    return render_template(
        'my_custom_cakes.html',
        custom_cakes=custom_cakes
    )

@app.route('/admin-custom-cakes')
@login_required
def admin_custom_cakes():

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            custom_cakes.*,
            users.nama
        FROM custom_cakes
        JOIN users
            ON custom_cakes.user_id = users.id
        ORDER BY custom_cakes.id DESC
    """)

    cakes = cursor.fetchall()

    return render_template(
        'admin_custom_cakes.html',
        cakes=cakes
    )

@app.route('/admin-custom-cake-detail/<int:id>')
@login_required
def admin_custom_cake_detail(id):

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            custom_cakes.*,
            users.nama
        FROM custom_cakes
        JOIN users
            ON custom_cakes.user_id = users.id
        WHERE custom_cakes.id = %s
    """, (id,))

    cake = cursor.fetchone()

    return render_template(
        'admin_custom_cake_detail.html',
        cake=cake
    )

@app.route('/update-custom-cake/<int:id>/<status>')
@login_required
def update_custom_cake(id, status):

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE custom_cakes
        SET status=%s
        WHERE id=%s
        """,
        (status, id)
    )

    db.commit()

    return redirect('/admin-custom-cakes')

@app.route('/cart')
@login_required
def cart():

    user_id = session['user_id']

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            cart.id,
            cart.qty,
            products.nama_produk,
            products.harga,
            products.gambar,
            (cart.qty * products.harga) as subtotal
        FROM cart
        JOIN products
            ON cart.product_id = products.id
        WHERE cart.user_id=%s
    """, (user_id,))

    carts = cursor.fetchall()
    total = sum(item['subtotal'] for item in carts)

    return render_template(
        'cart.html',
        carts=carts,
        total=total
    )

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):

    qty = int(request.form['qty'])
    user_id = session['user_id']

    cursor = db.cursor()

    # cek apakah produk sudah ada di keranjang
    cursor.execute("""
        SELECT * FROM cart
        WHERE user_id=%s AND product_id=%s
    """, (user_id, product_id))

    item = cursor.fetchone()

    if item:

        cursor.execute("""
            UPDATE cart
            SET qty = qty + %s
            WHERE user_id=%s AND product_id=%s
        """, (qty, user_id, product_id))

    else:

        cursor.execute("""
            INSERT INTO cart(user_id, product_id, qty)
            VALUES(%s,%s,%s)
        """, (user_id, product_id, qty))

    db.commit()

    return redirect('/cart')

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():

    if request.method == 'POST':

        nama_penerima = request.form['nama_penerima']
        no_hp = request.form['no_hp']
        alamat = request.form['alamat']
        catatan = request.form['catatan']

        bukti = request.files['bukti_pembayaran']

        nama_file = None

        if bukti and bukti.filename != '':
            nama_file = secure_filename(bukti.filename)
            bukti.save(os.path.join(
                app.config['UPLOAD_FOLDER'],
                nama_file
            ))

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                cart.product_id,
                cart.qty,
                products.harga
            FROM cart
            JOIN products
                ON cart.product_id = products.id
            WHERE cart.user_id=%s
        """, (session['user_id'],))

        carts = cursor.fetchall()

        if not carts:
            return redirect('/cart')

        total = sum(item['harga'] * item['qty'] for item in carts)

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO orders(
                user_id,
                total_harga,
                status,
                nama_penerima,
                no_hp,
                alamat,
                catatan,
                bukti_pembayaran
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            session['user_id'],
            total,
            'menunggu_verifikasi',
            nama_penerima,
            no_hp,
            alamat,
            catatan,
            nama_file
        ))

        order_id = cursor.lastrowid

        for item in carts:

            cursor.execute("""
                INSERT INTO order_items(
                    order_id,
                    product_id,
                    qty
                )
                VALUES(%s,%s,%s)
            """, (
                order_id,
                item['product_id'],
                item['qty']
            ))

        cursor.execute("""
            DELETE FROM cart
            WHERE user_id=%s
        """, (session['user_id'],))

        db.commit()

        return redirect('/my-orders')

    return render_template('checkout.html')

@app.route('/order-detail/<int:order_id>')
@login_required
def order_detail(order_id):

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE id=%s
        AND user_id=%s
    """, (
        order_id,
        session['user_id']
    ))

    order = cursor.fetchone()

    cursor.execute("""
        SELECT
            products.nama_produk,
            products.harga,
            order_items.qty
        FROM order_items
        JOIN products
            ON order_items.product_id = products.id
        WHERE order_items.order_id=%s
    """, (order_id,))

    items = cursor.fetchall()

    return render_template(
        'order_detail.html',
        order=order,
        items=items
    )

@app.route('/admin-order-detail/<int:order_id>')
@login_required
def admin_order_detail(order_id):

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM orders
        JOIN users ON orders.user_id = users.id
        WHERE orders.id = %s
    """, (order_id,))

    order = cursor.fetchone()

    cursor.execute("""
        SELECT
            products.nama_produk,
            products.harga,
            order_items.qty
        FROM order_items
        JOIN products
            ON order_items.product_id = products.id
        WHERE order_items.order_id = %s
    """, (order_id,))

    items = cursor.fetchall()

    return render_template(
        'admin_order_detail.html',
        order=order,
        items=items
    )

@app.route('/verifikasi-pembayaran/<int:order_id>')
@login_required
def verifikasi_pembayaran(order_id):

    cursor = db.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = 'diproses'
        WHERE id = %s
    """, (order_id,))

    db.commit()

    return redirect(f'/admin-order-detail/{order_id}')

@app.route('/review/<int:product_id>', methods=['GET', 'POST'])
def review(product_id):

    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu')
        return redirect('/login')

    cursor = db.cursor(dictionary=True)

    # ambil data produk
    cursor.execute(
        "SELECT * FROM products WHERE id=%s",
        (product_id,)
    )

    product = cursor.fetchone()

    if request.method == 'POST':

        rating = request.form['rating']
        komentar = request.form['komentar']

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO reviews
            (
                user_id,
                product_id,
                rating,
                komentar
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            session['user_id'],
            product_id,
            rating,
            komentar
        ))

        db.commit()

        flash('Review berhasil dikirim!')

        return redirect(f'/product/{product_id}')

    return render_template(
        'review.html',
        product=product
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)