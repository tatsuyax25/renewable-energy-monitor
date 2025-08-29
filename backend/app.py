# Import required libraries
from flask import Flask, jsonify, send_from_directory  # Flask web framework
from flask_cors import CORS  # Cross-Origin Resource Sharing for API access
import os  # Operating system interface
import requests  # HTTP library for API calls (future use)
from datetime import datetime, timedelta  # Date and time handling
import random  # Random number generation for mock data

# Initialize Flask application
# static_folder: Points to frontend directory for serving HTML/CSS/JS files
# static_url_path: Makes static files available at root URL
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Enable CORS (Cross-Origin Resource Sharing)
# This allows the frontend to make API calls to the backend
CORS(app)

# ROUTE 1: Serve the main dashboard page
@app.route('/')
def serve_frontend():
    """Serves the main index.html file when users visit the root URL"""
    return send_from_directory(app.static_folder, 'index.html')

# ROUTE 2: Serve static files (CSS, JS, images)
@app.route('/<path:path>')
def serve_static(path):
    """Serves CSS, JavaScript, and other static files from frontend folder"""
    return send_from_directory(app.static_folder, path)

# HELPER FUNCTION: Calculate solar energy production
def get_solar_potential(lat=37.7749, lon=-122.4194):
    """Calculate solar potential based on time of day and weather simulation
    
    Args:
        lat (float): Latitude coordinate (default: San Francisco)
        lon (float): Longitude coordinate (default: San Francisco)
    
    Returns:
        float: Solar energy production in kWh
    """
    try:
        # Get current hour (0-23)
        hour = datetime.now().hour
        
        # Solar panels only produce energy during daylight hours (6 AM - 6 PM)
        if 6 <= hour <= 18:
            # Calculate base solar production with peak at noon (hour 12)
            # Formula creates a bell curve: maximum at noon, decreasing toward sunrise/sunset
            base_solar = 800 * (1 - abs(hour - 12) / 6)
            
            # Simulate weather impact (clouds, rain, etc.)
            # Random factor between 0.7-1.0 (70%-100% efficiency)
            weather_factor = random.uniform(0.7, 1.0)
            
            # Return calculated solar production (never negative)
            return max(0, base_solar * weather_factor)
        
        # No solar production at night
        return 0
    except:
        # Fallback: return random value if calculation fails
        return random.uniform(0, 800)

# API ENDPOINT 1: Monthly energy data for charts
@app.route('/api/energy-data', methods=['GET'])
def get_energy_data():
    """Returns monthly energy consumption and production data for the main chart
    
    Returns:
        JSON: Object containing months, consumption, and production arrays
    """
    # Mock data representing a full year of energy data
    # In a real application, this would come from a database or external API
    data = {
        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        # Energy consumption typically higher in summer (AC) and winter (heating)
        'consumption': [120, 180, 250, 320, 450, 580, 720, 680, 520, 380, 220, 150],
        # Solar production higher in summer months (more sunlight)
        'production': [180, 280, 420, 580, 720, 850, 920, 880, 650, 480, 280, 200],
    }
    # Convert Python dictionary to JSON format for frontend
    return jsonify(data)

# API ENDPOINT 2: Real-time energy metrics
@app.route('/api/real-time', methods=['GET'])
def get_real_time_data():
    """Returns current energy metrics updated in real-time
    
    Returns:
        JSON: Current solar production, consumption, savings, and environmental impact
    """
    # Get current solar production based on time of day
    current_solar = get_solar_potential()
    
    # Simulate current energy consumption (varies throughout the day)
    # Typical household: 50-200 kWh depending on appliances, time of day
    current_consumption = random.uniform(50, 200)
    
    # Calculate real-time metrics
    data = {
        # ISO format timestamp for precise time tracking
        'timestamp': datetime.now().isoformat(),
        
        # Current solar energy production (rounded to 1 decimal)
        'solar_production': round(current_solar, 1),
        
        # Current energy consumption (rounded to 1 decimal)
        'consumption': round(current_consumption, 1),
        
        # Net energy: positive = surplus, negative = deficit
        'net_energy': round(current_solar - current_consumption, 1),
        
        # Environmental impact: CO2 savings calculation
        # 0.0004 kg CO2 saved per kWh of renewable energy (EPA standard)
        'carbon_saved': round(current_solar * 0.0004, 2),
        
        # Financial savings: money saved by using solar instead of grid
        # $0.12 per kWh is average US electricity rate
        'cost_savings': round(current_solar * 0.12, 2)
    }
    
    return jsonify(data)

# API ENDPOINT 3: Weekly analytics and performance data
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Returns weekly energy analytics and performance summary
    
    Returns:
        JSON: Daily data for past 7 days plus weekly summary statistics
    """
    # Generate data for the last 7 days
    days = []
    
    # Loop through past 7 days (0 = today, 6 = week ago)
    for i in range(7):
        # Calculate date for each day
        date = datetime.now() - timedelta(days=i)
        
        # Generate realistic daily energy values
        # Solar: 400-800 kWh per day (varies by weather)
        solar = random.uniform(400, 800)
        # Consumption: 300-600 kWh per day (varies by usage)
        consumption = random.uniform(300, 600)
        
        # Store daily data
        days.append({
            'date': date.strftime('%Y-%m-%d'),  # Format: 2024-01-15
            'solar': round(solar, 1),
            'consumption': round(consumption, 1),
            # Daily savings = (solar - consumption) * electricity rate
            'savings': round((solar - consumption) * 0.12, 2)
        })
    
    # Calculate weekly summary statistics
    # Sum all daily savings for the week
    total_savings = sum(day['savings'] for day in days)
    
    # Calculate total CO2 saved this week
    total_carbon_saved = sum(day['solar'] * 0.0004 for day in days)
    
    # Calculate energy efficiency percentage
    # Efficiency = (total solar production / total consumption) * 100
    total_solar = sum(day['solar'] for day in days)
    total_consumption = sum(day['consumption'] for day in days)
    efficiency = (total_solar / total_consumption) * 100
    
    return jsonify({
        # Reverse list so most recent day appears first
        'daily_data': list(reversed(days)),
        
        # Weekly summary for dashboard cards
        'weekly_summary': {
            'total_savings': round(total_savings, 2),      # Total $ saved
            'carbon_saved': round(total_carbon_saved, 2),   # Total kg CO2 saved
            'efficiency': round(efficiency, 1)              # Energy efficiency %
        }
    })

# APPLICATION STARTUP
if __name__ == '__main__':
    # Get port from environment variable (for deployment) or use 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    
    # Start the Flask application
    # host='0.0.0.0': Accept connections from any IP (required for deployment)
    # port: Use environment port or 5000 for local development
    # debug=False: Disable debug mode for production (security)
    app.run(host='0.0.0.0', port=port, debug=False)