async function startScan() {
  const url = document.getElementById("targetUrl").value;
  const tableBody = document.querySelector("#resultsTable tbody");

  tableBody.innerHTML = "";

  if (!url) {
    alert("Please enter a target URL");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await response.json();

    data.findings.forEach(finding => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${finding.name}</td>
        <td class="severity-${finding.severity.toLowerCase()}">${finding.severity}</td>
        <td>${finding.location}</td>
        <td>${finding.description}</td>
      `;

      tableBody.appendChild(row);
    });

  } catch (error) {
    alert("Scan failed. Is backend running?");
  }
}
