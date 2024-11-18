import json
from flask import Flask, jsonify, request
from SQL_Manager import *

app = Flask(__name__)
SQL_database = SQL_Manager()
product_table_name = "Products"
factory = Factory()

@app.route('/products', methods=['GET'])
def get_products():
    try:
        table = SQL_database.get_table(product_table_name)
        payload = []
        for row in table:
            payload.append(str(row))

        return jsonify(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['POST'])
def create_product():
    # Get data
    product = json.loads(request.data)


    convertet_product = factory.create_class("Product", name = product['ProductName'], price = product['Price'], stock = product['StockQuantity'])

    SQL_database.add_item(convertet_product)

    return '', 201, { 'location' : f'/products/'}

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


   
