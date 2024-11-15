import json
from flask import Flask, jsonify, request
app = Flask(__name__)


products = [
    {'id' : 1, 'name' : 'Niki shoe'},
    {'id' : 2, 'name' : 'Blue jeans'}
]

def product_is_valid(product):
    for key in product.keys():
        if(key != 'name'):
            return False
    return True

def get_Product(id : int):
    return next((p for p in products if e['id'] == id), None)

@app.route('/products', methods=['GET'])
def get_Products():
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    global nextProductId
    product = json.loads(request.data)
    if not product_is_valid(product):
        return jsonify({'error' : ' Invalid product propertoes'}), 400

    product['id'] = nextProductId
    nextProductId += 1
    products.append(product)

    return '', 201, { 'location' : '/products/{}'.format(product[id])}

@app.route('/products/<int:ud>', methods=['PUT'])    
def update_product(id : int):
    product = get_Product(id)
    if product is None:
        return jsonify({'error' : 'Product does not exits'}), 404
    
    update_product = json.loads(request.data)
    if not product_is_valid(update_product):
        return jsonify({'error' : 'Invalid product properties'}), 404
    
    product.update(update_product)

    return jsonify(product)

@app.route('/products/<int:ud>', methods=['DELETE'])
def delete_product(id):
    global products
    product = get_Product(id)
    if product is None:
        return jsonify({'error', 'Product does not exits'}), 404

    products = [p for p in products if e['id'] != id]
    return jsonify(product), 200    


if __name__ == '__main__':
   app.run(port=5000)
