const charts = [
    ["api/submissions", "submission_timeline"],
    ["api/submission_heatmap", "submission_heatmap"],
    ["api/last_grade_time_pie_chart", "last_grade_time_pie_chart"],
    ["api/starting_time_effect_on_grading", "starting_time_effect_on_grading"],
    ["api/grading_distribution", "grading_dist"],
    ["api/grade_improvement", "grade_improvement"],
    ["api/grade_by_submission_count_scatter", "grade_by_submission_count_scatter"],
];

const chartViews = {};

async function getChart(endpoint, chartId) {
    try {
        let response = await fetch(endpoint);
        let spec = await response.json();
        spec.config.background = "none";
        spec.config.font = "Open Sans";
        spec.width = 700;

        const chartOptions = {
            config: {
                axis: {
                    labelColor: "#ffffff",
                    titleColor: "#ffffff",
                    gridColor: '#444444',
                    labelFont: "Open Sans",
                    labelFontSize: 14,
                    titleFont: "Open Sans",
                    titleFontWeight: "normal",
                    titleFontSize: 15,
                }, title: {
                    anchor: "start",
                    color: "#ffffff",
                    font: "Open Sans",
                    fontSize: 21,
                    fontStyle: "normal",
                    fontWeight: "bold",
                    subtitleColor: "#ffffff",
                    subtitleFontSize: 17,
                    subtitleFont: "Open Sans",
                    subtitleFontStyle: "normal",
                    subtitleFontWeight: "normal",
                    subtitlePadding: 10,
                    offset: 20,
                },
                header: {
                    labelColor: "#ffffff",
                    labelFontSize: 14,
                    labelFontWeight: "bold",
                    titleColor: "#ffffff",
                    titleFontSize: 16
                }, range: {
                    category: ['#f72585', '#7209b7', '#4361ee', '#4cc9f0', '#b5179e', '#3a0ca3'],
                    heatmap: ['#f4d3dd', '#e2b6d4', '#c9a5da', '#b3a4d9', '#9fb4e5', '#6c97df']
                }, tooltip: {
                    content: "data", theme: 'dark', style: true
                }, legend: {
                    labelColor: "#ffffff",
                    titleColor: "#ffffff",
                    titleFont: "Open Sans",
                    titleFontStyle: 'normal',
                    titleFontSize: 16,
                    labelFont: "Open Sans",
                    labelFontSize: 14,
                    symbolSize: 100,
                    symbolType: "circle"
                }, mark: {
                    color: "#4361ee"
                }
            }
        };

        const embedResult = await vegaEmbed(`#${chartId}`, spec, chartOptions);
        chartViews[chartId] = embedResult.view;
    } catch (error) {
        console.log(`Error getting chart ${chartId}`, error);
    }
}

function createChartCards() {
    const container = document.getElementById("chart-container");

    charts.forEach(([_, id]) => {
        const card = document.createElement("div");
        card.className = "card mb-5 p-4";

        // language=HTML
        card.innerHTML = `
            <div>
                <div id="${id}" class="vega-embed"></div>
            </div>
        `

        container.appendChild(card);
    });
}

function updateCharts() {
    const picker = document.querySelector("#date_range")._flatpickr;
    const dates = picker?.selectedDates;

    if (!dates || dates.length !== 2) {
        alert("Please select both start and end dates.");
        return;
    }

    const startDate = flatpickr.formatDate(dates[0], "d/m/Y");
    const endDate = flatpickr.formatDate(dates[1], "d/m/Y");

    charts.forEach(([url, id]) => getChart(`${url}?start_date=${startDate}&end_date=${endDate}`, id));
}

document.addEventListener("DOMContentLoaded", function () {
    createChartCards();
    charts.forEach(([url, id]) => getChart(url, id));
});

