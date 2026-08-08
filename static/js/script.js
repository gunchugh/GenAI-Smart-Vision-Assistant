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
/* ==========================================
   PART 1 - ASK AI
========================================== */

async function askAI() {

    const questionBox = document.getElementById("question");
    const answerBox = document.getElementById("answer");

    if (!questionBox || !answerBox) {
        console.error("Question or Answer element not found.");
        return;
    }

    const question = questionBox.value.trim();

    if (question === "") {
        alert("Please enter a question.");
        return;
    }

    answerBox.innerHTML = "⏳ AI is thinking...";

    try {

        const formData = new FormData();

        formData.append(
            "question",
            question
        );

        const response = await fetch(
            "/ask",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Server Error");
        }

        const data = await response.json();

        answerBox.innerHTML =
            "<b>Answer:</b> " + data.answer;

    }

    catch (error) {

        console.error(error);

        answerBox.innerHTML =
            "❌ Unable to get answer.";

    }

}


/* ==========================================
   SMALL HELPER
========================================== */

function showMessage(message) {

    console.log(message);

}
/* ==========================================
   VOICE QUESTION ANSWERING
========================================== */

/* ==========================================
   VOICE QUESTION ANSWERING
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    const voiceBtn = document.getElementById("voiceBtn");

    if (!voiceBtn) {
        console.log("Voice button not found.");
        return;
    }

    let voiceRecorder = null;
    let voiceChunks = [];

    voiceBtn.addEventListener("click", async function () {

        try {

            /* ==========================
               START RECORDING
            ========================== */

            if (
                !voiceRecorder ||
                voiceRecorder.state === "inactive"
            ) {

                const stream =
                    await navigator.mediaDevices.getUserMedia({
                        audio: true
                    });

                voiceRecorder =
                    new MediaRecorder(stream);

                voiceChunks = [];

                voiceRecorder.ondataavailable =
                    function (event) {

                        if (event.data.size > 0) {

                            voiceChunks.push(
                                event.data
                            );

                        }

                    };

                voiceRecorder.onstop =
                    async function () {

                        /* Stop microphone */

                        stream.getTracks().forEach(
                            track => track.stop()
                        );

                        const blob =
                            new Blob(
                                voiceChunks,
                                {
                                    type: "audio/webm"
                                }
                            );

                        const formData =
                            new FormData();

                        formData.append(
                            "audio",
                            blob,
                            "voice_question.webm"
                        );

                        const questionBox =
                            document.getElementById(
                                "voiceQuestion"
                            );

                        const answerBox =
                            document.getElementById(
                                "voiceAnswer"
                            );

                        if (answerBox) {

                            answerBox.innerHTML =
                                "⏳ AI is listening...";

                        }

                        try {

                            const response =
                                await fetch(
                                    "/voice_ask",
                                    {
                                        method: "POST",
                                        body: formData
                                    }
                                );

                            if (!response.ok) {

                                throw new Error(
                                    "Voice server error"
                                );

                            }

                            const data =
                                await response.json();

                            console.log(
                                "Voice response:",
                                data
                            );

                            /* ==========================
                               ERROR
                            ========================== */

                            if (data.error) {

                                if (answerBox) {

                                    answerBox.innerHTML =
                                        "❌ " +
                                        data.error;

                                }

                                return;

                            }

                            /* ==========================
                               QUESTION
                            ========================== */

                            if (questionBox) {

                                questionBox.innerHTML =
                                    "<b>Question:</b> " +
                                    data.question;

                            }

                            /* ==========================
                               ANSWER
                            ========================== */

                            if (answerBox) {

                                answerBox.innerHTML =
                                    "<b>Answer:</b> " +
                                    data.answer;

                            }

                            /* ==========================
                               AUDIO ANSWER
                            ========================== */

                            const audioPlayer =
                                document.getElementById(
                                    "voiceAudio"
                                );

                            if (
                                audioPlayer &&
                                data.audio
                            ) {

                                audioPlayer.src =
                                    "/static/" +
                                    data.audio;

                                audioPlayer.load();

                            }

                        }

                        catch (error) {

                            console.error(
                                "Voice processing error:",
                                error
                            );

                            if (answerBox) {

                                answerBox.innerHTML =
                                    "❌ Voice processing failed.";

                            }

                        }

                    };

                voiceRecorder.start();

                voiceBtn.innerText =
                    "⏹ Stop Voice Question";

                voiceBtn.classList.add(
                    "recording"
                );

            }

            /* ==========================
               STOP RECORDING
            ========================== */

            else {

                voiceRecorder.stop();

                voiceBtn.innerText =
                    "⏳ Processing...";

                voiceBtn.classList.remove(
                    "recording"
                );

            }

        }

        catch (error) {

            console.error(
                "Microphone error:",
                error
            );

            alert(
                "❌ Microphone access is required."
            );

            voiceBtn.innerText =
                "🎤 Start Voice Question";

        }

    });

});
/* ==========================================
   DOWNLOAD AI REPORT
========================================== */

async function downloadReport() {

    try {

        const response = await fetch("/download_report");

        if (!response.ok) {
            throw new Error("Unable to generate report.");
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download = "AI_Vision_Report.pdf";

        document.body.appendChild(a);

        a.click();

        a.remove();

        window.URL.revokeObjectURL(url);

    }

    catch (err) {

        console.error(err);

        alert("❌ Failed to download report.");

    }

}
/* ==========================================
   AUDIO FILE UPLOAD (Speech To Text)
========================================== */

const uploadSpeechForm =
    document.getElementById("uploadSpeechForm");

if (uploadSpeechForm) {

    uploadSpeechForm.onsubmit = async function (e) {

        e.preventDefault();

        const formData = new FormData(uploadSpeechForm);

        document.getElementById(
            "speechResult"
        ).innerHTML = "⏳ Converting speech to text...";

        try {

            const response = await fetch(
                "/speech_to_text",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            document.getElementById(
                "speechResult"
            ).innerHTML =
                "<b>Speech:</b> " + data.text;

        }

        catch (err) {

            console.log(err);

            document.getElementById(
                "speechResult"
            ).innerHTML =
                "❌ Failed to convert audio.";

        }

    };

}