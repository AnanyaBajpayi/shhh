document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("csvFile");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) throw new Error("Failed to generate report");

        const result = await response.json();
        const report = result.report;

        let reportHtml = "<h2>Fine Report</h2><ul>";
        reportHtml += `<li>${report}</li>`;  // Display the full report as returned from the API
        reportHtml += "</ul>";

        document.getElementById("report").innerHTML = reportHtml;
    } catch (err) {
        console.error(err);
        alert("An error occurred");
    }
});
