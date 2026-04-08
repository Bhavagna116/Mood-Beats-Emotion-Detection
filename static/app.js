const video = document.getElementById('videoElement');
const canvas = document.getElementById('canvasElement');
const ctx = canvas.getContext('2d');
const processedFrame = document.getElementById('processedFrame');
const videoContainer = document.getElementById('videoContainer');
const fileInput = document.getElementById('fileInput');

let currentMood = 'neutral';
let currentMusicMode = 'online'; // online or offline
let isStreaming = false;
let streamingInterval = null;

// Tab logic
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
        
        if (btn.dataset.tab !== 'live' && isStreaming) {
            stopCamera();
        }
    });
});

// Mode Toggle logic
document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMusicMode = btn.dataset.mode;
        
        // Ask for new track based on current mood manually to trigger mode switch UI
        fetchNextTrack(currentMood, false);
    });
});

// Video stream logic
document.getElementById('startBtn').addEventListener('click', async () => {
    if (isStreaming) return;
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
        video.srcObject = stream;
        video.classList.remove('hidden');
        processedFrame.classList.add('hidden');
        isStreaming = true;
        videoContainer.classList.add('active-stream');
        
        video.onloadedmetadata = () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        };

        // Poll frames every 400ms (approx 2.5 FPS) to save bandwidth but respond fast
        streamingInterval = setInterval(processFrame, 400);
        
    } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Camera access is required for live detection.");
    }
});

document.getElementById('stopBtn').addEventListener('click', stopCamera);

function stopCamera() {
    if (!isStreaming) return;
    
    clearInterval(streamingInterval);
    const stream = video.srcObject;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
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
            body: JSON.stringify({ frame: frameData })
        });
        
        if (response.ok) {
            const result = await response.json();
            updateUI(result);
            
            // Show bounding box
            if (result.processed_image) {
                video.classList.add('hidden');
                processedFrame.classList.remove('hidden');
                processedFrame.src = result.processed_image;
            }
        }
    } catch (err) {
        console.error("Frame processing error:", err);
    }
}

// Photo Upload Logic
fileInput.addEventListener('change', async (e) => {
    if (!e.target.files.length) return;
    const file = e.target.files[0];
    
    document.getElementById('fileUploadContainer').classList.add('input-filled');
    document.getElementById('fileUploadContainer').querySelector('h4').textContent = file.name;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/detect/photo', {
            method: 'POST',
            body: formData
        });
        
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
    } catch (err) {
        console.error("Photo processing error:", err);
    }
});

document.getElementById('clearPhotoBtn')?.addEventListener('click', () => {
    document.getElementById('photoResultContainer').classList.add('hidden');
    document.getElementById('photoControls').classList.add('hidden');
    document.getElementById('fileUploadContainer').classList.remove('hidden');
    document.getElementById('fileUploadContainer').classList.remove('input-filled');
    document.getElementById('fileUploadContainer').querySelector('h4').textContent = 'Click to Upload Photo';
    fileInput.value = '';
});

function updateUI(result) {
    if (result.emotion !== currentMood) {
        currentMood = result.emotion;
        
        // 1. Change website color dynamically matching mood
        document.documentElement.style.setProperty('--accent-color', result.color);
        
        // 2. Update global badge
        document.getElementById('globalMoodBadge').textContent = currentMood;
        
        // 3. Update music suggestion text
        document.getElementById('musicStatusText').textContent = `Your ${currentMood.charAt(0).toUpperCase() + currentMood.slice(1)} Mix:`;
        
        // 4. Update the Music Player
        renderMusicDetails(result);
    }
}

async function fetchNextTrack(emotion, excludeCurrent=false) {
    let excludeOpt = ""; 
    try {
        const resp = await fetch('/api/next-track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                emotion, 
                exclude: excludeCurrent ? window._currentTrackId : ""
            })
        });
        if(resp.ok){
            const result = await resp.json();
            // Backend returns the full correctly formatted emotion payload
            renderMusicDetails(result);
            if(result.spotify) window._currentTrackId = result.spotify.track_id;
        }
    } catch(e) {}
}

document.getElementById('nextTrackBtn').addEventListener('click', () => {
    fetchNextTrack(currentMood, true);
});

function renderMusicDetails(data) {
    const container = document.getElementById('musicContainer');
    
    if (currentMusicMode === 'online') {
        const track = data.spotify;
        if(track){
            container.innerHTML = `
                <div class="music-card" style="border-left-color: ${data.color}">
                    <div class="song-label">🎵 Now Playing</div>
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
        const track = data.offline;
        if (track) {
            container.innerHTML = `
                <div class="music-card offline" style="border-left-color: ${data.color}">
                    <div class="song-label">💾 Offline Library</div>
                    <div class="song-title">${track.song_title || track.song_name || 'Unknown'}</div>
                    <div class="song-artist">by ${track.artist || 'Unknown'}</div>
                    <div style="color: #666; font-size: 0.9em; margin-top: 15px;">Playing from local files</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 10px; margin-top: 10px;">
                    <audio id="localAudio" autoplay controls style="width: 100%;">
                        <source src="/api/audio/${encodeURIComponent(track.song_title)}" type="audio/mp3">
                        Your browser does not support audio.
                    </audio>
                </div>
            `;
            
            // Note: to play offline audio smoothly, our Flask server needs to serve audio streams
        } else {
             container.innerHTML = `
                <div class="music-card offline" style="border-left-color: ${data.color}">
                    <div class="song-label">⚠️ No Audio Found</div>
                    <div class="song-title">No offline songs stored</div>
                    <div class="song-artist">for the emotion "${data.emotion}"</div>
                </div>
            `;
        }
    }
}
