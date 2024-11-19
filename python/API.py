import json
from flask import Flask, jsonify, request
from SQL_Manager import *

app = Flask(__name__)
SQL_database = SQL_Manager("root", "bWsEocb2r706!", "127.0.0.1")
product_table_name = "Products"
factory = Factory()

@app.route('/products', methods=['GET'])
def get_products():
    try:
        # Get table
        table = SQL_database.get_table(product_table_name)

        # Collect data
        payload = []
        for row in table:
            payload.append(str(row))

        # Return
        return jsonify(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get specifick item
@app.route('/products_item_name', methods=['GET'])
def get_product_by_name():
    try:
        return jsonify(str(SQL_database.get_item(table_name = "product", parametor = "name", item_value = str(request.args.get("name")))))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get specifick item
@app.route('/products_item_id', methods=['GET'])
def get_product_by_id():
    try:
        return jsonify(str(SQL_database.get_item(table_name = "product", parametor = "id", item_value = str(request.args.get("id")))))
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


@app.route('/products_update_all', methods=['PUT'])    
def update_product():
    try:
        # Read form data
        product_id = request.form.get('id', type=int)
        name = request.form.get('name')
        price = request.form.get('price', type=float)
        stock = request.form.get('stock', type=int)

        # Read JSON data
        json_data = request.get_json(silent=True)
        if json_data:
            product_id = json_data.get('id')
            name = json_data.get('name')
            price = json_data.get('price')
            stock = json_data.get('stock')

        # Process the data
        SQL_database.update_item(table_name = "Product", parametor = "id", 
            item_value = str(product_id), update_parametor = "name", update_value = str(name))
        SQL_database.update_item(table_name = "Product", parametor = "id", 
            item_value = str(product_id), update_parametor = "price", update_value = str(price))
        SQL_database.update_item(table_name = "Product", parametor = "id", 
            item_value = str(product_id), update_parametor = "stock", update_value = str(stock))

        # Return a response
        return jsonify({"message": "Product updated successfully"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/products_delete_id', methods=['DELETE'])
def delete_product():
    targetID = request.args.get("id")
    SQL_database.remove_item(table_name = "Product", parametor = "id", item_value = str(targetID))

    return jsonify(product), 200    


if __name__ == '__main__':
   app.run(port=5000)


   
