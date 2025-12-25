import json
import os
from datetime import datetime

veri_dosyasi = "data/araclar.json"

def araclari_oku():
    if not os.path.exists(veri_dosyasi):
        return []
    with open(veri_dosyasi, "r", encoding="utf-8") as f:
        araclar = json.load(f)
    for arac in araclar:
        arac.setdefault("fotograf", "assets/default.png")
        arac.setdefault("durum", "müsait")
        arac.setdefault("musteri_ad", "")
        arac.setdefault("gun_sayisi", 0)
        arac.setdefault("silinebilir", False)
    return araclar

def arac_ekle(arac):
    araclar = araclari_oku()
    araclar.append({"plaka": arac["plaka"],"marka": arac["marka"],"model": arac["model"],"fotograf":arac["fotograf"],"gunluk_ucret": arac["gunluk_ucret"],"durum": "müsait","musteri_ad": "","gun_sayisi": 0,"silinebilir":True})
    with open(veri_dosyasi, "w", encoding="utf-8") as f:
        json.dump(araclar, f, ensure_ascii=False, indent=4)

def arac_sil(plaka):
    with open(veri_dosyasi, "r", encoding="utf-8") as f:
        araclar = json.load(f)
    araclar = [a for a in araclar if a["plaka"] != plaka]
    with open(veri_dosyasi, "w", encoding="utf-8") as f:
        json.dump(araclar, f, ensure_ascii=False, indent=4)

def arac_kirala(plaka, musteri_ad, baslangic, bitis, gun_sayisi):
    with open(veri_dosyasi, "r", encoding="utf-8") as f:
        araclar = json.load(f)
    for arac in araclar:
        if arac["plaka"] == plaka and arac["durum"] == "müsait":
            arac["durum"] = "kirada"
            arac["musteri_ad"] = musteri_ad
            arac["baslangic_tarihi"] = baslangic
            arac["bitis_tarihi"] = bitis
            arac["gun_sayisi"] = gun_sayisi
            break
    with open(veri_dosyasi, "w", encoding="utf-8") as f:
        json.dump(araclar, f, ensure_ascii=False, indent=4)

def arac_iade(plaka):
    with open(veri_dosyasi, "r", encoding="utf-8") as f:
        araclar = json.load(f)
    ucret = 0
    for arac in araclar:
        if arac["plaka"] == plaka and arac["durum"] == "kirada":
            ucret = arac["gun_sayisi"] * arac["gunluk_ucret"]
            arac["durum"] = "müsait"
            arac["musteri_ad"] = ""
            arac["gun_sayisi"] = 0
            break
    with open(veri_dosyasi, "w", encoding="utf-8") as f:
        json.dump(araclar, f, ensure_ascii=False, indent=4)
    return ucret

def guncelle_arac(plaka, marka, model, gunluk_ucret):
    with open(veri_dosyasi, "r", encoding="utf-8") as f:
        araclar = json.load(f)
    for arac in araclar:
        if arac["plaka"] == plaka:
            arac["marka"] = marka
            arac["model"] = model
            arac["gunluk_ucret"] = gunluk_ucret
            break
    with open(veri_dosyasi, "w", encoding="utf-8") as f:
        json.dump(araclar, f, ensure_ascii=False, indent=4)