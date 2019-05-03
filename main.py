from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/products/<product_id>')
def product(product_id):
    return render_template('/product.html', product_id = product_id)

if __name__ == '__main__':
    app.run(debug=True)