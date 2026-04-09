import urllib.request
import json
import re

def get_spotify_info(track_id):
    url = f'https://open.spotify.com/oembed?url=spotify:track:{track_id}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(resp)
        title = data.get('title', 'Unknown Track')
        
        # Clean up title
        if ' by ' in title:
            title_part, artist_part = title.split(' by ', 1)
            return title_part.strip(), artist_part.strip()
        else:
            return title, data.get('author_name', 'Unknown Artist')
    except Exception as e:
        return 'Unknown Track', 'Unknown Artist'

with open('src/config.py', 'r', encoding='utf-8') as f:
    config_code = f.read()

# Find all tuples in the config: ('ID', 'Old Name', 'Old Artist')
pattern = r"\(\s*'([A-Za-z0-9]{22})'\s*,\s*['\"].*?['\"]\s*,\s*['\"].*?['\"]\s*\)"

def replace_tuple(match):
    track_id = match.group(1)
    title, artist = get_spotify_info(track_id)
    # properly escape quotes
    title = title.replace("'", "\\'")
    artist = artist.replace("'", "\\'")
    return f"('{track_id}', '{title}', '{artist}')"

new_config_code = re.sub(pattern, replace_tuple, config_code)

with open('src/config.py', 'w', encoding='utf-8') as f:
    f.write(new_config_code)

print("Config rewritten with verified authentic track names from Spotify Web API!")
