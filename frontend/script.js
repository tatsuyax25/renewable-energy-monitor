// Basic setup for a chart using Chart.js
document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById("energyChart").getContext("2d");
  new Chart(ctx, {
    type: "bar", // You can change this to 'line', 'pie', etc.
    data: {
      labels: [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ],
      datasets: [
        {
          label: "Energy Consumption (kWh)",
          data: [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200],
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
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
});
