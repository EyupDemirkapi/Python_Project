import json
import os
veri_dosyasi = "data/araclar.json"


def veri_oku():
    if not os.path.exists(veri_dosyasi):
        return []
    with open(veri_dosyasi, "r", encoding="utf-8") as file:
        return json.load(file)

def veri_yaz(arac_listesi):
    with open(veri_dosyasi, "w", encoding="utf-8") as file:
        json.dump(arac_listesi, file, ensure_ascii=False, indent=4)
