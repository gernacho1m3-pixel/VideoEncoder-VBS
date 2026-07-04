const input = document.getElementById("videoInput");
const metadata = document.getElementById("metadata");
const convertBtn = document.getElementById("convertBtn");
const format = document.getElementById("format");
const vcodec = document.getElementById("vcodec");
const resolution = document.getElementById("resolution");
const fps = document.getElementById("fps");
const videoBitrate = document.getElementById("videoBitrate");
const audioBitrate = document.getElementById("audioBitrate");
const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");

let currentFilename = "";

input.addEventListener("change", async () => {

    const file = input.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    metadata.innerHTML = "Uploading...";

    const uploadRes = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData
    });

    const uploadData = await uploadRes.json();

    currentFilename = uploadData.filename;

    const metaRes = await fetch(
        `${API_BASE}/metadata/${uploadData.filename}`
    );

    const data = await metaRes.json();

    renderMetadata(data);

});

function renderMetadata(data) {

    const video = data.streams.find(s => s.codec_type === "video");
    const audio = data.streams.find(s => s.codec_type === "audio");

    const sizeMB = (data.format.size / 1024 / 1024).toFixed(2);
    const duration = Number(data.format.duration).toFixed(2);
    const fpsValue = eval(video.r_frame_rate);

    metadata.innerHTML = `
        <h3>${uploadDataSafe(data)}</h3>

        <p><b>Resolution:</b> ${video.width} × ${video.height}</p>
        <p><b>FPS:</b> ${fpsValue}</p>
        <p><b>Duration:</b> ${duration} sec</p>
        <p><b>Video Codec:</b> ${video.codec_name}</p>
        <p><b>Audio Codec:</b> ${audio.codec_name}</p>
        <p><b>Size:</b> ${sizeMB} MB</p>
    `;

}

function uploadDataSafe(data) {

    return data.format.filename.split("\\").pop();

}

convertBtn.addEventListener("click", async () => {

    if (!currentFilename) {

        alert("Upload video terlebih dahulu.");

        return;

    }

    const body = {

        filename: currentFilename,
        output_format: format.value,
        vcodec: vcodec.value,
        resolution: resolution.value,
        fps: fps.value === "original" ? 30 : Number(fps.value),
        vbitrate: Number(videoBitrate.value),
        abitrate: Number(audioBitrate.value)

    };

    progressBar.value = 0;
    progressText.innerText = "0%";

    watchProgress(currentFilename);

    await fetch(`${API_BASE}/convert`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)

    });

});

async function watchProgress(filename) {

    while (true) {

        const res = await fetch(
            `${API_BASE}/progress/${filename}`
        );

        const data = await res.json();

        progressBar.value = data.progress;
        progressText.innerText = data.progress + "%";

        if (data.progress >= 100) {

            const old = document.getElementById("downloadBtn");

            if (old) old.remove();

            const downloadLink = document.createElement("a");

            downloadLink.id = "downloadBtn";

            downloadLink.href =
                `${API_BASE}/download/${filename.replace(/\.[^/.]+$/, "")}_converted.${format.value}`;

            downloadLink.innerText = "⬇ Download Hasil";

            downloadLink.target = "_blank";

            metadata.appendChild(document.createElement("br"));
            metadata.appendChild(downloadLink);

            break;

        }

        await new Promise(resolve => setTimeout(resolve, 500));

    }

}