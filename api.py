from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(name)

uri = "mongodb+srv://rahmatahlin:rahmat002@cluster-rahmat.a600y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-Rahmat"

# Koneksi ke MongoDB (ganti dengan URL MongoDB jika di server lain)
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sensor_db"]
collection = db["sensor_data"]

@app.route('/store', methods=['POST'])
def store_data():
    try:
        data = request.json  # Terima data dalam format JSON
        collection.insert_one(data)  # Simpan ke MongoDB
        return jsonify({"message": "Data stored successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True)