import tkinter as tk
from veri_duzenleme import *
from tkinter import messagebox

sayfalar = {}

renkler = ["#f7f7f7","#639bff","#000000","#ecf0f1","#a8db2b","#b70000","#e4b133"]


def start_app():
    root = tk.Tk()
    root.title("Araç Kiralama Sistemi")
    root.geometry("900x550")
    baslik_olustur(root)
    menu_olustur(root)
    anabolum_olustur(root)
    root.mainloop()

def baslik_olustur(root):
    header = tk.Frame(root, height=80, bg=renkler[1])
    header.pack(fill="x")
    tk.Label(header,text="🚗 Araç Kiralama Sistemi ✈️",fg=renkler[0], bg=renkler[1],font=("Arial",20,"bold")).pack(pady=20)

def menu_olustur(root):
    menu = tk.Frame(root, height=60, bg=renkler[3])
    menu.pack(fill="x")
    tk.Button(menu, text="Araçlar",command=lambda: sayfa_goster("araclar")).pack(side="left", padx=10, pady=10)
    tk.Button(menu, text="Araç Ekle",command=lambda: sayfa_goster("arac_ekle")).pack(side="left", padx=10, pady=10)
    tk.Button(menu, text="Yardım",command=lambda: sayfa_goster("yardim")).pack(side="left", padx=10, pady=10)

def anabolum_olustur(root):
    global ana_frame
    ana_frame = tk.Frame(root)
    ana_frame.pack(fill="both", expand=True)
    sayfalar["araclar"] = araclar_sayfasi(ana_frame)
    sayfalar["arac_ekle"] = arac_ekle_sayfasi(ana_frame)
    sayfalar["yardim"] = yardim_sayfasi(ana_frame)
    sayfa_goster("araclar")

def sayfa_goster(ad):
    for sayfa in sayfalar.values():
        sayfa.pack_forget()
    sayfalar[ad].pack(fill="both", expand=True)

