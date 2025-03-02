document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("button").addEventListener("click", startScan);
});

function startScan() {
    let url = document.getElementById("url").value.trim();

    if (!url) {
        alert("❌ Please enter a valid URL!");
        return;
    }

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result").innerHTML = "";

    fetch("/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").classList.add("hidden");

        if (data.error) {
            document.getElementById("result").innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }

        let output = `<h3>🔍 Scan Results for: ${data.url}</h3>`;
        output += `<p>🛡️ <strong>SQL Injection:</strong> ${data.sql_injection ? "✅ Vulnerable" : "❌ Safe"}</p>`;
        output += `<p>🛡️ <strong>XSS:</strong> ${data.xss ? "✅ Vulnerable" : "❌ Safe"}</p>`;
        output += `<p>🛡️ <strong>Open Redirect:</strong> ${data.open_redirect ? "✅ Vulnerable" : "❌ Safe"}</p>`;
        output += `<p>🛡️ <strong>Clickjacking:</strong> ${data.clickjacking ? "✅ Vulnerable" : "❌ Safe"}</p>`;
        output += `<p>🛡️ <strong>CORS Misconfig:</strong> ${data.cors_misconfig ? "✅ Vulnerable" : "❌ Safe"}</p>`;
        output += `<p>🛡️ <strong>CSRF:</strong> ${data.csrf_vulnerable ? "✅ Vulnerable" : "❌ Safe"}</p>`;

        // Subdomains List
        if (data.subdomains && data.subdomains.length > 0) {
            output += `<h4>🌐 Subdomains Found:</h4><ul>`;
            data.subdomains.forEach(sub => {
                output += `<li>${sub}</li>`;
            });
            output += `</ul>`;
        } else {
            output += `<p>🌐 No subdomains found.</p>`;
        }

        document.getElementById("result").innerHTML = output;
    })
    .catch(error => {
        document.getElementById("loading").classList.add("hidden");
        document.getElementById("result").innerHTML = `<p class="error">⚠️ Error: ${error.message}</p>`;
    });
}
