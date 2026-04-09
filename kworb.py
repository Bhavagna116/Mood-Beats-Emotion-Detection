import urllib.request
import re

try:
    req = urllib.request.Request('https://kworb.net/spotify/country/in_daily.html', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = re.findall(r'href="../track/(.{22})\.html">(.*?)</a>(.*?)<td', html) # Kworb format
    if not matches:
        matches = re.findall(r'href=\'../track/(.{22})\.html\'>(.*?)</a>', html)
    
    print("Found", len(matches), "matches")
    for group in matches[:100]:
        print(group[0], group[1][:50])
except Exception as e:
    print("Error:", e)
