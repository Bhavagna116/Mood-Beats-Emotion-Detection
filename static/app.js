const video = document.getElementById('videoElement');
const canvas = document.getElementById('canvasElement');
const ctx = canvas.getContext('2d');
const processedFrame = document.getElementById('processedFrame');
const videoContainer = document.getElementById('videoContainer');
const fileInput = document.getElementById('fileInput');

let currentMood = 'neutral';
let currentLanguage = 'english';  // english | hindi | telugu
let currentMusicMode = 'online'; // online | offline
let isStreaming = false;
let streamingInterval = null;
let lastResult = null;

// ── Tab logic ────────────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
        if (btn.dataset.tab !== 'live' && isStreaming) stopCamera();
    });
});

// ── Mode Toggle ─────────────────────────────────────────────────────────────
document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMusicMode = btn.dataset.mode;
        
        // Re-render music if we have a previous detection
        if(lastResult) {
            renderMusicDetails(lastResult);
        }
    });
});

// ── Language Selector ────────────────────────────────────────────────────────
document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.dataset.lang === currentLanguage) return;
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentLanguage = btn.dataset.lang;
        fetchNextTrack(currentMood, false);
    });
});

// ── Camera / Live Stream ─────────────────────────────────────────────────────
document.getElementById('startBtn').addEventListener('click', async () => {
    if (isStreaming) return;
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Your browser does not support camera access or you are not on a secure HTTPS connection.");
        return;
    }
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
        video.srcObject = stream;
        video.classList.remove('hidden');
        processedFrame.classList.add('hidden');
        isStreaming = true;
        videoContainer.classList.add('active-stream');
        video.onloadedmetadata = async () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            try { await video.play(); } catch (e) { console.error("Autoplay prevented:", e); }
        };
        streamingInterval = setInterval(processFrame, 400);
    } catch (err) {
        console.error("Camera error:", err);
        alert("Camera access was denied or failed. Please allow camera permissions.");
    }
});

document.getElementById('stopBtn').addEventListener('click', stopCamera);

function stopCamera() {
    if (!isStreaming) return;
    clearInterval(streamingInterval);
    const stream = video.srcObject;
    if (stream) stream.getTracks().forEach(t => t.stop());
    video.srcObject = null;
    isStreaming = false;
    videoContainer.classList.remove('active-stream');
    video.classList.remove('hidden');
    processedFrame.classList.add('hidden');
}

async function processFrame() {
    if (!isStreaming || video.paused || video.ended) return;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frameData = canvas.toDataURL('image/jpeg', 0.8);
    try {
        const response = await fetch('/api/detect/frame', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ frame: frameData, language: currentLanguage })
        });
        if (response.ok) {
            const result = await response.json();
            updateUI(result);
            if (result.processed_image) {
                video.classList.add('hidden');
                processedFrame.classList.remove('hidden');
                processedFrame.src = result.processed_image;
            }
        }
    } catch (err) { console.error("Frame error:", err); }
}

// ── Photo Upload ─────────────────────────────────────────────────────────────
fileInput.addEventListener('change', async (e) => {
    if (!e.target.files.length) return;
    const file = e.target.files[0];
    document.getElementById('fileUploadContainer').classList.add('input-filled');
    document.getElementById('fileUploadContainer').querySelector('h4').textContent = file.name;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', currentLanguage);
    try {
        const response = await fetch('/api/detect/photo', { method: 'POST', body: formData });
        if (response.ok) {
            const result = await response.json();
            updateUI(result);
            if (result.processed_image) {
                document.getElementById('fileUploadContainer').classList.add('hidden');
                const pContainer = document.getElementById('photoResultContainer');
                pContainer.classList.remove('hidden');
                document.getElementById('photoResultFrame').src = result.processed_image;
                document.getElementById('photoControls').classList.remove('hidden');
            }
        }
    } catch (err) { console.error("Photo error:", err); }
});

