const statusBox = document.getElementById("server-status");

async function checkBackend() {
    try {
        const response = await fetch("http://127.0.0.1:8000/health");

        if (!response.ok) {
            throw new Error("Backend Error");
        }

        const data = await response.json();

        statusBox.textContent = `🟢 ${data.service} (${data.version})`;
        statusBox.style.backgroundColor = "#2e7d32";

    } catch (error) {

        statusBox.textContent = "🔴 Backend Offline";
        statusBox.style.backgroundColor = "#b71c1c";

    }
}

checkBackend();