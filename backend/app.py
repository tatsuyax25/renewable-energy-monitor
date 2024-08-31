from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend')
CORS(app) # Enable CORS to allow communication with front-end

@app.route('/')
def serve_frontend():
  return send_from_directory(app.static_folder, 'index.html')

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