let energyChart, analyticsChart;

function updateRealTimeMetrics() {
  fetch('/api/real-time')
    .then(response => response.json())
    .then(data => {
      document.getElementById('currentSolar').textContent = data.solar_production;
      document.getElementById('currentConsumption').textContent = data.consumption;
      document.getElementById('netEnergy').textContent = data.net_energy;
      document.getElementById('carbonSaved').textContent = data.carbon_saved;
    })
    .catch(error => console.error('Error fetching real-time data:', error));
}

function initializeCharts() {
  // Monthly Energy Chart
  const ctx1 = document.getElementById('energyChart').getContext('2d');
  fetch('/api/energy-data')
    .then(response => response.json())
    .then(data => {
      energyChart = new Chart(ctx1, {
        type: 'line',
        data: {
          labels: data.months,
          datasets: [
            {
              label: 'Consumption',
              data: data.consumption,
              borderColor: '#e74c3c',
              backgroundColor: 'rgba(231, 76, 60, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: 'Production',
              data: data.production,
              borderColor: '#27ae60',
              backgroundColor: 'rgba(39, 174, 96, 0.1)',
              tension: 0.4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            },
            x: {
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            }
          }
        }
      });
    });

  // Analytics Chart
  const ctx2 = document.getElementById('analyticsChart').getContext('2d');
  fetch('/api/analytics')
    .then(response => response.json())
    .then(data => {
      analyticsChart = new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: data.daily_data.map(d => new Date(d.date).toLocaleDateString()),
          datasets: [
            {
              label: 'Daily Savings ($)',
              data: data.daily_data.map(d => d.savings),
              backgroundColor: '#3498db',
              borderColor: '#2980b9',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0,0,0,0.1)'
              }
            }
          }
        }
      });
    });
}

document.addEventListener('DOMContentLoaded', function() {
  initializeCharts();
  updateRealTimeMetrics();
  
  // Update real-time data every 5 seconds
  setInterval(updateRealTimeMetrics, 5000);
});
