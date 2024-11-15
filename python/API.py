import json
from flask import Flask, jsonify, request
from SQL_Manager import *
app = Flask(__name__)

SQL_database = SQL_Manager()
product_table_name = "Products"


def product_is_valid(product):
    for key in product.keys():
        if(key != 'name'):
            return False
    return True

def get_Product(id : int):
    return next((p for p in products if e['id'] == id), None)

@app.route('/products', methods=['GET'])
def get_products():
    try:
        print(SQL_database.get_table(product_table_name))
        return jsonify(SQL_database.get_table(product_table_name))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['POST'])
def create_product():
    product = json.loads(request.data)
    if not product_is_valid(product):
        return jsonify({'error' : ' Invalid product propertoes'}), 400

    curretID = len(products) + 1 #Placeholder for making id
    product['id'] = curretID
    products.append(product)

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


   
