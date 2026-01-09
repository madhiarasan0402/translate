const voiceData = {
    en: [
        { id: "en-US-EmmaNeural", name: "Female" },
        { id: "en-US-AndrewNeural", name: "Male" }
    ],
    hi: [
        { id: "hi-IN-SwaraNeural", name: "Female" },
        { id: "hi-IN-MadhurNeural", name: "Male" }
    ],
    es: [
        { id: "es-MX-DaliaNeural", name: "Female" },
        { id: "es-MX-JorgeNeural", name: "Male" }
    ],
    ja: [
        { id: "ja-JP-NanamiNeural", name: "Female" },
        { id: "ja-JP-KeitaNeural", name: "Male" }
    ],
    fr: [
        { id: "fr-FR-DeniseNeural", name: "Female" },
        { id: "fr-FR-HenriNeural", name: "Male" }
    ],
    de: [
        { id: "de-DE-KatjaNeural", name: "Female" },
        { id: "de-DE-ConradNeural", name: "Male" }
    ],
    ta: [
        { id: "ta-IN-SaranyaNeural", name: "Female" },
        { id: "ta-IN-AnbuNeural", name: "Male" }
    ],
    ml: [
        { id: "ml-IN-SobhanaNeural", name: "Female" },
        { id: "ml-IN-MidhunNeural", name: "Male" }
    ]
};

function updateVoices() {
    const targetLang = document.getElementById('targetLang').value;
    const voiceSelect = document.getElementById('voiceSelect');

    // Default options if language not in our detailed list
    let voices = [
        { id: 'female', name: 'Standard Female' },
        { id: 'male', name: 'Standard Male' }
    ];

    if (voiceData[targetLang]) {
        voices = voiceData[targetLang];
    }

    voiceSelect.innerHTML = '';
    voices.forEach(voice => {
        const option = document.createElement('option');
        option.value = voice.id;
        option.textContent = voice.name;
        voiceSelect.appendChild(option);
    });
}

// Listen for language changes
document.getElementById('targetLang').addEventListener('change', updateVoices);

// Initialize voices on load
window.addEventListener('load', updateVoices);

document.getElementById('translatorForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const videoSource = document.getElementById('videoSource');
    const videoPlayer = document.getElementById('videoPlayer');

    // Prepare FormData
    const formData = new FormData(this);

    // Reset UI
    loadingOverlay?.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = 'DUBBING...';

    // Quick Health Check
    try {
        const health = await fetch('/api/health');
        if (!health.ok) throw new Error("Server is not responding");
        console.log("Server is healthy, starting translation...");
    } catch (e) {
        alert("⚠️ Backend Server Error: Cannot reach the translation engine. Please make sure the server is running.");
        loadingOverlay.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Translate Video';
        return;
    }

    try {
        const loadingText = loadingOverlay.querySelector('p');
        const messages = [
            "DUBBING VIDEO...",
            "TRANSCRIBING AUDIO...",
            "TRANSLATING TEXT...",
            "GENERATING AI VOICE...",
            "MIXING VIDEO & AUDIO..."
        ];
        let msgIdx = 0;
        const interval = setInterval(() => {
            if (!loadingOverlay.classList.contains('hidden')) {
                loadingText.textContent = messages[msgIdx];
                msgIdx = (msgIdx + 1) % messages.length;
            } else {
                clearInterval(interval);
            }
        }, 5000);

        const response = await fetch('/api/translate', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Translation failed');
        }

        const data = await response.json();
        if (data.output_video_url) {
            displayResult(data);
        } else {
            throw new Error("No video URL returned from server");
        }

    } catch (error) {
        alert('🚨 Translation Error: ' + error.message);
        console.error('Translation error:', error);
    } finally {
        loadingOverlay.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Translate Video';
        document.getElementById('loadingOverlay').querySelector('p').textContent = "DUBBING VIDEO...";
    }
});

// Clear Button
document.getElementById('clearBtn').addEventListener('click', () => {
    document.getElementById('translatorForm').reset();
    updateVoices(); // Reset dropdown
    document.getElementById('videoSource').src = '';
    document.getElementById('videoPlayer').load();
    document.getElementById('resultTextSection')?.classList.add('hidden');
});

function displayResult(data) {
    // Set Video
    const videoPlayer = document.getElementById('videoPlayer');
    const videoSource = document.getElementById('videoSource');

    // Add a slight fade effect to the video appearing
    videoPlayer.style.opacity = '0';
    videoSource.src = data.output_video_url;
    videoPlayer.load();

    videoPlayer.onloadeddata = () => {
        videoPlayer.style.transition = 'opacity 0.5s ease';
        videoPlayer.style.opacity = '1';
        videoPlayer.play();
        loadingOverlay.classList.add('hidden'); // Double check it's hidden
    };

    // Fallback if event doesn't fire
    setTimeout(() => {
        if (videoPlayer.style.opacity !== '1') {
            videoPlayer.style.opacity = '1';
            videoPlayer.play();
            loadingOverlay.classList.add('hidden');
        }
    }, 2000);

    // Set Text Section
    const resultSection = document.getElementById('resultTextSection');
    resultSection.classList.remove('hidden');
    resultSection.style.opacity = '0';
    resultSection.style.transform = 'translateY(20px)';

    document.getElementById('originalText').textContent = data.original_text;
    document.getElementById('translatedText').textContent = data.translated_text;

    // Trigger animation
    setTimeout(() => {
        resultSection.style.transition = 'all 0.8s ease-out';
        resultSection.style.opacity = '1';
        resultSection.style.transform = 'translateY(0)';
    }, 100);
}