document.getElementById('clearPhotoBtn')?.addEventListener('click', () => {
    document.getElementById('photoResultContainer').classList.add('hidden');
    document.getElementById('photoControls').classList.add('hidden');
    document.getElementById('fileUploadContainer').classList.remove('hidden');
    document.getElementById('fileUploadContainer').classList.remove('input-filled');
    document.getElementById('fileUploadContainer').querySelector('h4').textContent = 'Click to Upload Photo';
    fileInput.value = '';
});

// ── UI Update ────────────────────────────────────────────────────────────────
function updateUI(result) {
    lastResult = result;
    if (result.emotion !== currentMood) {
        currentMood = result.emotion;
        document.documentElement.style.setProperty('--accent-color', result.color);
        document.getElementById('globalMoodBadge').textContent = currentMood;
        document.getElementById('musicStatusText').textContent =
            `Your ${currentMood.charAt(0).toUpperCase() + currentMood.slice(1)} Mix:`;
        renderMusicDetails(result);
    }
}

// ── Next Track ───────────────────────────────────────────────────────────────
async function fetchNextTrack(emotion, excludeCurrent = false) {
    try {
        let excludeId = "";
        if(excludeCurrent) {
            excludeId = currentMusicMode === 'online' ? window._currentTrackId : window._currentAudioUrl;
        }

        const resp = await fetch('/api/next-track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                emotion,
                language: currentLanguage,
                exclude: excludeId
            })
        });
        if (resp.ok) {
            const result = await resp.json();
            lastResult = result;
            renderMusicDetails(result);
        }
    } catch (e) { console.error("Next track error:", e); }
}

document.getElementById('nextTrackBtn').addEventListener('click', () => {
    fetchNextTrack(currentMood, true);
});

// ── Music Render + Custom Player ─────────────────────────────────────────────
const MOOD_EMOJI = {
    happy: '😊', sad: '😢', angry: '😡', fear: '😨',
    disgust: '🤢', neutral: '😐', surprise: '😲'
};
const LANG_FLAG = { english: '🌍', hindi: '🎬', telugu: '🇮🇳' };

function renderMusicDetails(data) {
    const container = document.getElementById('musicContainer');
    const moodEmoji = MOOD_EMOJI[data.emotion] || '🎵';
    const langFlag = LANG_FLAG[data.language] || '🎵';

    // Stop any currently playing audio gracefully
    const existingAudio = document.getElementById('inPageAudio');
    if (existingAudio) {
        existingAudio.pause();
        existingAudio.src = '';
    }

    if (currentMusicMode === 'online') {
        const track = data.spotify;
        if(track && track.track_id){
            container.innerHTML = `
                <div class="music-card" style="border-left-color: ${data.color}">
                    <div class="song-label">${langFlag} Spotify &nbsp;·&nbsp; <span style="text-transform:capitalize;">${data.language || 'english'}</span></div>
                    <div class="song-title">${track.song_name}</div>
                    <div class="song-artist">by ${track.artist}</div>
                </div>
                <div class="spotify-embed">
                    <iframe src="https://open.spotify.com/embed/track/${track.track_id}?utm_source=generator&theme=0&autoplay=1" width="100%" height="152" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                </div>
            `;
            window._currentTrackId = track.track_id;
        }
    } else {
        // Offline Custom Player
        const audioUrl = data.audio_url;
        const songName = data.offline ? data.offline.song_title : 'Unknown';
        const artist = data.offline ? data.offline.artist : 'Unknown';

        if (audioUrl) {
            window._currentAudioUrl = audioUrl;

            container.innerHTML = `
                <div class="music-card offline" style="border-left-color:${data.color}">
                    <div class="song-label">💿 Local Audio &nbsp;·&nbsp; <span style="text-transform:capitalize;">${data.language || 'english'}</span></div>
                    <div class="song-title">${songName}</div>
                    <div class="song-artist">by ${artist}</div>
                </div>

                <div class="custom-player" id="customPlayer">
                    <!-- Mood Art + EQ Visualiser -->
                    <div class="player-art" style="background: radial-gradient(circle, ${data.color}30, transparent 70%);">
                        <span class="mood-emoji-big">${moodEmoji}</span>
                        <div class="eq-bars" id="eqBars">
                            <span></span><span></span><span></span><span></span><span></span>
                        </div>
                    </div>

                    <!-- Progress Timeline -->
                    <div class="player-timeline">
                        <span class="player-time" id="timeCurrent">0:00</span>
                        <input type="range" class="player-progress" id="progressBar" value="0" min="0" max="100" step="0.1">
                        <span class="player-time" id="timeTotal">0:00</span>
                    </div>

                    <!-- Control Buttons -->
                    <div class="player-btns">
                        <button class="player-btn" id="restartBtn" title="Restart">⏮</button>
                        <button class="player-btn play-btn" id="playPauseBtn" title="Play / Pause">▶</button>
                        <button class="player-btn" id="skipBtn" title="Next Track">⏭</button>
                    </div>

                    <!-- Volume -->
                    <div class="player-volume">
                        <span>🔊</span>
                        <input type="range" class="volume-slider" id="volumeSlider" min="0" max="100" value="80">
                        <span id="volPct">80%</span>
                    </div>

                    <!-- Hidden Audio Element -->
                    <audio id="inPageAudio" preload="auto">
                        <source src="${audioUrl}" type="audio/mpeg">
                    </audio>
                </div>
            `;

            setupPlayer();
        } else {
            container.innerHTML = `
                <div class="music-card offline" style="border-left-color:${data.color}">
                    <div class="song-label">${langFlag} Mood Detected</div>
                    <div class="song-title">${songName}</div>
                    <div class="song-artist">by ${artist}</div>
                </div>
                <div class="no-audio-msg">
                    <span>${moodEmoji}</span>
                    <p>No local audio found for this emotion.<br>Add MP3 files to <code>local_music/</code> folder.</p>
                </div>
            `;
        }
    }
}

