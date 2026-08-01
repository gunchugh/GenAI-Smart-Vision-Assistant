console.log("SCRIPT LOADED");
let recorder;
let chunks = [];

const btn = document.getElementById("recordBtn");

if (btn) {

    btn.onclick = async () => {

        if (!recorder || recorder.state === "inactive") {

            const stream = await navigator.mediaDevices.getUserMedia({
                audio: true
            });

            recorder = new MediaRecorder(stream);

            chunks = [];

            recorder.ondataavailable = e => {
                chunks.push(e.data);
            };

            recorder.onstop = async () => {

                const blob = new Blob(chunks, {
                    type: "audio/webm"
                });

                const formData = new FormData();

                formData.append(
                    "audio",
                    blob,
                    "recording.webm"
                );

                const response = await fetch("/speech_to_text", 
                    {
                        method: "POST",
                        body: formData
                    }
                );

                const data = await response.json();
                console.log(data);

                document.getElementById(
                    "speechResult"
                ).innerHTML =
                    "<b>Speech:</b> " + data.text;

            };

            recorder.start();

            btn.innerText = "Stop Recording";

        } else {

            recorder.stop();

            btn.innerText = "Start Recording";

        }

    };

}
window.addEventListener("load", () => {
    const loader = document.getElementById("loader");

    if (loader) {
        setTimeout(() => {
            loader.style.opacity = "0";

            setTimeout(() => {
                loader.style.display = "none";
            }, 500);
        }, 1200); // Loader 1.2 sec baad hide hoga
    }
});
const text = "Detect. Track. Understand.";
const typingElement = document.getElementById("typingText");

let i = 0;

function typeWriter() {
    if (typingElement && i < text.length) {
        typingElement.innerHTML += text.charAt(i);
        i++;
        setTimeout(typeWriter, 90);
    }
}

window.addEventListener("load", () => {
    setTimeout(typeWriter, 300);
});