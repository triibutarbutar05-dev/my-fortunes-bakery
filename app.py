from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'myfortunes_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_myfortunes"
)

@app.route('/')
def home():
    return "My Fortunes Bakery"

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
        (nama,email,password)
        VALUES (%s,%s,%s)
        """

        cursor.execute(
            sql,
            (nama,email,hashed_password)
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

                return redirect('/dashboard')

        return "Email atau Password Salah"

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    return f"Selamat Datang, {session['nama']}"


@app.route('/add_product', methods=['GET', 'POST'])
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

        return "Produk Berhasil Ditambahkan"

    cursor.execute(
        "SELECT * FROM categories"
    )

    categories = cursor.fetchall()

    return render_template(
        'add_product.html',
        categories=categories
    )



@app.route('/products')
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

if __name__ == '__main__':
    app.run(debug=True)