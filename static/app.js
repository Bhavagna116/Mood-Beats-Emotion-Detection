/* ════════════════════════════════════════════════════════════
   Live Mood Beats – app.js
   Fixes: stop-camera reliability, lag, mobile, Spotify re-render
   ════════════════════════════════════════════════════════════ */

// ── DOM refs ────────────────────────────────────────────────────────────────
const video          = document.getElementById('videoElement');
const canvas         = document.getElementById('canvasElement');
const ctx            = canvas.getContext('2d');
const processedFrame = document.getElementById('processedFrame');
const videoContainer = document.getElementById('videoContainer');
const fileInput      = document.getElementById('fileInput');

// ── State ───────────────────────────────────────────────────────────────────
let currentMood      = 'neutral';
let currentLanguage  = 'english';   // english | hindi | telugu
let currentMusicMode = 'online';    // online  | offline
let isStreaming      = false;
let isProcessing     = false;       // prevents queued duplicate requests
let frameLoopId      = null;        // setTimeout handle
let lastResult       = null;
let lastRenderedTrackId = '';       // avoids re-injecting Spotify iframe unnecessarily

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

// ── Mode Toggle ──────────────────────────────────────────────────────────────
document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMusicMode = btn.dataset.mode;
        lastRenderedTrackId = ''; // force re-render on mode switch
        if (lastResult) renderMusicDetails(lastResult);
    });
});

// ── Language Selector ────────────────────────────────────────────────────────
document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.dataset.lang === currentLanguage) return;
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentLanguage = btn.dataset.lang;
        lastRenderedTrackId = '';
        fetchNextTrack(currentMood, false);
    });
});

// ── Start Camera ─────────────────────────────────────────────────────────────
document.getElementById('startBtn').addEventListener('click', async () => {
    if (isStreaming) return;

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Camera not supported. Please use a modern browser on HTTPS.');
        return;
    }

    // Try ideal resolution first; fall back to any camera if it fails
    const tryStart = async (constraints) => {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;

        await new Promise(resolve => {
            video.onloadedmetadata = () => {
                canvas.width  = video.videoWidth  || 640;
                canvas.height = video.videoHeight || 480;
                resolve();
            };
        });

        try { await video.play(); } catch (_) {}

        // Show live video feed first
        video.classList.remove('hidden');
        processedFrame.classList.add('hidden');
        isStreaming = true;
        videoContainer.classList.add('active-stream');

        // Start frame-loop
        scheduleNextFrame();
    };

    try {
        await tryStart({
            video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
            audio: false
        });
    } catch (err) {
        // Fallback for older Android/iOS that don't support ideal constraints
        try {
            await tryStart({ video: { facingMode: 'user' }, audio: false });
        } catch (err2) {
            try {
                await tryStart({ video: true, audio: false });
            } catch (err3) {
                console.error('Camera error:', err3);
                alert('Camera access denied or unavailable. Please allow camera permissions and try again.');
            }
        }
    }
});

// ── Stop Camera ───────────────────────────────────────────────────────────────
document.getElementById('stopBtn').addEventListener('click', stopCamera);

function stopCamera() {
    // Mark stopped FIRST so any in-flight processFrame call exits immediately
    isStreaming  = false;
    isProcessing = false;

    // Cancel the pending setTimeout
    if (frameLoopId !== null) {
        clearTimeout(frameLoopId);
        frameLoopId = null;
    }

    // Release camera hardware
    const stream = video.srcObject;
    if (stream) {
        stream.getTracks().forEach(track => {
            track.stop();
        });
    }
    video.srcObject = null;
    video.load();   // resets the video element fully

    // Reset UI
    videoContainer.classList.remove('active-stream');
    video.classList.remove('hidden');
    processedFrame.classList.add('hidden');
    processedFrame.src = '';
}

// ── Frame Loop (setTimeout chain, NOT setInterval) ───────────────────────────
// Using setTimeout chains avoids overlapping async calls that cause lag &
// makes it trivial to stop: just don't schedule the next timeout.
function scheduleNextFrame() {
    if (!isStreaming) return;
    // Use a slower interval on mobile to avoid CPU choke
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    const delay = isMobile ? 1200 : 800;   // ms between frames
    frameLoopId = setTimeout(captureAndSend, delay);
}

