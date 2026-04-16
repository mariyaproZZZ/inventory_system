from flask import Flask, render_template, request, redirect, url_for
import database
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    items = database.get_all_items()
    low_stock = database.get_low_stock(10)  # товары с количеством меньше 10
    total_value = database.get_total_value()  # общая стоимость
    return render_template('index.html',
                         items=items,
                         low_stock=low_stock,
                         total_value=total_value,
                         now=datetime.now())

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    database.add_item(name, quantity, price)
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    database.update_item(item_id, quantity, price)
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    database.delete_item(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)