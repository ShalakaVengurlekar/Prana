const xValues = ["Jan", "Feb", "March", "April", "May (Predicted Value)"];
const yValues = [674.298, 606.86, 404.57, 708.01, 560.87];
const barColors = ["red", "green","blue","orange","brown"];
const myChart = new Chart("myChart", {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
        legend: {display: false},
        title: {
        display: true,
        text: "Carbon Footprint Emissions"
        }
    }
  });