async function captureAndSend() {
    // Guard: do nothing if already stopped or another request is in flight
    if (!isStreaming) return;
    if (isProcessing) {
        scheduleNextFrame();
        return;
    }
    if (video.paused || video.ended || video.readyState < 2) {
        scheduleNextFrame();
        return;
    }
    if (canvas.width === 0 || canvas.height === 0) {
        scheduleNextFrame();
        return;
    }

    isProcessing = true;

    try {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        // Lower quality on mobile to reduce payload size
        const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
        const quality  = isMobile ? 0.55 : 0.7;
        const frameData = canvas.toDataURL('image/jpeg', quality);

        const response = await fetch('/api/detect/frame', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ frame: frameData, language: currentLanguage })
        });

        if (response.ok && isStreaming) {   // check isStreaming again after await
            const result = await response.json();
            updateUI(result);

            if (result.processed_image && isStreaming) {
                // Overlay processed frame on top of live feed; less jarring than hide/show
                processedFrame.src = result.processed_image;
                processedFrame.classList.remove('hidden');
                // Show live video underneath as fallback — keep it visible
                video.classList.remove('hidden');
            }
        }
    } catch (err) {
        if (isStreaming) console.error('Frame error:', err);
    } finally {
        isProcessing = false;
        scheduleNextFrame();    // schedule next ONLY after current completes
    }
}

// ── Photo Upload ──────────────────────────────────────────────────────────────
fileInput.addEventListener('change', async (e) => {
    if (!e.target.files.length) return;
    const file = e.target.files[0];

    const uploadBox = document.getElementById('fileUploadContainer');
    uploadBox.classList.add('input-filled');
    uploadBox.querySelector('h4').textContent = '⏳ Analysing...';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', currentLanguage);

    try {
        const response = await fetch('/api/detect/photo', { method: 'POST', body: formData });
        if (response.ok) {
            const result = await response.json();
            updateUI(result);
            uploadBox.querySelector('h4').textContent = file.name;
            if (result.processed_image) {
                uploadBox.classList.add('hidden');
                const pContainer = document.getElementById('photoResultContainer');
                pContainer.classList.remove('hidden');
                document.getElementById('photoResultFrame').src = result.processed_image;
                document.getElementById('photoControls').classList.remove('hidden');
            }
        } else {
            uploadBox.querySelector('h4').textContent = 'Upload failed – try again';
        }
    } catch (err) {
        console.error('Photo error:', err);
        uploadBox.querySelector('h4').textContent = 'Error – check server';
    }
});

document.getElementById('clearPhotoBtn')?.addEventListener('click', () => {
    document.getElementById('photoResultContainer').classList.add('hidden');
    document.getElementById('photoControls').classList.add('hidden');
    const uploadBox = document.getElementById('fileUploadContainer');
    uploadBox.classList.remove('hidden', 'input-filled');
    uploadBox.querySelector('h4').textContent = 'Click to Upload Photo';
    fileInput.value = '';
});

// ── Emotion chip strip ────────────────────────────────────────────────────────
function highlightEmotionChip(emotion) {
    document.querySelectorAll('.emotion-chip').forEach(chip => chip.classList.remove('detected'));
    const chip = document.getElementById(`chip-${emotion}`);
    if (chip) chip.classList.add('detected');
}

// ── UI Update ─────────────────────────────────────────────────────────────────
// Only re-render music when the EMOTION actually changes (avoids Spotify iframe reload lag)
function updateUI(result) {
    lastResult   = result;
    const changed = (result.emotion !== currentMood);
    currentMood  = result.emotion;

    document.documentElement.style.setProperty('--accent-color', result.color);
    document.getElementById('globalMoodBadge').textContent = currentMood;
    document.getElementById('musicStatusText').textContent =
        `Your ${currentMood.charAt(0).toUpperCase() + currentMood.slice(1)} Mix:`;
    highlightEmotionChip(currentMood);

    // Only re-render music if emotion changed or track ID changed
    const newTrackId = result.spotify && result.spotify.track_id;
    if (changed || (newTrackId && newTrackId !== lastRenderedTrackId)) {
        renderMusicDetails(result);
    }
}

