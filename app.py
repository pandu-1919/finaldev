from flask import Flask, render_template, request, redirect, url_for, session
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'change-this-secret'

# sample data
RESTAURANTS = [
    {"id": "r1", "name": "Spice Biryani", "cuisine": "Indian", "menu": [
        {"id": "m1", "name": "Chicken Biryani", "price": 220},
        {"id": "m2", "name": "Veg Biryani", "price": 160}
    ]},
    {"id": "r2", "name": "Pizza Palace", "cuisine": "Italian", "menu": [
        {"id": "m3", "name": "Margherita Pizza", "price": 299},
        {"id": "m4", "name": "Pepperoni Pizza", "price": 349}
    ]}
]


def get_restaurant(rid):
    for r in RESTAURANTS:
        if r['id'] == rid:
            return r
    return None


@app.route('/')
def index():
    return render_template('index.html', restaurants=RESTAURANTS)


@app.route('/restaurant/<rid>')
def restaurant(rid):
    r = get_restaurant(rid)
    if not r:
        return "Restaurant not found", 404
    return render_template('restaurant.html', restaurant=r)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    r_id = request.form.get('r_id')
    name = request.form.get('name')
    price = float(request.form.get('price', 0))

    cart = session.get('cart', [])
    cart.append({
        'cart_id': str(uuid4()),
        'item_id': item_id,
        'restaurant_id': r_id,
        'name': name,
        'price': price
    })
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
