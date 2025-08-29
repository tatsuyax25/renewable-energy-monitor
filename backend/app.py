from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from datetime import datetime, timedelta
import random

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

def get_solar_potential(lat=37.7749, lon=-122.4194):
  """Calculate solar potential based on weather data"""
  try:
    # Using free OpenWeatherMap API (requires API key)
    # For demo, using simulated data based on time of day
    hour = datetime.now().hour
    if 6 <= hour <= 18:  # Daylight hours
      base_solar = 800 * (1 - abs(hour - 12) / 6)  # Peak at noon
      weather_factor = random.uniform(0.7, 1.0)  # Weather variability
      return max(0, base_solar * weather_factor)
    return 0
  except:
    return random.uniform(0, 800)

@app.route('/api/energy-data', methods=['GET'])
def get_energy_data():
  data = {
    'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'consumption': [120, 180, 250, 320, 450, 580, 720, 680, 520, 380, 220, 150],
    'production': [180, 280, 420, 580, 720, 850, 920, 880, 650, 480, 280, 200],
  }
  return jsonify(data)

@app.route('/api/real-time', methods=['GET'])
def get_real_time_data():
  current_solar = get_solar_potential()
  current_consumption = random.uniform(50, 200)
  
  data = {
    'timestamp': datetime.now().isoformat(),
    'solar_production': round(current_solar, 1),
    'consumption': round(current_consumption, 1),
    'net_energy': round(current_solar - current_consumption, 1),
    'carbon_saved': round(current_solar * 0.0004, 2),  # kg CO2 per kWh
    'cost_savings': round(current_solar * 0.12, 2)  # $0.12 per kWh
  }
  return jsonify(data)

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
  # Generate last 7 days of data
  days = []
  for i in range(7):
    date = datetime.now() - timedelta(days=i)
    solar = random.uniform(400, 800)
    consumption = random.uniform(300, 600)
    days.append({
      'date': date.strftime('%Y-%m-%d'),
      'solar': round(solar, 1),
      'consumption': round(consumption, 1),
      'savings': round((solar - consumption) * 0.12, 2)
    })
  
  total_savings = sum(day['savings'] for day in days)
  total_carbon_saved = sum(day['solar'] * 0.0004 for day in days)
  
  return jsonify({
    'daily_data': list(reversed(days)),
    'weekly_summary': {
      'total_savings': round(total_savings, 2),
      'carbon_saved': round(total_carbon_saved, 2),
      'efficiency': round((sum(day['solar'] for day in days) / sum(day['consumption'] for day in days)) * 100, 1)
    }
  })

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=False)