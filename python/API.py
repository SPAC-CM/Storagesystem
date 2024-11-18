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
        # Get tabæe
        table = SQL_database.get_table(product_table_name)

        # Collect data
        payload = []
        for row in table:
            payload.append(str(row))

        # Return
        return jsonify(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['POST'])
def create_product():
    # Get data
    product = json.loads(request.data)

    # Check of item with name exits
    found_item = SQL_database.get_item(table_name="product", parametor="name", item_value=str(product['ProductName']))
    print(found_item)
    if not found_item:
        # Convert to Product obj, to put in database
        convertet_product = factory.create_class("Product", name = product['ProductName'], price = product['Price'], stock = product['StockQuantity'])

        # Add to database
        SQL_database.add_item(convertet_product)

        return '', 201, { 'location' : f'/products/'}
    else:
        return '', 200, { 'Report_message' : f'Item_already_exits'}


@app.route('/products/<int:ud>', methods=['PUT'])    
def update_product(id : int):
    # Check for id
    product = SQL_database.get_item(product_table_name, "id", id)    
    if not product:
        return jsonify({'error' : 'Product does not exits'}), 404
    
    # Get update data
    update_product = json.loads(request.data)
    if not product_is_valid(update_product):
        return jsonify({'error' : 'Invalid product properties'}), 404
    
    # Update
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


   