// ── Next Track ────────────────────────────────────────────────────────────────
async function fetchNextTrack(emotion, excludeCurrent = false) {
    try {
        const excludeId = excludeCurrent
            ? (currentMusicMode === 'online'
                ? (window._currentTrackId  || '')
                : (window._currentAudioUrl || ''))
            : '';

        const resp = await fetch('/api/next-track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ emotion, language: currentLanguage, exclude: excludeId })
        });

        if (resp.ok) {
            const result = await resp.json();
            lastResult = result;
            lastRenderedTrackId = ''; // force re-render
            renderMusicDetails(result);
        }
    } catch (e) { console.error('Next track error:', e); }
}

document.getElementById('nextTrackBtn').addEventListener('click', () => {
    fetchNextTrack(currentMood, true);
});

// ── Music Render ──────────────────────────────────────────────────────────────
const MOOD_EMOJI = {
    happy: '😊', sad: '😢', angry: '😡', fear: '😨',
    disgust: '🤢', neutral: '😐', surprise: '😲'
};
const LANG_FLAG = { english: '🌍', hindi: '🎬', telugu: '🇮🇳' };

function renderMusicDetails(data) {
    const container  = document.getElementById('musicContainer');
    const moodEmoji  = MOOD_EMOJI[data.emotion] || '🎵';
    const langFlag   = LANG_FLAG[data.language]  || '🎵';

    // Stop any in-page audio
    const existingAudio = document.getElementById('inPageAudio');
    if (existingAudio) { existingAudio.pause(); existingAudio.src = ''; }

    if (currentMusicMode === 'online') {
        const track = data.spotify;
        if (track && track.track_id) {
            // Only re-inject the iframe if the track actually changed
            if (track.track_id === lastRenderedTrackId) return;
            lastRenderedTrackId = track.track_id;
            window._currentTrackId = track.track_id;

            container.innerHTML = `
                <div class="music-card" style="border-left-color:${data.color}">
                    <div class="song-label">${moodEmoji} ${langFlag} Spotify &nbsp;·&nbsp;
                        <span style="text-transform:capitalize">${data.language || 'english'}</span>
                    </div>
                    <div class="song-title">${track.song_name}</div>
                    <div class="song-artist">by ${track.artist}</div>
                </div>
                <div class="spotify-embed">
                    <iframe
                        src="https://open.spotify.com/embed/track/${track.track_id}?utm_source=generator&theme=0&autoplay=1"
                        width="100%" height="152"
                        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                        loading="lazy">
                    </iframe>
                </div>`;
        } else {
            lastRenderedTrackId = '';
            container.innerHTML = `
                <div class="music-card" style="border-left-color:${data.color}">
                    <div class="song-label">${moodEmoji} Spotify</div>
                    <div class="song-title">No track available</div>
                    <div class="song-artist">Switch to Offline mode</div>
                </div>`;
        }
    } else {
        // ── Offline Player ────────────────────────────────────────────────────
        const audioUrl = data.audio_url;
        const songName = data.offline ? data.offline.song_title : 'Unknown';
        const artist   = data.offline ? data.offline.artist     : 'Unknown';
        lastRenderedTrackId = audioUrl || '';

        if (audioUrl) {
            window._currentAudioUrl = audioUrl;
            container.innerHTML = `
                <div class="music-card offline" style="border-left-color:${data.color}">
                    <div class="song-label">${moodEmoji} 💿 Local Audio &nbsp;·&nbsp;
                        <span style="text-transform:capitalize">${data.language || 'english'}</span>
                    </div>
                    <div class="song-title">${songName}</div>
                    <div class="song-artist">by ${artist}</div>
                </div>

                <div class="custom-player" id="customPlayer">
                    <div class="player-art" style="background:radial-gradient(circle,${data.color}30,transparent 70%)">
                        <span class="mood-emoji-big">${moodEmoji}</span>
                        <div class="eq-bars" id="eqBars">
                            <span></span><span></span><span></span><span></span><span></span>
                        </div>
                    </div>

                    <div class="player-timeline">
                        <span class="player-time" id="timeCurrent">0:00</span>
                        <input type="range" class="player-progress" id="progressBar" value="0" min="0" max="100" step="0.1">
                        <span class="player-time" id="timeTotal">0:00</span>
                    </div>

                    <div class="player-btns">
                        <button class="player-btn" id="restartBtn" title="Restart">⏮</button>
                        <button class="player-btn play-btn" id="playPauseBtn" title="Play / Pause">▶</button>
                        <button class="player-btn" id="skipBtn" title="Next Track">⏭</button>
                    </div>

                    <div class="player-volume">
                        <span>🔊</span>
                        <input type="range" class="volume-slider" id="volumeSlider" min="0" max="100" value="80">
                        <span id="volPct">80%</span>
                    </div>

                    <audio id="inPageAudio" preload="auto">
                        <source src="${audioUrl}" type="audio/mpeg">
                    </audio>
                </div>`;
            setupPlayer();
        } else {
            lastRenderedTrackId = '';
            container.innerHTML = `
                <div class="music-card offline" style="border-left-color:${data.color}">
                    <div class="song-label">${moodEmoji} Mood Detected</div>
                    <div class="song-title">${songName}</div>
                    <div class="song-artist">by ${artist}</div>
                </div>
                <div class="no-audio-msg">
                    <span>${moodEmoji}</span>
                    <p>No local audio for this emotion.<br>Add MP3s to <code>local_music/</code>.</p>
                </div>`;
        }
    }
}

