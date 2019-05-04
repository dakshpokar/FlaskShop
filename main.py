from flask import Flask, request, render_template, url_for, flash, redirect
from flask import send_from_directory
import sqlite3 as sql
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from flask_mail import Mail, Message
import os

UPLOAD_FOLDER = UPLOADS_PATH = join(dirname(realpath(__file__)), 'product_image/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mailsender.420@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mailsender@420'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

def add_product(name, category, desc, rating, image_url, price):
    with sql.connect("database.db") as con:
        print("Opened database successfully")
        query = "INSERT INTO products (name, category, desc, rating, image_url, price) VALUES(\"" + name + "\", \"" + category + "\", \"" + desc + "\", " + rating + ", \"" + image_url + "\", " + price + ")"
        print(query)
        con.execute(query)
        con.commit()

@app.route('/')
def index():
    return render_template('/index.html', home = True)

@app.route('/product/<id>', methods=['GET', 'POST'])
def product(id):
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from products where id = " + id)
    rows = cur.fetchall()
    
    if request.method == "POST":
        msg = Message('FlaskShop - ' + rows[0]['name'] + ' details!', sender = 'yourId@gmail.com', recipients = [request.form["email"]])
        html_response = render_template('mail.html', row = rows[0])
        msg.html = html_response
        mail.send(msg)
        return redirect('/products')

    return render_template("messager.html", row = rows[0])



@app.route('/about')
def about():
    return render_template('/about.html')
@app.route('/products')
def products():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from products")
    rows = cur.fetchall()
    con.close()
    return render_template('/products.html', rows = rows, search_item = None)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/add-product', methods=['GET', 'POST'])
def addProduct():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        desc = request.form["desc"]
        rating = request.form["rating"]
        price = request.form["price"]
        
        if 'image' not in request.files:
            flash('No file part')
            print("ikde ala")
            #return redirect(request.url)
        file = request.files['image']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(url_for('uploaded_file', filename=filename))
            add_product(name, category, desc, rating, url_for('uploaded_file', filename=filename), price)
            return render_template('/add_product.html')
        add_product(name, category, desc, rating, '/product_image/default_product.jpg', price)
    return render_template('/add_product.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get("query")
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from products where name like " + "\"%"  + query + "%\"")
    rows = cur.fetchall()
    con.close()
    return render_template('/products.html', rows = rows, search_item = query)

app.secret_key = '#include<iostream.h>'

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)