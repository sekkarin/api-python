from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated in-memory database
data = []
# Create - Add a new item
@app.route('/items', methods=['POST'])
def create_item():
    item = request.json
    if not item.get('id') or not item.get('name'):
        return jsonify({'error': 'ID and Name are required fields.'}), 400

    # Check if the ID already exists
    for existing_item in data:
        if existing_item['id'] == item['id']:
            return jsonify({'error': 'Item with this ID already exists.'}), 400

    data.append(item)
    return jsonify({'message': 'Item created successfully', 'item': item}), 201

# Read - Get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data), 200

# Read - Get a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item), 200

# Update - Modify an existing item by ID
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    updates = request.json
    item.update(updates)
    return jsonify({'message': 'Item updated successfully', 'item': item}), 200

# Delete - Remove an item by ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({'message': 'Item deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=80)
