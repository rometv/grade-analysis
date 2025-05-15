let minDateGlobal = null;
let maxDateGlobal = null;

document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/date_range')
        .then(res => res.json())
        .then(data => {
            minDateGlobal = data.start_date;
            maxDateGlobal = data.end_date;

            flatpickr("#date_range", {
                mode: "range",
                dateFormat: "d/m/Y",
                defaultDate: [minDateGlobal, maxDateGlobal],
                minDate: minDateGlobal,
                maxDate: maxDateGlobal,
                locale: {
                    firstDayOfWeek: 1
                }
            });
        });

    getGeneral();
});

function setDateRangePicker(start, end) {
    const picker = document.querySelector("#date_range");
    if (picker && picker._flatpickr) {
        picker._flatpickr.setDate([start, end]);
    }
}

async function getDateRange() {
    try {
        const response = await fetch('/api/date_range');
        const data = await response.json();

        if (data.start_date && data.end_date) {
            setDateRangePicker(data.start_date, data.end_date);
        } else {
            console.warn("Date range unavailable");
        }
    } catch (err) {
        console.error("Failed to load date range:", err);
    }
}