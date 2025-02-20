from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://ganeshsriramulu2:Ganesh73005@cluster0.a4zpgcx.mongodb.net/buildingDB?retryWrites=true&w=majority"
mongo = PyMongo(app)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buildings', methods=['GET'])
def get_buildings():
    buildings = list(mongo.db.buildings.find({}, {'_id': 0}))
    return jsonify(buildings)

@app.route('/buildings/<name>', methods=['PUT'])
def update_building(name):
    try:
        state = request.json.get('state')
        if not state:
            return jsonify({'error': 'State is required'}), 400
        
        result = mongo.db.buildings.update_one(
            {'name': name}, 
            {'$set': {'state': state}}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Building not found'}), 404
            
        return jsonify({'status': 'success', 'message': f'Building {name} state updated to {state}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)