function setupPlayer() {
    const audio = document.getElementById('inPageAudio');
    const playBtn = document.getElementById('playPauseBtn');
    const progressBar = document.getElementById('progressBar');
    const timeCurrent = document.getElementById('timeCurrent');
    const timeTotal = document.getElementById('timeTotal');
    const volumeSlider = document.getElementById('volumeSlider');
    const volPct = document.getElementById('volPct');
    const eqBars = document.getElementById('eqBars');

    if (!audio) return;

    // Auto-play
    audio.volume = 0.8;
    audio.play().catch(() => {
        // Browser blocked autoplay — user must click play
        playBtn && (playBtn.textContent = '▶');
    });

    audio.addEventListener('loadedmetadata', () => {
        progressBar.max = audio.duration;
        timeTotal.textContent = fmt(audio.duration);
    });

    audio.addEventListener('timeupdate', () => {
        progressBar.value = audio.currentTime;
        timeCurrent.textContent = fmt(audio.currentTime);
    });

    audio.addEventListener('play', () => {
        playBtn.textContent = '⏸';
        eqBars?.classList.add('playing');
    });

    audio.addEventListener('pause', () => {
        playBtn.textContent = '▶';
        eqBars?.classList.remove('playing');
    });

    audio.addEventListener('ended', () => {
        eqBars?.classList.remove('playing');
        fetchNextTrack(currentMood, true);
    });

    // Play / Pause
    playBtn?.addEventListener('click', () => {
        audio.paused ? audio.play() : audio.pause();
    });

    // Seek
    progressBar?.addEventListener('input', () => {
        audio.currentTime = parseFloat(progressBar.value);
    });

    // Volume
    volumeSlider?.addEventListener('input', () => {
        audio.volume = volumeSlider.value / 100;
        volPct.textContent = volumeSlider.value + '%';
    });

    // Restart current track
    document.getElementById('restartBtn')?.addEventListener('click', () => {
        audio.currentTime = 0;
        audio.play();
    });

    // Skip to next
    document.getElementById('skipBtn')?.addEventListener('click', () => {
        fetchNextTrack(currentMood, true);
    });
}

function fmt(sec) {
    if (!isFinite(sec) || isNaN(sec)) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}
