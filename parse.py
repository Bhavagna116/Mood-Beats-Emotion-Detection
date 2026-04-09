import re
html = open('kworb_html.txt', 'r', encoding='utf-8').read()
matches = re.findall(r'<a href=\"../track/(.{22})\.html\">(.*?)</a>', html)
tracks = [(i, t.replace('&#39;', "'"), 'Various Artists') for i, t in matches]

hindi = {
    'happy': [tracks[0]],
    'sad': [tracks[1]],
    'angry': [tracks[2]],
    'fear': [tracks[3]],
    'disgust': [tracks[4]],
    'neutral': [tracks[5]],
    'surprise': [tracks[6]]
}

telugu = {
    'happy': [tracks[7]],
    'sad': [tracks[8]],
    'angry': [tracks[9]],
    'fear': [tracks[10]],
    'disgust': [tracks[11]],
    'neutral': [tracks[12]],
    'surprise': [tracks[13]]
}

print("HINDI =", hindi)
print("TELUGU =", telugu)
