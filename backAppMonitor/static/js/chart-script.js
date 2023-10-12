// Función para crear el gráfico de líneas
function createLineChart(context, data) {


    const { data1, data2, data3 } = data;



    const datasetData = {
        labels: data1.labels,
        datasets: [
            {
                label: data1.name,  // Deberías usar data.data.name en lugar de labels
                data: data1.data,
                borderWidth: 1.2,
                fill: false,
                tension: 0,
                pointRadius: 0,
                pointHoverRadius: 7,
                borderColor: "rgba(0, 129, 255, 1)",
                backgroundColor: "rgba(0, 129, 255, 0.2)",

            },
            {
                label: data2.name,  // Deberías usar data.data.name en lugar de labels
                data: data2.data,
                borderWidth: 1.2,
                fill: false,
                tension: 0,
                pointRadius: 0,
                pointHoverRadius: 7,
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
            },
            {
                label: data3.name,  // Deberías usar data.data.name en lugar de labels
                data: data3.data,
                borderWidth: 1.2,
                fill: false,
                tension: 0,
                pointRadius: 0,
                pointHoverRadius: 7,
                borderColor: "rgba(254, 192, 1, 1)",
                backgroundColor: "rgba(254, 192, 1, 0.2)",
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
                title: {
                    display: true,
                    text: "Time",
                },
                type: "time",
                time: {
                    unit: "day",
                    stepSize: 1,
                    displayFormats: {
                        day: "DD MMM",
                    },
                }
            },
            y: {
                beginAtZero: false,
                ticks: {
                },
            },
        },
    };


    new Chart(context, {
        type: "line",
        data: datasetData,
        options: chartConfig,
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
