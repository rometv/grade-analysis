async function purgeUploads() {
    if (confirm("Oled kindel, et soovid kõik andmed kustutada?")) {
        try {
            const response = await fetch('/api/purge', {method: 'POST'});
            const result = await response.json();
            alert(result.message || "Andmed edukalt kustutatud!");
            window.location.href = "/upload";
        } catch (error) {
            console.error("Puhastamisel tekkis viga:", error);
            alert("Midagi läks valesti puhastamisel.");
        }
    }
}

async function getGeneral() {
    fetch('api/general')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#summary-table tbody");
            tbody.innerHTML = "";

            data.forEach(([_key, label, value]) => {
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

document.addEventListener("DOMContentLoaded", function () {
    getGeneral();
});

fetch("/api/hw_name")
    .then(response => response.text())
    .then(hwName => {
        document.getElementById("dashboard-title").textContent = `Kodutöö analüüs | ${hwName}`;
        document.getElementById("footer-hwname").textContent = `${hwName}`;
    })
    .catch(err => console.error("Homework name fetch failed:", err));