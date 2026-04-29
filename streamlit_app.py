import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# =========================================================
# KATALOG ARTIKALA
# =========================================================
katalog = {
    "Meso": {
        "Juneće meso": ["Ramstek", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Rozbif", "File", "Koljenica"],
        "Svinjsko meso": ["Kare", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Trbušina", "Koljenica", "File"],
        "Živinsko meso": ["Pileći file", "Pileći but", "Pileća krilca", "Ćureći file", "Ćureći but", "Pileća jetra"],
        "Jagnjeće meso": ["Jagnjeći but", "Jagnjeća plećka", "Jagnjeća rebra", "Jagnjeći kotlet"],
        "Iznutrice": ["Goveđa jetra", "Svinjska jetra", "Bubrezi", "Srce", "Jezik"]
    },
    "Riba i morski plodovi": {
        "Morska riba": ["Brancin", "Orada", "Tuna", "Losos", "Skuša", "Sardina", "Oslić", "Zubatac"],
        "Rečna riba": ["Šaran", "Som", "Smuđ", "Štuka", "Pastrmka"],
        "Morski plodovi": ["Škampi", "Lignje", "Hobotnica", "Dagnje", "Kamenice", "Jastog"]
    },
    "Povrće": {
        "Lisnato povrće": ["Zelena salata", "Spanać", "Blitva", "Rukola", "Kelj", "Kupus", "Crveni kupus"],
        "Krtolasto povrće": ["Krompir", "Šargarepa", "Cvekla", "Rotkva", "Celer koren", "Batat"],
        "Plodovito povrće": ["Paradajz", "Paprika", "Tikvice", "Patlidžan", "Krastavac", "Brokoli", "Karfiol"],
        "Lukovičasto povrće": ["Crni luk", "Beli luk", "Por", "Mladi luk", "Crveni luk"],
        "Mahunarke": ["Boranija", "Grašak", "Bob", "Leblebija", "Sočivo", "Pasulj"]
    },
    "Voće": {
        "Jezgričavo voće": ["Jabuka", "Kruška", "Dunja"],
        "Koštičavo voće": ["Breskva", "Kajsija", "Trešnja", "Višnja", "Šljiva"],
        "Bobičasto voće": ["Jagoda", "Malina", "Kupina", "Borovnica", "Ribizla"],
        "Citrusi": ["Limun", "Narandža", "Grejpfrut", "Mandarina", "Limeta"],
        "Egzotično voće": ["Banana", "Ananas", "Mango", "Papaja", "Avokado", "Kivi"]
    },
    "Mlečni proizvodi": {
        "Sirevi": ["Beli sir", "Kačkavalj", "Gauda", "Ementaler", "Parmezan", "Mocarela", "Feta", "Ricota"],
        "Mleko i vrhnje": ["Punomasno mleko", "Polumasno mleko", "Slatka pavlaka", "Kisela pavlaka"],
        "Fermentisani proizvodi": ["Jogurt", "Kefir", "Kiselo mleko", "Grčki jogurt"],
        "Maslac i margarin": ["Maslac", "Ghee maslac", "Biljni margarin"]
    },
    "Jaja": {
        "Kokošja jaja": ["Jaja L (63-73g)", "Jaja M (53-63g)", "Jaja XL (73g+)", "Jaja S (ispod 53g)"],
        "Ostala jaja": ["Pačja jaja", "Prepelicija jaja"]
    },
    "Suhe namirnice": {
        "Žitarice i brašno": ["Pšenično brašno T400", "Pšenično brašno T550", "Kukuruzno brašno", "Ovsene pahuljice", "Griz"],
        "Tjestenina i riža": ["Špageti", "Penne", "Fusilli", "Lasagne", "Basmati riža", "Okrugla riža", "Kus kus"],
        "Šećer i zaslađivači": ["Beli šećer", "Smeđi šećer", "Med", "Stevia"],
        "Ulja i masti": ["Suncokretovo ulje", "Maslinovo ulje extra virgin", "Maslinovo ulje", "Kokosovo ulje"],
        "Konzerve i tegle": ["Paradajz pelati", "Paradajz pire", "Tunjevina u ulju", "Kukuruz", "Grašak", "Masline crne"]
    },
    "Začini i dodaci": {
        "Suvi začini": ["So", "Biber crni", "Paprika slatka", "Paprika ljuta", "Kurkuma", "Kim", "Cimet", "Timijan", "Origano", "Bazilika", "Lovor", "Ruzmarin"],
        "Sosevi i umaci": ["Kečap", "Senf", "Majonez", "Tabasco", "Soja sos", "Pesto"]
    },
    "Pekarski proizvodi": {
        "Hleb": ["Beli hleb", "Crni hleb", "Integralni hleb", "Ciabatta", "Baguette", "Somun"],
        "Peciva": ["Kifla", "Zemička", "Kroasan", "Perec", "Lepinja"],
        "Brašno": ["Pšenično brašno T400", "Pšenično brašno-ostro T400", "Pšenično brašno T500"],
    },
    "Pića": {
        "Bezalkoholna pića": ["Prirodna mineralna voda", "Gazirana mineralna voda", "Sok od narandže", "Coca Cola", "Pepsi", "Sprite"],
        "Alkoholna pića": ["Pivo svetlo", "Pivo tamno", "Belo vino", "Crveno vino", "Roze vino", "Rakija", "Whisky", "Vodka"],
        "Topli napici": ["Espresso kafa", "Filter kafa", "Crni čaj", "Zeleni čaj", "Kakao"]
    },
    "Higijena i čistoća": {
        "Sredstva za čišćenje": ["Deterdžent za sudove", "Dezinficijens", "Sredstvo za podove", "Sredstvo za staklo"],
        "Sanitarna higijena": ["Toalet papir", "Papirni ubrusi", "Salvete", "Sapun za ruke"],
        "Kuhinjska ambalaža": ["Folija za hranu", "Aluminijumska folija", "Kese za zamrzivač", "Kutije za poneti"]
    }
}

# =========================================================
# KORISNICI
# =========================================================
korisnici = {
    "hotel_moskva":     {"naziv": "Hotel Moskva",           "tip": "kupac",     "poeni": 94, "lozinka": "1234"},
    "restoran_znak":    {"naziv": "Restoran Znak Pitanja",  "tip": "kupac",     "poeni": 91, "lozinka": "1234"},
    "kafic_peron":      {"naziv": "Kafić Peron 9",          "tip": "kupac",     "poeni": 87, "lozinka": "1234"},
    "klub_parlament":   {"naziv": "Klub Parlament",         "tip": "kupac",     "poeni": 89, "lozinka": "1234"},
    "hotel_balkan":     {"naziv": "Hotel Balkan",           "tip": "kupac",     "poeni": 92, "lozinka": "1234"},
    "restoran_lorenzo": {"naziv": "Restoran Lorenzo",       "tip": "kupac",     "poeni": 85, "lozinka": "1234"},
    "kafana_sesir":     {"naziv": "Kafana Šešir Moj",       "tip": "kupac",     "poeni": 88, "lozinka": "1234"},
    "meso_prom":        {"naziv": "Meso-Prom d.o.o.",       "tip": "dobavljac", "poeni": 91, "lozinka": "1234"},
    "agro_klanica":     {"naziv": "Agro-Klanica Petrović",  "tip": "dobavljac", "poeni": 87, "lozinka": "1234"},
    "premium_meat":     {"naziv": "Premium Meat Co.",       "tip": "dobavljac", "poeni": 94, "lozinka": "1234"},
    "agro_fresh":       {"naziv": "Agro Fresh d.o.o.",      "tip": "dobavljac", "poeni": 90, "lozinka": "1234"},
    "adriatic_fish":    {"naziv": "Adriatic Fish d.o.o.",   "tip": "dobavljac", "poeni": 92, "lozinka": "1234"},
    "mlekara_zlatibor": {"naziv": "Mlekara Zlatibor",       "tip": "dobavljac", "poeni": 92, "lozinka": "1234"},
    "farma_nikolic":    {"naziv": "Farma Nikolić",          "tip": "oba",       "poeni": 89, "lozinka": "1234"},
    "agro_kombinat":    {"naziv": "Agro Kombinat d.o.o.",   "tip": "oba",       "poeni": 86, "lozinka": "1234"},
}

# =========================================================
# DOBAVLJAČI (artikli i kapaciteti)
# =========================================================
svi_dobavljaci = [
    {"dobavljac": "Meso-Prom d.o.o.",      "artikl": "Ramstek",               "kolicina": 150,  "cena": 1850, "poeni": 91},
    {"dobavljac": "Agro-Klanica Petrović", "artikl": "Ramstek",               "kolicina": 120,  "cena": 1780, "poeni": 87},
    {"dobavljac": "Premium Meat Co.",      "artikl": "Ramstek",               "kolicina": 200,  "cena": 1950, "poeni": 94},
    {"dobavljac": "Meso-Prom d.o.o.",      "artikl": "But",                   "kolicina": 300,  "cena": 1200, "poeni": 91},
    {"dobavljac": "Agro-Klanica Petrović", "artikl": "But",                   "kolicina": 180,  "cena": 1100, "poeni": 87},
    {"dobavljac": "Meso-Prom d.o.o.",      "artikl": "Plećka",                "kolicina": 200,  "cena":  980, "poeni": 91},
    {"dobavljac": "Meso-Prom d.o.o.",      "artikl": "Kare",                  "kolicina": 200,  "cena": 1100, "poeni": 91},
    {"dobavljac": "Farma Nikolić",         "artikl": "Kare",                  "kolicina": 120,  "cena":  980, "poeni": 89},
    {"dobavljac": "Meso-Prom d.o.o.",      "artikl": "Vrat",                  "kolicina": 250,  "cena":  890, "poeni": 91},
    {"dobavljac": "Farma Nikolić",         "artikl": "Vrat",                  "kolicina": 200,  "cena":  850, "poeni": 89},
    {"dobavljac": "Farma Nikolić",         "artikl": "Trbušina",              "kolicina": 120,  "cena":  720, "poeni": 89},
    {"dobavljac": "Premium Meat Co.",      "artikl": "File",                  "kolicina":  80,  "cena": 2200, "poeni": 94},
    {"dobavljac": "Agro-Klanica Petrović", "artikl": "File",                  "kolicina":  60,  "cena": 2100, "poeni": 87},
    {"dobavljac": "Adriatic Fish d.o.o.",  "artikl": "Brancin",               "kolicina": 100,  "cena": 2800, "poeni": 92},
    {"dobavljac": "Adriatic Fish d.o.o.",  "artikl": "Orada",                 "kolicina": 120,  "cena": 2600, "poeni": 92},
    {"dobavljac": "Adriatic Fish d.o.o.",  "artikl": "Losos",                 "kolicina":  80,  "cena": 3200, "poeni": 92},
    {"dobavljac": "Adriatic Fish d.o.o.",  "artikl": "Škampi",                "kolicina":  50,  "cena": 2300, "poeni": 92},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Paradajz",              "kolicina": 500,  "cena":  120, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Paprika",               "kolicina": 400,  "cena":  150, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Krompir",               "kolicina": 2000, "cena":   55, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Šargarepa",             "kolicina":  800, "cena":   65, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Crni luk",              "kolicina": 1000, "cena":   60, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Beli luk",              "kolicina":  300, "cena":  220, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Zelena salata",         "kolicina":  300, "cena":   65, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Spanać",                "kolicina":  250, "cena":  120, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Tikvice",               "kolicina":  400, "cena":  130, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Jabuka",                "kolicina": 1000, "cena":   80, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Banana",                "kolicina":  500, "cena":  120, "poeni": 90},
    {"dobavljac": "Agro Fresh d.o.o.",     "artikl": "Limun",                 "kolicina":  400, "cena":  150, "poeni": 90},
    {"dobavljac": "Mlekara Zlatibor",      "artikl": "Beli sir",              "kolicina":  500, "cena":  680, "poeni": 92},
    {"dobavljac": "Mlekara Zlatibor",      "artikl": "Kačkavalj",             "kolicina":  300, "cena":  980, "poeni": 92},
    {"dobavljac": "Mlekara Zlatibor",      "artikl": "Punomasno mleko",       "kolicina": 1500, "cena":  100, "poeni": 92},
    {"dobavljac": "Mlekara Zlatibor",      "artikl": "Kisela pavlaka",        "kolicina":  400, "cena":  220, "poeni": 92},
    {"dobavljac": "Mlekara Zlatibor",      "artikl": "Jogurt",                "kolicina":  800, "cena":  130, "poeni": 92},
    {"dobavljac": "Agro Kombinat d.o.o.",  "artikl": "Pšenično brašno T400",  "kolicina": 3000, "cena":   62, "poeni": 86},
    {"dobavljac": "Agro Kombinat d.o.o.",  "artikl": "Beli šećer",            "kolicina": 2000, "cena":  118, "poeni": 86},
    {"dobavljac": "Agro Kombinat d.o.o.",  "artikl": "Suncokretovo ulje",     "kolicina": 1000, "cena":  185, "poeni": 86},
    # Farma Nikolić kao dobavljač
    {"dobavljac": "Farma Nikolić",         "artikl": "Pileći file",           "kolicina":  300, "cena":  650, "poeni": 89},
    {"dobavljac": "Farma Nikolić",         "artikl": "Pileći but",            "kolicina":  400, "cena":  430, "poeni": 89},
    {"dobavljac": "Farma Nikolić",         "artikl": "Jaja L (63-73g)",       "kolicina": 3000, "cena":   25, "poeni": 89},
]

# =========================================================
# ZAJEDNIČKI ZAHTJEVI (sinhronizacija kupac ↔ dobavljač)
# Format: zid -> {kupac, kupac_poeni, artikl, kolicina,
#                 cena, status, dobavljac_naziv, item_id_kupca}
# =========================================================
zahtjevi = {}
zahtjev_counter = [0]

def novi_zahtjev_id():
    zahtjev_counter[0] += 1
    return f"Z{zahtjev_counter[0]:04d}"

# =========================================================
# POMOĆNE FUNKCIJE
# =========================================================
def nadji_dobavljace_za_artikl(artikl):
    return [d for d in svi_dobavljaci if d["artikl"] == artikl]

def filtriraj_dobavljace(lista, trazena):
    kval = [d for d in lista if d["kolicina"] >= trazena]
    return sorted(kval, key=lambda x: x["poeni"], reverse=True)

def svi_kupci_sortirani():
    kupci = [v for v in korisnici.values() if v["tip"] in ("kupac", "oba")]
    return sorted(kupci, key=lambda x: x["poeni"], reverse=True)

# =========================================================
# POPUP ARTIKLI
# =========================================================
def otvori_artikl_popup(tree_ref, item_id):
    top = tk.Toplevel()
    top.title("Izbor artikla")
    top.grab_set()

    frame = tk.Frame(top)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame, text="Kategorija").grid(row=0, column=0)
    tk.Label(frame, text="Vrsta").grid(row=0, column=1)
    tk.Label(frame, text="Artikl").grid(row=0, column=2)

    lb_kat   = tk.Listbox(frame, width=20, height=14, exportselection=False)
    lb_vrsta = tk.Listbox(frame, width=20, height=14, exportselection=False)
    lb_art   = tk.Listbox(frame, width=20, height=14, exportselection=False)

    lb_kat.grid(row=1, column=0, padx=4)
    lb_vrsta.grid(row=1, column=1, padx=4)
    lb_art.grid(row=1, column=2, padx=4)

    for k in katalog:
        lb_kat.insert(tk.END, k)

    def on_kat(e):
        sel = lb_kat.curselection()
        if not sel: return
        kat = lb_kat.get(sel[0])
        lb_vrsta.delete(0, tk.END); lb_art.delete(0, tk.END)
        for v in katalog[kat]: lb_vrsta.insert(tk.END, v)

    def on_vrsta(e):
        sk = lb_kat.curselection(); sv = lb_vrsta.curselection()
        if not sk or not sv: return
        kat = lb_kat.get(sk[0]); vrsta = lb_vrsta.get(sv[0])
        lb_art.delete(0, tk.END)
        for a in katalog[kat][vrsta]: lb_art.insert(tk.END, a)

    def on_art(e):
        sel = lb_art.curselection()
        if not sel: return
        artikl = lb_art.get(sel[0])
        vals = list(tree_ref.item(item_id, "values"))
        while len(vals) < 6: vals.append("")
        vals[0] = artikl
        tree_ref.item(item_id, values=tuple(vals))
        top.destroy()

    lb_kat.bind("<ButtonRelease-1>", on_kat)
    lb_vrsta.bind("<ButtonRelease-1>", on_vrsta)
    lb_art.bind("<ButtonRelease-1>", on_art)

# =========================================================
# NARUDŽBENICE — detalj i pregled
# =========================================================
def otvori_detalj_narudžbenice(tree_n_ref, narudžbenice_ref):
    sel = tree_n_ref.selection()
    if not sel: return
    dob    = tree_n_ref.item(sel[0], "values")[0]
    stavke = narudžbenice_ref.get(dob, [])
    top = tk.Toplevel(); top.title(f"Narudžbenica — {dob}")
    top.grab_set(); top.geometry("620x350")
    tk.Label(top, text=f"Narudžbenica za: {dob}",
             font=("Arial", 12, "bold")).pack(pady=5)
    cols = ("Artikl", "Količina", "Cena (RSD)", "Iznos (RSD)")
    t = ttk.Treeview(top, columns=cols, show="headings")
    for col in cols: t.heading(col, text=col); t.column(col, width=148)
    t.pack(fill="both", expand=True, padx=10, pady=5)
    ukupno = 0
    for s in stavke:
        iznos = s["kolicina"]*s["cena"]; ukupno += iznos
        t.insert("", "end", values=(s["artikl"], s["kolicina"],
                                    f"{s['cena']:,}", f"{iznos:,}"))
    tk.Label(top, text=f"UKUPNO: {ukupno:,.0f} RSD",
             font=("Arial", 11, "bold"), fg="darkgreen").pack(pady=5)
    tk.Button(top, text="Zatvori", command=top.destroy).pack(pady=3)

def otvori_sve_narudžbenice(narudžbenice_ref):
    if not narudžbenice_ref:
        messagebox.showinfo("Info", "Nema narudžbenica."); return
    top = tk.Toplevel(); top.title("Sve narudžbenice")
    top.grab_set(); top.geometry("720x500")
    tk.Label(top, text="Sve narudžbenice",
             font=("Arial", 13, "bold")).pack(pady=5)
    nb = ttk.Notebook(top); nb.pack(fill="both", expand=True, padx=10, pady=5)
    ukupno_sve = 0
    for dob, stavke in narudžbenice_ref.items():
        frame = tk.Frame(nb); nb.add(frame, text=dob[:20])
        cols = ("Artikl", "Količina", "Cena (RSD)", "Iznos (RSD)")
        t = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols: t.heading(col, text=col); t.column(col, width=170)
        t.pack(fill="both", expand=True)
        ukupno = 0
        for s in stavke:
            iznos = s["kolicina"]*s["cena"]; ukupno += iznos; ukupno_sve += iznos
            t.insert("", "end", values=(s["artikl"], s["kolicina"],
                                        f"{s['cena']:,}", f"{iznos:,}"))
        tk.Label(frame, text=f"Ukupno: {ukupno:,.0f} RSD",
                 font=("Arial", 10, "bold"), fg="darkgreen").pack(pady=3)
    tk.Label(top, text=f"UKUPNO SVE: {ukupno_sve:,.0f} RSD",
             font=("Arial", 12, "bold"), fg="darkblue").pack(pady=5)
    tk.Button(top, text="Zatvori", command=top.destroy).pack(pady=3)

# =========================================================
# GLAVNI PROZOR — tip "oba"
# =========================================================
def pokreni(korisnik_kupac, korisnik_dobavljac):
    """
    korisnik_kupac    — dict iz korisnici (tip kupac ili oba)
    korisnik_dobavljac — dict iz korisnici (tip dobavljac ili oba)
    Može biti isti entitet (tip "oba") ili dva različita.
    """
    root = tk.Tk()
    root.title(f"KAIZA — {korisnik_kupac['naziv']}  |  {korisnik_dobavljac['naziv']}")
    root.geometry("1100x860")

    narudžbenice_kupac = {}

    # Mapa: item_id u tree_k → zahtjev_id
    # Potrebno da bismo ažurirali STATUS kolonu kod kupca
    item_zahtjev_map = {}

    # =========================================================
    # LEVI PANEL — TABLA KUPCA
    # =========================================================
    frame_levo = tk.LabelFrame(root,
        text=f"▲  UPRAVLJAČKA TABLA — KUPAC: {korisnik_kupac['naziv']}",
        font=("Arial", 10, "bold"), fg="#1565C0", pady=4)
    frame_levo.pack(side="left", fill="both", expand=True, padx=6, pady=6)

    tk.Label(frame_levo, text="Stavke narudžbine",
             font=("Arial", 9, "bold")).pack(anchor="w", padx=5)

    # Kolone kupca — dodana STATUS kolona
    cols_k = ("Artikl", "Količina", "Dobavljač", "Cena (RSD)", "Raspoloživo", "Status")
    tree_k = ttk.Treeview(frame_levo, columns=cols_k, show="headings", height=8)
    sirine_k = [130, 75, 150, 90, 90, 80]
    for col, w in zip(cols_k, sirine_k):
        tree_k.heading(col, text=col)
        tree_k.column(col, width=w)
    tree_k.pack(fill="both", expand=True, padx=5)

    # Boje za STATUS
    tree_k.tag_configure("da",    foreground="green", font=("Arial", 9, "bold"))
    tree_k.tag_configure("ne",    foreground="red",   font=("Arial", 9, "bold"))
    tree_k.tag_configure("ceka",  foreground="orange")

    btn_k = tk.Frame(frame_levo); btn_k.pack(pady=3)
    tk.Button(btn_k, text="+ Novi artikl",
              command=lambda: tree_k.insert("", "end",
                  values=("Klikni za artikl", "", "", "", "", "")),
              bg="#4CAF50", fg="white", width=14).pack(side="left", padx=4)
    tk.Button(btn_k, text="📋 Narudžbenice",
              command=lambda: otvori_sve_narudžbenice(narudžbenice_kupac),
              bg="#2196F3", fg="white", width=16).pack(side="left", padx=4)

    tk.Label(frame_levo, text="Narudžbenice po dobavljačima",
             font=("Arial", 9, "bold")).pack(anchor="w", padx=5)

    cols_n = ("Dobavljač", "Artikala", "Ukupno (RSD)")
    tree_n = ttk.Treeview(frame_levo, columns=cols_n, show="headings", height=5)
    for col, w in zip(cols_n, [200, 80, 180]):
        tree_n.heading(col, text=col); tree_n.column(col, width=w)
    tree_n.pack(fill="both", expand=True, padx=5)
    tree_n.bind("<Double-1>",
                lambda e: otvori_detalj_narudžbenice(tree_n, narudžbenice_kupac))

    # =========================================================
    # DESNI PANEL — TABLA DOBAVLJAČA
    # =========================================================
    frame_desno = tk.LabelFrame(root,
        text=f"▼  UPRAVLJAČKA TABLA — DOBAVLJAČ: {korisnik_dobavljac['naziv']}",
        font=("Arial", 10, "bold"), fg="#2E7D32", pady=4)
    frame_desno.pack(side="right", fill="both", expand=True, padx=6, pady=6)

    tk.Label(frame_desno, text="Pristigli zahtjevi",
             font=("Arial", 9, "bold")).pack(anchor="w", padx=5)

    cols_z = ("ID", "Kupac", "Poeni", "Artikl", "Količina", "Cena (RSD)", "Status")
    tree_z = ttk.Treeview(frame_desno, columns=cols_z, show="headings", height=8)
    for col, w in zip(cols_z, [55, 160, 50, 130, 70, 95, 85]):
        tree_z.heading(col, text=col); tree_z.column(col, width=w)
    tree_z.pack(fill="both", expand=True, padx=5)

    tree_z.tag_configure("prihvaceno", foreground="green", font=("Arial", 9, "bold"))
    tree_z.tag_configure("odbijeno",   foreground="red",   font=("Arial", 9, "bold"))
    tree_z.tag_configure("ceka",       foreground="orange")

    btn_d = tk.Frame(frame_desno); btn_d.pack(pady=3)
    tk.Button(btn_d, text="🔄  Osveži zahtjeve",
              command=lambda: osveži_tablu_dobavljaca(),
              bg="#FF9800", fg="white", width=18).pack(side="left", padx=4)
    tk.Button(btn_d, text="✅  Odgovori",
              command=lambda: otvori_matching(),
              bg="#1565C0", fg="white", width=14).pack(side="left", padx=4)

    tk.Label(frame_desno, text="Potvrđene narudžbine",
             font=("Arial", 9, "bold")).pack(anchor="w", padx=5)

    cols_p = ("ID", "Kupac", "Artikl", "Količina", "Cena (RSD)", "Iznos (RSD)")
    tree_p = ttk.Treeview(frame_desno, columns=cols_p, show="headings", height=5)
    for col, w in zip(cols_p, [55, 160, 130, 70, 95, 110]):
        tree_p.heading(col, text=col); tree_p.column(col, width=w)
    tree_p.pack(fill="both", expand=True, padx=5)

    # =========================================================
    # FUNKCIJE AŽURIRANJA
    # =========================================================
    def azuriraj_narudžbenice():
        for r in tree_n.get_children(): tree_n.delete(r)
        for dob, stavke in narudžbenice_kupac.items():
            ukupno = sum(s["kolicina"]*s["cena"] for s in stavke)
            tree_n.insert("", "end", values=(dob, len(stavke), f"{ukupno:,.0f} RSD"))

    def azuriraj_status_kupca(item_id, status):
        """Ažurira STATUS kolonu u tabeli kupca za dati red."""
        vals = list(tree_k.item(item_id, "values"))
        while len(vals) < 6: vals.append("")
        if status == "prihvaćeno":
            vals[5] = "DA"
            tree_k.item(item_id, values=tuple(vals), tags=("da",))
        elif status == "odbijeno":
            vals[5] = "NE"
            tree_k.item(item_id, values=tuple(vals), tags=("ne",))
        else:
            vals[5] = "čeka..."
            tree_k.item(item_id, values=tuple(vals), tags=("ceka",))

    def osveži_tablu_dobavljaca():
        naziv_dob = korisnik_dobavljac["naziv"]

        # Pristigli zahtjevi
        for r in tree_z.get_children(): tree_z.delete(r)
        for zid, z in zahtjevi.items():
            if z["dobavljac_naziv"] == naziv_dob:
                tag = "ceka"
                if z["status"] == "prihvaćeno": tag = "prihvaceno"
                elif z["status"] == "odbijeno":  tag = "odbijeno"
                tree_z.insert("", "end", iid=zid, tags=(tag,), values=(
                    zid, z["kupac"], z["kupac_poeni"],
                    z["artikl"], z["kolicina"],
                    f"{z['cena']:,}", z["status"]))

        # Potvrđene narudžbine
        for r in tree_p.get_children(): tree_p.delete(r)
        for zid, z in zahtjevi.items():
            if z["dobavljac_naziv"] == naziv_dob and z["status"] == "prihvaćeno":
                iznos = z["kolicina"] * z["cena"]
                tree_p.insert("", "end", values=(
                    zid, z["kupac"], z["artikl"],
                    z["kolicina"], f"{z['cena']:,}", f"{iznos:,}"))

    # =========================================================
    # POPUP DOBAVLJAČI (kupac bira dobavljača)
    # =========================================================
    def otvori_dobavljaci_popup(item_id, artikl, kolicina):
        lista = nadji_dobavljace_za_artikl(artikl)
        if not lista:
            messagebox.showinfo("Info", "Nema dobavljača za ovaj artikl")
            return
        kval = filtriraj_dobavljace(lista, kolicina)

        top = tk.Toplevel()
        top.title("Izbor dobavljača")
        top.grab_set()

        tk.Label(top, text=f"Dobavljači za: {artikl} — {kolicina} kom/kg",
                 font=("Arial", 11, "bold")).pack(pady=5)

        if not kval:
            tk.Label(top, text="Nema dobavljača sa dovoljnom količinom",
                     fg="red").pack(pady=10)
            tk.Button(top, text="Zatvori", command=top.destroy).pack()
            return

        cols_d = ("Dobavljač", "Raspoloživo", "Cena (RSD)", "Poeni")
        tree_d = ttk.Treeview(top, columns=cols_d, show="headings")
        for col, w in zip(cols_d, [200, 110, 110, 80]):
            tree_d.heading(col, text=col); tree_d.column(col, width=w)
        tree_d.pack(padx=10, pady=5)

        for d in kval:
            tree_d.insert("", "end", values=(
                d["dobavljac"], d["kolicina"], d["cena"], d["poeni"]))
        tree_d.selection_set(tree_d.get_children()[0])

        def prihvati():
            sel = tree_d.selection()
            if not sel:
                messagebox.showwarning("Upozorenje", "Izaberite dobavljača")
                return
            vals_d = tree_d.item(sel[0], "values")
            izabran_dob   = vals_d[0]
            izabrana_cena = int(vals_d[2])

            # Umanji kapacitet dobavljača
            nova_kol = None
            for d in svi_dobavljaci:
                if d["dobavljac"] == izabran_dob and d["artikl"] == artikl:
                    d["kolicina"] -= kolicina
                    nova_kol = d["kolicina"]
                    break
            if nova_kol is None:
                messagebox.showerror("Greška", "Dobavljač nije pronađen")
                return

            # Ažuriraj red kupca — STATUS = "čeka..."
            tree_k.item(item_id, values=(
                artikl, kolicina, izabran_dob,
                izabrana_cena, nova_kol, "čeka..."),
                tags=("ceka",))

            # Dodaj u narudžbenicu
            if izabran_dob not in narudžbenice_kupac:
                narudžbenice_kupac[izabran_dob] = []
            postoji = False
            for s in narudžbenice_kupac[izabran_dob]:
                if s["artikl"] == artikl:
                    s["kolicina"] += kolicina; postoji = True; break
            if not postoji:
                narudžbenice_kupac[izabran_dob].append(
                    {"artikl": artikl, "kolicina": kolicina, "cena": izabrana_cena})
            azuriraj_narudžbenice()

            # Kreiraj zahtjev
            zid = novi_zahtjev_id()
            zahtjevi[zid] = {
                "zahtjev_id":      zid,
                "kupac":           korisnik_kupac["naziv"],
                "kupac_poeni":     korisnik_kupac["poeni"],
                "artikl":          artikl,
                "kolicina":        kolicina,
                "cena":            izabrana_cena,
                "status":          "čeka",
                "dobavljac_naziv": izabran_dob,
                "item_id_kupca":   item_id   # ← veza sa redom u tabeli kupca
            }
            item_zahtjev_map[item_id] = zid

            # Automatski osveži tablu dobavljača
            osveži_tablu_dobavljaca()
            top.destroy()

        fb = tk.Frame(top); fb.pack(pady=5)
        tk.Button(fb, text="Prihvati", command=prihvati,
                  bg="green", fg="white").pack(side="left", padx=5)
        tk.Button(fb, text="Odbij", command=top.destroy,
                  bg="red", fg="white").pack(side="left", padx=5)

    # =========================================================
    # MATCHING KUPACA (dobavljač odgovara)
    # =========================================================
    def otvori_matching():
        sel = tree_z.selection()
        if not sel:
            messagebox.showwarning("Upozorenje", "Izaberite zahtjev."); return
        zid = sel[0]
        z = zahtjevi.get(zid)
        if not z: return
        if z["status"] != "čeka":
            messagebox.showinfo("Info", f"Zahtjev {zid} je već: {z['status']}."); return

        kupci_lista = svi_kupci_sortirani()

        top = tk.Toplevel()
        top.title(f"Matching kupaca — {z['artikl']}")
        top.grab_set()

        tk.Label(top,
                 text=f"Zahtjev: {zid}  |  Artikl: {z['artikl']}  |  Količina: {z['kolicina']}",
                 font=("Arial", 11, "bold")).pack(pady=5)
        tk.Label(top, text="Kupci rangirani po poenima (opadajuće):",
                 font=("Arial", 9)).pack(pady=2)

        cols_k = ("Kupac", "Poeni")
        tree_kupci = ttk.Treeview(top, columns=cols_k, show="headings", height=10)
        for col, w in zip(cols_k, [300, 100]):
            tree_kupci.heading(col, text=col); tree_kupci.column(col, width=w)
        tree_kupci.pack(padx=10, pady=5)

        # Originalni kupac na vrhu sa oznakom ★
        tree_kupci.insert("", "end", iid="orig",
            values=(f"★  {z['kupac']}", z["kupac_poeni"]))
        tree_kupci.selection_set("orig")

        for k in kupci_lista:
            if k["naziv"] != z["kupac"]:
                tree_kupci.insert("", "end",
                    values=(k["naziv"], k["poeni"]))

        def potvrdi():
            sk = tree_kupci.selection()
            if not sk:
                messagebox.showwarning("Upozorenje", "Izaberite kupca."); return
            vals_k = tree_kupci.item(sk[0], "values")
            izabran_kupac = vals_k[0].replace("★  ", "")

            # Ažuriraj zahtjev
            zahtjevi[zid]["status"] = "prihvaćeno"
            zahtjevi[zid]["kupac"]  = izabran_kupac

            # ← Ažuriraj STATUS na tabli kupca
            item_id_kupca = z.get("item_id_kupca")
            if item_id_kupca:
                azuriraj_status_kupca(item_id_kupca, "prihvaćeno")

            osveži_tablu_dobavljaca()
            top.destroy()
            messagebox.showinfo("Potvrđeno",
                f"Narudžbina {zid} potvrđena!\n"
                f"Kupac: {izabran_kupac}\n"
                f"Artikl: {z['artikl']} — {z['kolicina']} kom/kg")

        def odbij_z():
            zahtjevi[zid]["status"] = "odbijeno"

            # ← Ažuriraj STATUS na tabli kupca
            item_id_kupca = z.get("item_id_kupca")
            if item_id_kupca:
                azuriraj_status_kupca(item_id_kupca, "odbijeno")

            osveži_tablu_dobavljaca()
            top.destroy()
            messagebox.showinfo("Odbijeno", f"Zahtjev {zid} odbijen.")

        fb = tk.Frame(top); fb.pack(pady=8)
        tk.Button(fb, text="✅  Potvrdi",       command=potvrdi,
                  bg="green", fg="white", width=14).pack(side="left", padx=6)
        tk.Button(fb, text="❌  Odbij zahtjev", command=odbij_z,
                  bg="red",   fg="white", width=14).pack(side="left", padx=6)
        tk.Button(fb, text="Zatvori", command=top.destroy,
                  width=10).pack(side="left", padx=6)

    # =========================================================
    # DOUBLE CLICK — TABLA KUPCA
    # =========================================================
    def on_double_click(event):
        item = tree_k.identify_row(event.y)
        col  = tree_k.identify_column(event.x)
        if not item: return

        if col == "#1":
            otvori_artikl_popup(tree_k, item)
        elif col == "#2":
            x, y, w, h = tree_k.bbox(item, col)
            entry = tk.Entry(frame_levo)
            entry.place(x=x, y=y, width=w, height=h)
            def save():
                try: kolicina = int(entry.get())
                except: entry.destroy(); return
                vals = list(tree_k.item(item, "values"))
                while len(vals) < 6: vals.append("")
                vals[1] = kolicina
                tree_k.item(item, values=tuple(vals))
                entry.destroy()
                artikl = vals[0]
                if artikl and artikl != "Klikni za artikl":
                    otvori_dobavljaci_popup(item, artikl, kolicina)
            entry.bind("<Return>", lambda e: save())
            entry.focus()

    tree_k.bind("<Double-1>", on_double_click)
    root.mainloop()

# =========================================================
# START — Hotel Moskva (kupac) + Meso-Prom d.o.o. (dobavljač)
# Za demo: dva različita entiteta u jednom prozoru
# =========================================================
if __name__ == "__main__":
    kupac     = korisnici["hotel_moskva"]
    dobavljac = korisnici["meso_prom"]
    pokreni(kupac, dobavljac)

# --- WEB LOGIKA ---
st.set_page_config(layout="wide")
st.title("LOBO B2B Platforma - Prototip")

# Prikaz podataka kao tabela
st.subheader("Trenutni katalog dobavljača")
df_dobavljaci = pd.DataFrame(svi_dobavljaci)
st.dataframe(df_dobavljaci, use_container_width=True)

# Jednostavan filter za investitore
st.subheader("Pretraga artikala")
artikl_input = st.selectbox("Izaberite artikl:", df_dobavljaci['artikl'].unique())
kolicina_input = st.number_input("Količina:", min_value=1, value=10)

if st.button("Pronađi dobavljače"):
    rezultat = [d for d in svi_dobavljaci if d["artikl"] == artikl_input and d["kolicina"] >= kolicina_input]
    if rezultat:
        st.success(f"Pronađeno {len(rezultat)} dobavljača!")
        st.table(pd.DataFrame(rezultat))
    else:
        st.error("Nema dostupnih dobavljača za ovu količinu.")
