const charts = [
    ["api/submissions", "submission_timeline"],
    ["api/submission_heatmap", "submission_heatmap"],
    ["api/grading_distribution", "grading_dist"],
    ["api/starting_time_effect_on_grading", "starting_time_effect_on_grading"],
];

$(document).ready(function () {
    $('.datepicker').datepicker({
        format: 'dd/mm/yyyy',
        autoclose: true,
        todayHighlight: true
    });
});

async function getGeneral() {
    fetch('api/general')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#summary-table tbody");
            tbody.innerHTML = "";

            data.forEach(([key, label, value]) => {
                if (key === 'first_submission_date') {
                    $('#start-date').datepicker('setDate', value.split(' ')[0]);
                }
                if (key === 'last_submission_date') {
                    $('#end-date').datepicker('setDate', value.split(' ')[0]);
                }
                // language=HTML
                const row = `
                    <tr>
                        <td>${label}</td>
                        <td>${value}</td>
                    </tr>
                `;
                tbody.insertAdjacentHTML('beforeend', row);
            })

        })
        .catch(err => console.error("Error loading summary:", err));
}

async function getChart(endpoint, chartId) {
    try {
        let response = await fetch(endpoint);
        let spec = await response.json();
        spec.config.background = "none";
        spec.config.font = "Open Sans";
        spec.width = 700;
        spec.interactive = true;
        spec


        const chartOptions = {
            config: {
                axis: {
                    labelColor: "#ffffff",
                    titleColor: "#ffffff",
                    gridColor: "#444444",
                },
                title: {
                    anchor: "start",
                    color: "#ffffff"
                },
                legend: {
                    fontSize: 100,
                    labelColor: "#ffffff",
                    titleColor: "#ffffff"
                },
                header: {
                    labelColor: "#ffffff",        // ← Change facet label color
                    labelFontSize: 14,
                    labelFontWeight: "bold",
                    titleColor: "#ffffff",        // If you use facet titles
                    titleFontSize: 16
                },
                range: {
                    category: ['#f72585', '#7209b7', '#4361ee'], // pastel red, blue, green
                    //heatmap: ['#f72585', '#7209b7', '#4361ee']
                },
                // mark: {
                //     type: 'arc',
                //     tooltip: true,
                //     stroke: '#1e1e2f',
                //     strokeWidth: 2
                // },
            }
        };

        vegaEmbed(`#${chartId}`, spec, chartOptions);
    } catch (error) {
        console.log(`Error getting chart ${chartId}`, error);
    }
}

function updateCharts() {
    let startDate = document.getElementById("start_date").value;
    let endDate = document.getElementById("end_date").value;

    if (!startDate || !endDate) {
        alert("Please select both start and end dates.");
    }

    charts.forEach(([url, id]) => getChart(`${url}?start_date=${startDate}&end_date=${endDate}`, id));
}

getGeneral()

charts.forEach(([url, id]) => getChart(url, id));