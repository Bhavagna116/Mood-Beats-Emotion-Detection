import urllib.request
import json
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Get anonymous token
try:
    req = urllib.request.Request("https://open.spotify.com/get_access_token?reason=transport&productType=web_player", headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, context=ctx)
    data = json.loads(resp.read().decode('utf-8'))
    token = data.get('accessToken')
    if not token:
        print("No token")
        sys.exit(1)
except Exception as e:
    print("Failed token", e)
    sys.exit(1)

# 2. Search function
def search_spotify(query, limit=3):
    url = f"https://api.spotify.com/v1/search?type=track&q={urllib.parse.quote(query)}&limit={limit}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = urllib.request.urlopen(req, context=ctx)
        d = json.loads(resp.read().decode('utf-8'))
        tracks = d.get("tracks", {}).get("items", [])
        return [(t["id"], t["name"], t["artists"][0]["name"]) for t in tracks]
    except Exception as e:
        print("Fail search", e)
        return []

queries = {
    "hindi": {
        "happy": ["Badtameez Dil", "Gallan Goodiyaan", "Kar Gayi Chull"],
        "sad": ["Agar Tum Saath Ho", "Channa Mereya", "Kabira"],
        "angry": ["Ek Villain", "Sultan Title Track", "Krrish"],
        "fear": ["Ek Thi Daayan", "Raaz", "Bhool Bhulaiyaa"],
        "disgust": ["Beedi", "Munni Badnaam Hui", "Sheila Ki Jawani"],
        "neutral": ["Kun Faya Kun", "Iktara", "Dil Se Re"],
        "surprise": ["Kala Chashma", "Dhoom Machale", "Dhan Te Nan"]
    },
    "telugu": {
        "happy": ["Samajavaragamana", "Butta Bomma", "Naatu Naatu"],
        "sad": ["Nuvvante Na Ishtam", "Pillagada", "Oka Lalana"],
        "angry": ["Simha", "Aarya 2", "Tagore"],
        "fear": ["Arundhati", "Rakshasi", "Magadheera"],
        "disgust": ["Dookudu", "Baahubali", "Pokiri"],
        "neutral": ["Ye Maya Chesave", "Oohalu Gusagusalade", "Emo Emo"],
        "surprise": ["Rangamma Mangamma", "Sarrainodu", "Allu Arjun mass bgm"]
    }
}

result = {}
for lang, emos in queries.items():
    result[lang] = {}
    for emo, qlist in emos.items():
        result[lang][emo] = []
        for q in qlist:
            found = search_spotify(q + " " + lang, 1)
            if found:
                result[lang][emo].append(found[0])

print("DONE")
print(result)
