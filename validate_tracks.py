import urllib.request
import urllib.error
from src.config import LANGUAGE_EMOTION_TRACKS

valid_tracks = {}
for lang, emo_dict in LANGUAGE_EMOTION_TRACKS.items():
    valid_tracks[lang] = {}
    for emo, tracks in emo_dict.items():
        valid_tracks[lang][emo] = []
        for track in tracks:
            track_id, name, artist = track
            url = 'https://open.spotify.com/track/' + track_id
            try:
                # Add User-Agent to avoid generic blocks
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                urllib.request.urlopen(req)
                valid_tracks[lang][emo].append(track)
            except Exception as e:
                pass

print('Counts:')
for lang, emo_dict in valid_tracks.items():
    print(lang, {k: len(v) for k, v in emo_dict.items()})

print('\nValid Config:')
print('EMOTION_TRACKS_ENGLISH =', valid_tracks['english'])
print('\nEMOTION_TRACKS_HINDI =', valid_tracks['hindi'])
print('\nEMOTION_TRACKS_TELUGU =', valid_tracks['telugu'])
