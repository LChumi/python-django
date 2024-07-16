document.addEventListener('DOMContentLoaded', (event) => {
    let tiempos = [];
    let valores = [];

    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: tiempos,
            datasets: [{
                label: 'Temperatura (°C)',
                data: valores,
                borderColor: 'red',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Tiempo (h)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Temperatura (°C)'
                    }
                }
            }
        }
    });

    function actualizarGrafica(data) {
        tiempos = data.tiempos;
        valores = data.valores;
        myChart.data.labels = tiempos;
        myChart.data.datasets[0].data = valores;
        myChart.update();
    }

    function iniciarSimulacion() {
        // Solo empieza a hacer solicitudes si la simulación no ha sido reiniciada
        const intervalo = setInterval(() => {
            fetch('/get-data/')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        clearInterval(intervalo); // Detener el intervalo si hay un error
                    } else {
                        actualizarGrafica(data);
                    }
                });
        }, 1000);
    }

    function reiniciar() {
        fetch('/reiniciar/')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'reiniciado') {
                    tiempos = [];
                    valores = [];
                    myChart.data.labels = tiempos;
                    myChart.data.datasets[0].data = valores;
                    myChart.update();
                }
            });
    }

    document.getElementById('iniciarSimulacion').addEventListener('click', iniciarSimulacion);
    document.getElementById('reiniciar').addEventListener('click', reiniciar);
});
