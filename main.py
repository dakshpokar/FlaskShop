from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html', home = True)

@app.route('/products/<product_id>')
def product(product_id):
    return render_template('/product.html', product_id = product_id)

@app.route('/about')
def about():
    return render_template('/about.html')
@app.route('/products')
def products():
    return render_template('/products.html')

@app.route('/add-product')
def addProduct():
    return render_template('/add_product.html')

if __name__ == '__main__':
    app.run(debug=True)