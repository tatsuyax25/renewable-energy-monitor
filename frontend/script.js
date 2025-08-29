// Global variables to store chart instances
// This allows us to update or destroy charts later if needed
let energyChart, analyticsChart;

/**
 * Updates the real-time metrics displayed in the dashboard cards
 * Fetches current data from the backend API and updates the UI
 */
function updateRealTimeMetrics() {
    // Make HTTP GET request to real-time API endpoint
    fetch('/api/real-time')
        .then(response => {
            // Convert response to JSON format
            return response.json();
        })
        .then(data => {
            // Update each metric card with new data
            // getElementById finds HTML elements by their ID attribute
            document.getElementById('currentSolar').textContent = data.solar_production;
            document.getElementById('currentConsumption').textContent = data.consumption;
            document.getElementById('netEnergy').textContent = data.net_energy;
            document.getElementById('carbonSaved').textContent = data.carbon_saved;
        })
        .catch(error => {
            // Log any errors to browser console for debugging
            console.error('Error fetching real-time data:', error);
        });
}

/**
 * Initializes both charts on the dashboard
 * Creates the monthly overview chart and weekly analytics chart
 */
function initializeCharts() {
    // CHART 1: Monthly Energy Overview (Line Chart)
    // Get the canvas element where the chart will be drawn
    const ctx1 = document.getElementById('energyChart').getContext('2d');
    
    // Fetch monthly data from backend API
    fetch('/api/energy-data')
        .then(response => response.json())
        .then(data => {
            // Create new Chart.js line chart
            energyChart = new Chart(ctx1, {
                type: 'line',  // Line chart shows trends over time
                data: {
                    // X-axis labels (months)
                    labels: data.months,
                    
                    // Chart datasets (lines on the graph)
                    datasets: [
                        {
                            label: 'Consumption',  // Legend label
                            data: data.consumption,  // Y-axis data points
                            borderColor: '#e74c3c',  // Red line color
                            backgroundColor: 'rgba(231, 76, 60, 0.1)',  // Light red fill
                            tension: 0.4,  // Curve smoothness (0 = straight lines, 1 = very curved)
                            fill: true  // Fill area under the line
                        },
                        {
                            label: 'Production',  // Legend label
                            data: data.production,  // Y-axis data points
                            borderColor: '#27ae60',  // Green line color
                            backgroundColor: 'rgba(39, 174, 96, 0.1)',  // Light green fill
                            tension: 0.4,  // Smooth curves
                            fill: true  // Fill area under the line
                        }
                    ]
                },
                options: {
                    responsive: true,  // Chart resizes with container
                    plugins: {
                        legend: {
                            position: 'top'  // Show legend at top of chart
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,  // Y-axis starts at 0
                            grid: {
                                color: 'rgba(0,0,0,0.1)'  // Light gray grid lines
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(0,0,0,0.1)'  // Light gray grid lines
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading monthly data:', error));

    // CHART 2: Weekly Analytics (Bar Chart)
    // Get the canvas element for the second chart
    const ctx2 = document.getElementById('analyticsChart').getContext('2d');
    
    // Fetch weekly analytics data from backend API
    fetch('/api/analytics')
        .then(response => response.json())
        .then(data => {
            // Create new Chart.js bar chart
            analyticsChart = new Chart(ctx2, {
                type: 'bar',  // Bar chart shows daily comparisons
                data: {
                    // X-axis labels: Convert date strings to readable format
                    // Example: "2024-01-15" becomes "1/15/2024"
                    labels: data.daily_data.map(d => new Date(d.date).toLocaleDateString()),
                    
                    datasets: [
                        {
                            label: 'Daily Savings ($)',  // Legend label
                            // Y-axis data: Extract savings value from each day
                            data: data.daily_data.map(d => d.savings),
                            backgroundColor: '#3498db',  // Blue bar color
                            borderColor: '#2980b9',      // Darker blue border
                            borderWidth: 1               // Border thickness
                        }
                    ]
                },
                options: {
                    responsive: true,  // Chart resizes with container
                    plugins: {
                        legend: {
                            display: false  // Hide legend (only one dataset)
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,  // Y-axis starts at 0
                            grid: {
                                color: 'rgba(0,0,0,0.1)'  // Light gray grid lines
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading analytics data:', error));
}

/**
 * Main application initialization
 * Runs when the HTML document is fully loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize both charts when page loads
    initializeCharts();
    
    // Load initial real-time data
    updateRealTimeMetrics();
    
    // Set up automatic updates every 5 seconds (5000 milliseconds)
    // This creates the "live data" effect by continuously fetching new metrics
    setInterval(updateRealTimeMetrics, 5000);
    
    console.log('Renewable Energy Monitor initialized successfully!');
});
