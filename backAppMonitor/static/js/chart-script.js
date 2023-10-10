// Función para crear el gráfico de líneas
function createLineChart(context, data) {

    new Chart(context, {
        type: "line",
        data: {
            labels: data.data1.labels,
            datasets: [
                {
                    label: data.data1.name,
                    data: data.data1.data,
                    borderWidth: 1,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    pointHoverRadius: 7,
                },
                {
                    label: data.data2.name,
                    data: data.data2.data,
                    borderWidth: 1,
                    fill: false,
                    tension: 0,
                    pointRadius: 0,
                    pointHoverRadius: 7,
                },
                {
                    label: data.data3.name,
                    data: data.data3.data,
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
        data1: JSON.parse(document.getElementById("chart_0").getAttribute("data-var1")),
        data2: JSON.parse(document.getElementById("chart_0").getAttribute("data-var2")),
        data3: JSON.parse(document.getElementById("chart_0").getAttribute("data-var3")),
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
