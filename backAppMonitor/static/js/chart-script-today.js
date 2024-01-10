// Función para crear el gráfico de líneas
function createLineChart(context, data) {
    const labels = data.data.labels;
    const datasetData = data.data.data;
    console.log(datasetData)

    const chartData = {
        labels: labels,
        datasets: [
            {
                label: data.data.name,  // Deberías usar data.data.name en lugar de labels
                data: datasetData,
                borderWidth: 2,
                fill: false,
                tension: 0,
                pointRadius: 0,
                pointHoverRadius: 7,
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
            },
        ],
    };

    const chartConfig = {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            display: false,
        },
        scales: {
            x: {
                title: { // Agrega un nombre al eje Y
                    display: true,
                    text: "HRS"
                },
                type: "time",
                time: {
                    unit: "hour",
                    stepSize: 1,
                    displayFormats: {
                        hour: "HH:00"
                    },

                },
            },

            y: {
                beginAtZero: false,
                title: { // Agrega un nombre al eje Y
                    display: true,
                    text: data.data.unit
                },
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function (value, index, ticks) {
                        return value;
                    },
                },
            },
        },
    };

    new Chart(context, {
        type: "line",
        data: chartData,  // Cambia 'data' a 'chartData'
        options: chartConfig,  // Cambia 'option' a 'options'
    });
}

// Función para cargar los datos del gráfico
function loadChartData() {
    return {
        data: JSON.parse(document.getElementById("chart_0").getAttribute("data-var")),
    };
}


// Función principal que se ejecuta cuando se carga la página
window.onload = function () {
    const ctx0 = document.getElementById("chart_0").getContext("2d");

    // Cargar los datos del gráfico de forma asíncrona
    const chartData = loadChartData();

    // Crear el gráfico con los datos cargados
    createLineChart(ctx0, chartData);

};
