import json

# Load Arabic and English structured files
with open("quran.json", "r", encoding="utf-8") as f:
    arabic = json.load(f)

with open("quran_en.json", "r", encoding="utf-8") as f:
    english = json.load(f)

combined = []

# Loop through each surah and each verse inside it
for surah_ar, surah_en in zip(arabic, english):
    surah_num = surah_ar["id"]
    verses_ar = surah_ar["verses"]
    verses_en = surah_en["verses"]

    for verse_ar, verse_en in zip(verses_ar, verses_en):
        combined.append({
            "surah": surah_num,
            "ayah": verse_ar["id"],
            "text": verse_ar["text"],
            "translation": verse_en["translation"]
        })

# Save to a new clean JSON file
with open("quran_ar_en.json", "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print("✅ Merged Qur’an file saved as 'quran_ar_en.json'")
