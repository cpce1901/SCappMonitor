// Función para crear el gráfico de líneas
function createLineChart(context, data) {

    new Chart(context, {
        type: "line",
        data: {
            labels: data.data.labels,
            datasets: [
                {
                    label: data.data.name,
                    data: data.data.data,
                    borderWidth: 1,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    pointHoverRadius: 7,
                },
                
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                },
            },
        },
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