def araclar_sayfasi(baba_frame):
    anaframe = tk.Frame(baba_frame)
    anaframe.pack(fill="both", expand=True)
    filtre_alani = tk.Frame(anaframe, width=250, bg=renkler[3])
    filtre_alani.pack(side="left", fill="y")
    filtre_alani.pack_propagate(False)
    sag_frame = tk.Frame(anaframe)
    sag_frame.pack(side="left", fill="both", expand=True)
    canvas = tk.Canvas(sag_frame, bg=renkler[0])
    canvas.pack(side="left", fill="both", expand=True)

    global ana_canvas
    ana_canvas = canvas
    canvas.bind_all("<MouseWheel>", mouse_wheel)
    scrollbar = tk.Scrollbar(sag_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas, bg=renkler[0])
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    tk.Label(filtre_alani, text="Filtreler",fg=renkler[0], bg=renkler[1],font=("Arial", 11, "bold")).pack(fill="x", pady=(0,5))
    tk.Label(filtre_alani, text="Markalar", bg=renkler[3],font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    global markalar_frame
    markalar_frame = tk.Frame(filtre_alani, bg=renkler[3])
    markalar_frame.pack(fill="x")
    marka_butonlari_olustur(markalar_frame)
    tk.Label(filtre_alani, text="Fiyat Aralığı", bg=renkler[3],font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    global fiyatlar_frame
    fiyatlar_frame = tk.Frame(filtre_alani, bg=renkler[3])
    fiyatlar_frame.pack(fill="x")
    fiyat_butonlari_olustur(fiyatlar_frame)

    tk.Button(filtre_alani, text="Filtrele",command=lambda: checkbox_filtrele(marka_vars, fiyat_vars)).pack(pady=5)
    tk.Button(filtre_alani, text="Temizle",command=lambda: filtreleri_temizle(marka_vars, fiyat_vars)).pack(pady=5)
    arama_alani = tk.Frame(frame, bg=renkler[0])
    arama_alani.pack(fill="x")
    arama_alani_olustur(arama_alani)

    kartlar_alani = tk.Frame(frame, bg=renkler[0])
    kartlar_alani.pack(fill="both", expand=True)

    global icerik_ref
    icerik_ref = kartlar_alani

    araclari_goster()

    return anaframe


def mouse_wheel(event):
    ana_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def marka_butonlari_olustur(alan):
    global marka_vars
    marka_vars = {}
    for buton in alan.winfo_children():
        buton.pack_forget()
    for marka in markalari_getir():
        var = tk.BooleanVar()
        marka_vars[marka] = var
        tk.Checkbutton(alan, text=marka, variable=var,bg=renkler[3]).pack(anchor="w", padx=20)
def fiyat_butonlari_olustur(alan):
    global fiyat_vars
    fiyat_vars = {}
    for buton in alan.winfo_children():
        buton.pack_forget()
    for min_f, max_f in fiyat_araliklarini_getir():
        var = tk.BooleanVar()
        fiyat_vars[(min_f, max_f)] = var
        tk.Checkbutton(
            alan,text=f"{min_f} – {max_f} ₺",variable=var,bg=renkler[3]).pack(anchor="w", padx=20)
def filtreleri_temizle(marka_vars, fiyat_vars):
    for var in marka_vars.values():
        var.set(False)
    for var in fiyat_vars.values():
        var.set(False)
    araclar_sayfasini_yenile()
    scroll_guncelle()

def kartlari_temizle():
    for widget in icerik_ref.winfo_children():
        widget.destroy()

def arac_ekle_sayfasi(baba_frame):
    anaframe = tk.Frame(baba_frame)
    anaframe.pack(fill="both", expand=True)
    canvas = tk.Canvas(anaframe, bg=renkler[0])
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(anaframe, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas, bg=renkler[0])
    canvas_window = canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",lambda e: canvas.itemconfig(canvas_window, width=e.width))
    tk.Label(frame, text="Araç Ekle",font=("Arial", 18, "bold")).pack(fill="x", pady=20)
    tk.Label(frame, text="Plaka").pack(anchor="w", padx=40)
    plaka_entry = tk.Entry(frame)
    plaka_entry.pack(fill="x", padx=40, pady=5)
    tk.Label(frame, text="Marka").pack(anchor="w", padx=40)
    marka_entry = tk.Entry(frame)
    marka_entry.pack(fill="x", padx=40, pady=5)
    tk.Label(frame, text="Model").pack(anchor="w", padx=40)
    model_entry = tk.Entry(frame)
    model_entry.pack(fill="x", padx=40, pady=5)
    tk.Label(frame, text="Günlük Ücret").pack(anchor="w", padx=40)
    ucret_entry = tk.Entry(frame)
    ucret_entry.pack(fill="x", padx=40, pady=5)
    def formdan_arac_ekle():
        try:
            if not plaka_entry.get() or not marka_entry.get() or not model_entry.get():
                messagebox.showerror("Hata", "Tüm alanlar doldurulmalı")
                return
            ucret = int(ucret_entry.get())
            arac = {"plaka": plaka_entry.get(),"marka": marka_entry.get(),"model": model_entry.get(),"gunluk_ucret": ucret}
            arac_ekle(arac)
            messagebox.showinfo("Başarılı", "Araç eklendi")
            plaka_entry.delete(0, tk.END)
            marka_entry.delete(0, tk.END)
            model_entry.delete(0, tk.END)
            ucret_entry.delete(0, tk.END)
            araclar_sayfasini_yenile()
        except ValueError:
            messagebox.showerror("Hata", "Günlük ücret sayı olmalı")
    tk.Button(frame, text="Aracı Kaydet", command=formdan_arac_ekle).pack(pady=20)
    return anaframe

def araclari_goster():
    kartlari_temizle()
    for arac in araclari_oku():
        aracKarti_olustur(icerik_ref, arac)
    scroll_guncelle()


def araclar_sayfasini_yenile():
    if icerik_ref:
        araclari_goster()
        marka_butonlari_olustur(markalar_frame)
        fiyat_butonlari_olustur(fiyatlar_frame)


def yardim_sayfasi(baba_frame):
    anaframe = tk.Frame(baba_frame)
    anaframe.pack(fill="both", expand=True)
    canvas = tk.Canvas(anaframe, bg=renkler[0])
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(anaframe, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas, bg=renkler[0])
    canvas_window = canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",lambda e: canvas.itemconfig(canvas_window, width=e.width))
    tk.Label(frame,text="Yardım",font=("Arial", 18, "bold")).pack(fill="x", pady=20)
    tk.Label(frame,text="Öneri ve geri bildirim için\n").pack(fill="x", padx=40, pady=3)

    return anaframe


def arama_alani_olustur(ana_frame):
    frame = tk.Frame(ana_frame, bg=renkler[0], pady=10)
    frame.pack(fill="x", padx=20)
    tk.Label(frame,text="Araç Ara:",font=("Arial", 11, "bold"),bg=renkler[0]).pack(side="left")
    entry = tk.Entry(frame, width=80,bd=1,relief="solid")
    entry.pack(side="left", padx=10)
    tk.Button(frame,text="Ara",command=lambda:arama_kontrol(entry.get())).pack(side="left")

def aracKarti_olustur(ana_frame, arac):
    kart = tk.Frame(ana_frame, bg=renkler[0], bd=1, relief="solid")
    kart.pack(fill="x", padx=20, pady=10)
    sol = tk.Frame(kart, bg=renkler[0])
    sol.pack(side="left", padx=10, pady=10)
    tk.Label(sol, text=f"Plaka: {arac['plaka']}").pack(anchor="w")
    tk.Label(sol, text=f"{arac['marka']} {arac['model']}").pack(anchor="w")
    tk.Label(sol, text=f"Günlük Ücret: {arac['gunluk_ucret']} ₺").pack(anchor="w")
    durum = arac["durum"].capitalize()
    tk.Label(sol, text=f"Durum: {durum}").pack(anchor="w")
    sağ = tk.Frame(kart, bg=renkler[0], width=120)
    sağ.pack(side="right", padx=10)
    img = tk.PhotoImage(file=arac['fotograf'],width=125,height=125)
    lbl = tk.Label(sağ, image=img,bg=renkler[0])
    lbl.image = img
    lbl.pack()

    if arac["silinebilir"]:
        tk.Button(sağ, text="Düzenle", bg=renkler[1], fg=renkler[2],command=lambda a=arac: arac_duzenleme_penceresi(a)).pack(pady=5)
        tk.Button(sağ, text="Sil", fg=renkler[0], bg=renkler[5], command=lambda p=arac["plaka"]: sil_ve_yenile(p)).pack(pady=5)
    else:
        if arac["durum"] == "müsait":
            tk.Button(kart,text="Kirala",bg=renkler[6],fg=renkler[2],command=lambda p=arac["plaka"]: kiralama_penceresi(p)).pack(pady=5)
        else:
            tk.Button(kart,text="İade Et",bg=renkler[4],command=lambda p=arac["plaka"]: iade_ve_yenile(p)).pack(pady=5)

    if arac["durum"] == "kirada":
        tk.Label(sol, text=f"Müşteri: {arac['musteri_ad']}").pack(anchor="w")
        tk.Label(sol, text=f"{arac['baslangic_tarihi']} → {arac['bitis_tarihi']}").pack(anchor="w")


def sil_ve_yenile(plaka):
    if messagebox.askyesno("Onay", "Bu aracı silmek istiyor musun?"):
        arac_sil(plaka)
        araclar_sayfasini_yenile()

def iade_ve_yenile(plaka):
    ucret = arac_iade(plaka)
    messagebox.showinfo("İade", f"Toplam ücret: {ucret} TL")
    araclar_sayfasini_yenile()

def arac_duzenleme_penceresi(arac):
    pencere = tk.Toplevel()
    pencere.title("Araç Düzenle")
    pencere.geometry("300x300")
    tk.Label(pencere, text="Plaka (Değiştirilemez)").pack()
    tk.Label(pencere, text=arac["plaka"], fg=renkler[0]).pack()
    tk.Label(pencere, text="Marka").pack()
    marka_entry = tk.Entry(pencere)
    marka_entry.insert(0, arac["marka"])
    marka_entry.pack()
    tk.Label(pencere, text="Model").pack()
    model_entry = tk.Entry(pencere)
    model_entry.insert(0, arac["model"])
    model_entry.pack()
    tk.Label(pencere, text="Günlük Ücret").pack()
    ucret_entry = tk.Entry(pencere)
    ucret_entry.insert(0, str(arac["gunluk_ucret"]))
    ucret_entry.pack()
    def kaydet():
        try:
            guncelle_arac(
                arac["plaka"],
                marka_entry.get(),
                model_entry.get(),
                int(ucret_entry.get())
            )
            messagebox.showinfo("Başarılı", "Araç güncellendi")
            pencere.destroy()
            araclar_sayfasini_yenile()
        except ValueError:
            messagebox.showerror("Hata", "Ücret sayı olmalı")

    tk.Button(pencere, text="Kaydet", command=kaydet).pack(pady=15)

def kiralama_penceresi(plaka):
    pencere = tk.Toplevel()
    pencere.title("Araç Kirala")
    pencere.geometry("300x320")
    tk.Label(pencere, text="Müşteri Ad Soyad").pack()
    ad_entry = tk.Entry(pencere)
    ad_entry.pack()
    tk.Label(pencere, text="Başlangıç Tarihi (YYYY-AA-GG)").pack()
    bas_entry = tk.Entry(pencere)
    bas_entry.pack()
    tk.Label(pencere, text="Bitiş Tarihi (YYYY-AA-GG)").pack()
    bit_entry = tk.Entry(pencere)
    bit_entry.pack()
    def kirala():
        try:
            baslangic = datetime.strptime(bas_entry.get(), "%Y-%m-%d")
            bitis = datetime.strptime(bit_entry.get(), "%Y-%m-%d")
            if baslangic.date() < datetime.today().date() or bitis.date() < datetime.today().date():
                messagebox.showerror("Hata", "Girilen tarih geçerli değil")
                return
            if bitis <= baslangic:
                messagebox.showerror("Hata", "Bitiş tarihi başlangıçtan sonra olmalı")
                return
            gun = (bitis - baslangic).days
            arac_kirala(plaka,ad_entry.get(),baslangic.strftime("%Y-%m-%d"),bitis.strftime("%Y-%m-%d"),gun)
            messagebox.showinfo("Başarılı", "Araç kiralandı")
            pencere.destroy()
            araclar_sayfasini_yenile()
        except ValueError:
            messagebox.showerror("Hata", "Tarih formatı hatalı")
    tk.Button(pencere, text="Kirala", command=kirala).pack(pady=20)

def arama_kontrol(aranan):
    aranan = aranan.lower().strip()
    tum_araclar = araclari_oku()
    sonuc = []
    for arac in tum_araclar:
        if (aranan in arac["plaka"].lower()or aranan in arac["marka"].lower()or aranan in arac["model"].lower()):
            sonuc.append(arac)
    kartlari_temizle()
    for arac in sonuc:
        aracKarti_olustur(icerik_ref, arac)
    scroll_guncelle()

def markalari_getir():
    markalar = set()
    for arac in araclari_oku():
        markalar.add(arac["marka"])
    return sorted(markalar)

def fiyat_araliklarini_getir(adim=200):
    fiyatlar = [a["gunluk_ucret"] for a in araclari_oku()]
    if not fiyatlar:
        return []
    minfiyat = min(fiyatlar)
    maxfiyat = max(fiyatlar)
    araliklar = []
    baslangic = (minfiyat // adim) * adim
    while baslangic <= maxfiyat:
        bitis = baslangic + adim - 1
        araliklar.append((baslangic, bitis))
        baslangic += adim
    return araliklar

def checkbox_filtrele(marka_vars, fiyat_vars):
    secili_markalar = [marka for marka, var in marka_vars.items() if var.get()]
    secili_araliklar = [aralik for aralik, var in fiyat_vars.items() if var.get()]
    sonuc = []
    for arac in araclari_oku():
        marka_ok = (not secili_markalar or arac["marka"] in secili_markalar)
        fiyat_ok = False
        if not secili_araliklar:
            fiyat_ok = True
        else:
            for min_f, max_f in secili_araliklar:
                if min_f <= arac["gunluk_ucret"] <= max_f:
                    fiyat_ok = True
                    break
        if marka_ok and fiyat_ok:
            sonuc.append(arac)
    kartlari_temizle()
    for arac in sonuc:
        aracKarti_olustur(icerik_ref, arac)
    scroll_guncelle()

def scroll_guncelle():
    if ana_canvas:
        ana_canvas.update_idletasks()
        ana_canvas.configure(scrollregion=ana_canvas.bbox("all"))