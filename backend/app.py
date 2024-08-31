from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app) # Enable CORS to allow communication with front-end

# Route for serving the index.html (front-end)
@app.route('/')
def serve_frontend():
  return send_from_directory(app.static_folder, 'index.html')

# Route for serving the rest of the static files (e.g., CSS, JS)
@app.route('/<path:path>')
def serve_static(path):
  return send_from_directory(app.static_folder, path)

# Route for serving the mock energy data (API)
@app.route('/api/energy-data', methods=['GET'])
def get_energy_data():
  # Exaple mock data (replace this with real API later)
  data = {
    'months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'consumption': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
    'production': [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300],
  }
  return jsonify(data)

if __name__ == '__main__':
  app.run(debug=True)