import json
import re
from fuzzywuzzy import process, fuzz

def normalize_arabic(text):
    # Remove diacritics and unwanted symbols
    text = re.sub(r'[ًٌٍَُِّْۣۡۗۚۛۜ۞]', '', text)  # Harakāt & small signs
    text = re.sub(r'[^\w\s]', '', text)             # Remove punctuation
    text = text.replace("ـ", "")                    # Tatweel
    return text.strip()

# Load Whisper lines
with open("whisper_output.txt", "r", encoding="utf-8") as f:
    lines = [normalize_arabic(line.strip()) for line in f if line.strip()]

# Load Quran
with open("quran_ar_en.json", "r", encoding="utf-8") as f:
    quran = json.load(f)

# Build normalized ayah list
ayah_map = {}
for ayah in quran:
    clean_text = normalize_arabic(ayah["text"])
    ayah_map[clean_text] = ayah

# Match each line
print(f"\n🔍 Matching {len(lines)} lines...\n")

for line in lines:
    best_match, score = process.extractOne(line, list(ayah_map.keys()), scorer=fuzz.token_set_ratio)

    if score >= 65:
        ayah = ayah_map[best_match]
        print(f"📖 Whisper: {line}")
        print(f"🕌 Surah {ayah['surah']}, Ayah {ayah['ayah']}")
        print(f"🧠 Arabic: {ayah['text']}")
        print(f"🌍 English: {ayah['translation']}")
        print("-" * 60)
    else:
        print(f"⚠️ No confident match for: {line} (score {score}) — skipping\n")
