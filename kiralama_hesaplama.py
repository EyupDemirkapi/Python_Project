from datetime import datetime

def gun_hesapla(baslangic_tarihi, bitis_tarihi):
    baslangic = datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
    bitis = datetime.strptime(bitis_tarihi, "%Y-%m-%d")
    return (bitis - baslangic).days

def arac_kirala(arac, musteri, baslangic_tarihi, bitis_tarihi):
    arac["durum"] = "kirada"
    arac["kiralayan"] = musteri
    arac["baslangic_tarihi"] = baslangic_tarihi
    arac["bitis_tarihi"] = bitis_tarihi

def arac_iade(arac):
    arac["durum"] = "müsait"
    arac["kiralayan"] = ""
    arac["baslangic_tarihi"] = ""
    arac["bitis_tarihi"] = ""
