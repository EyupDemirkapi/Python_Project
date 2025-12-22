import tkinter as tk
from hata_kontrol import *
from veri_duzenleme import *
from kiralama_hesaplama import *

def start_app():
    root = tk.Tk()
    root.title("Araç Kiralama Sistemi")
    root.geometry("900x550")
    baslik_olustur(root)
    menu_olustur(root)
    anabolum_olustur(root)
    root.mainloop()

def baslik_olustur(root):
    header = tk.Frame(root, height=80, bg="Blue")
    header.pack(fill="x")
    tk.Label(header,text="Araç Kiralama Sistemi",fg="white",bg="Blue",font=("Arial",20,"bold")).pack(pady=20)

def menu_olustur(root):
    menu = tk.Frame(root, height=40, bg="LightGray")
    menu.pack(fill="x")
    for text in ["Araçlar","Form","Yardım"]:
        tk.Button(menu, text=text).pack(side="left",padx=10,pady=5)

def anabolum_olustur(root):
    filtre_alani = tk.Frame(root, width=150, bg="#ecf0f1")
    filtre_alani.pack(side="left", fill="y")
    tk.Label(filtre_alani,text="Filtreler",bg="Gray",font=("Arial",11,"bold")).pack(pady=10)

    canvas = tk.Canvas(root, bg="White")
    canvas.pack(side="left",fill="both",expand=True)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    icerik_alani = tk.Frame(canvas, bg="#ffffff")
    canvas_window_id = canvas.create_window((0,0),window=icerik_alani,anchor="nw")
    canvas.bind("<Configure>",lambda e: canvas.itemconfig(canvas_window_id, width=e.width))
    icerik_alani.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    arama_alani_olustur(icerik_alani)
    for i in range(6):
        aracKarti_olustur(icerik_alani)

def arama_alani_olustur(parent):
    frame = tk.Frame(parent, bg="#ffffff", pady=10)
    frame.pack(fill="x", padx=20)

    tk.Label(frame,text="Araç Ara:",font=("Arial", 11, "bold"),bg="#ffffff").pack(side="left")

    entry = tk.Entry(frame, width=80,bd=1,relief="solid")
    entry.pack(side="left", padx=10)
    tk.Button(frame,text="Ara",command=lambda:arama_kontrol(entry.get())).pack(side="left")

def aracKarti_olustur(icerik_alani):
    kart = tk.Frame(icerik_alani, bg="#f7f7f7", bd=1,relief="solid")
    kart.pack(fill="x", padx=20,pady=10)
    sol = tk.Frame(kart, bg="#f7f7f7")
    sol.pack(side="left", padx=10, pady=10)
    sağ = tk.Frame(kart, bg="#f7f7f7", width=120, height=80)
    sağ.pack(side="right", padx=10)
