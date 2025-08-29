document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById("energyChart").getContext("2d");
  
  fetch('/api/energy-data')
    .then(response => response.json())
    .then(data => {
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.months,
          datasets: [
            {
              label: "Energy Consumption (kWh)",
              data: data.consumption,
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
            },
            {
              label: "Energy Production (kWh)",
              data: data.production,
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    })
    .catch(error => console.error('Error fetching data:', error));
});
