const translateBtn = document.getElementById('translateBtn');
const inputText = document.getElementById('inputText');
const outputText = document.getElementById('outputText');
const sourceLang = document.getElementById('sourceLang');
const targetLang = document.getElementById('targetLang');

// 1. Translation Logic
translateBtn.addEventListener('click', async () => {
    const text = inputText.value;
    if (!text) return;

    translateBtn.innerText = "Translating...";
    
    try {
        const res = await fetch("https://libretranslate.de/translate", {
            method: "POST",
            body: JSON.stringify({
                q: text,
                source: sourceLang.value,
                target: targetLang.value,
                format: "text"
            }),
            headers: { "Content-Type": "application/json" }
        });

        const data = await res.json();
        outputText.value = data.translatedText;
    } catch (error) {
        alert("Error connecting to Translation API.");
    } finally {
        translateBtn.innerText = "Translate";
    }
});

// 2. Copy to Clipboard
document.getElementById('copyBtn').addEventListener('click', () => {
    navigator.clipboard.writeText(outputText.value);
    alert("Copied!");
});

// 3. Text-to-Speech
document.getElementById('speakBtn').addEventListener('click', () => {
    const speech = new SpeechSynthesisUtterance(outputText.value);
    speech.lang = targetLang.value;
    window.speechSynthesis.speak(speech);
});