// ── Audio Player Setup ────────────────────────────────────────────────────────
function setupPlayer() {
    const audio       = document.getElementById('inPageAudio');
    const playBtn     = document.getElementById('playPauseBtn');
    const progressBar = document.getElementById('progressBar');
    const timeCurrent = document.getElementById('timeCurrent');
    const timeTotal   = document.getElementById('timeTotal');
    const volSlider   = document.getElementById('volumeSlider');
    const volPct      = document.getElementById('volPct');
    const eqBars      = document.getElementById('eqBars');
    if (!audio) return;

    audio.volume = 0.8;
    audio.play().catch(() => { if (playBtn) playBtn.textContent = '▶'; });

    audio.addEventListener('loadedmetadata', () => {
        progressBar.max        = audio.duration;
        timeTotal.textContent  = fmt(audio.duration);
    });

    audio.addEventListener('timeupdate', () => {
        progressBar.value         = audio.currentTime;
        timeCurrent.textContent   = fmt(audio.currentTime);
        const pct = (audio.currentTime / (audio.duration || 1)) * 100;
        progressBar.style.background =
            `linear-gradient(to right, var(--accent-color) ${pct}%, rgba(255,255,255,0.15) ${pct}%)`;
    });

    audio.addEventListener('play',  () => { playBtn && (playBtn.textContent = '⏸'); eqBars?.classList.add('playing'); });
    audio.addEventListener('pause', () => { playBtn && (playBtn.textContent = '▶'); eqBars?.classList.remove('playing'); });
    audio.addEventListener('ended', () => { eqBars?.classList.remove('playing'); fetchNextTrack(currentMood, true); });

    playBtn?.addEventListener('click', () => { audio.paused ? audio.play() : audio.pause(); });

    progressBar?.addEventListener('input', () => { audio.currentTime = parseFloat(progressBar.value); });

    volSlider?.addEventListener('input', () => {
        audio.volume = volSlider.value / 100;
        if (volPct) volPct.textContent = volSlider.value + '%';
    });

    document.getElementById('restartBtn')?.addEventListener('click', () => { audio.currentTime = 0; audio.play(); });
    document.getElementById('skipBtn')?.addEventListener('click',    () => { fetchNextTrack(currentMood, true); });
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function fmt(sec) {
    if (!isFinite(sec) || isNaN(sec)) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}
