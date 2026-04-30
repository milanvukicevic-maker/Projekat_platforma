import streamlit as st
import pandas as pd

# Podaci (preuzeti iz vašeg originalnog koda)
katalog = {
    "Meso": {"Juneće meso": ["Ramstek", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Rozbif", "File", "Koljenica"],
             "Svinjsko meso": ["Kare", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Trbušina", "Koljenica", "File"]},
    "Povrće": {"Plodovito povrće": ["Paradajz", "Paprika", "Tikvice", "Patlidžan", "Krastavac", "Brokoli", "Karfiol"]}
}

svi_dobavljaci = [
    {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
    {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Paradajz", "kolicina": 500, "cena": 120, "poeni": 90}
]
# Funkcije za logiku (prenesene iz vašeg koda)
def nadji_dobavljace_za_artikl(artikl):
    return [d for d in svi_dobavljaci if d["artikl"] == artikl]

def filtriraj_dobavljace(lista, trazena):
    kval = [d for d in lista if d["kolicina"] >= trazena]
    return sorted(kval, key=lambda x: x["poeni"], reverse=True)

# Inicijalizacija memorije aplikacije
if 'zahtjevi' not in st.session_state:
    st.session_state.zahtjevi = {}

st.set_page_config(page_title="KAIZA B2B", layout="wide")
if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []
st.title("KAIZA B2B Platforma")

# Tabovi za uloge
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC (Hotel Moskva)", "🚛 DOBAVLJAČ (Meso-Prom)"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    # Dinamički spisak iz vašeg kataloga
    svi_artikli = [a for sub in [cat.values() for cat in katalog.values()] for sublist in sub for a in sublist]
    artikl_za_izbor = st.selectbox("Izaberite artikl:", svi_artikli)
    kolicina = st.number_input("Količina:", min_value=1, value=10)
    
    if st.button("Pronađi dobavljače"):
        st.session_state.trazeni_rezultati = filtriraj_dobavljace(nadji_dobavljace_za_artikl(artikl_za_izbor), kolicina)
        st.session_state.artikl_trenutni = artikl_za_izbor
        st.session_state.kolicina_trenutna = kolicina

    # Prikaz rezultata ako postoje u memoriji
    if 'trazeni_rezultati' in st.session_state and st.session_state.trazeni_rezultati:
        df_rez = pd.DataFrame(st.session_state.trazeni_rezultati)
        st.table(df_rez)
        
        izabrani_dob = st.selectbox("Izaberite dobavljača za potvrdu:", [d['dobavljac'] for d in st.session_state.trazeni_rezultati])
        
        if st.button("Dodaj u narudžbinu"):
            stavka = next(d for d in st.session_state.trazeni_rezultati if d['dobavljac'] == izabrani_dob).copy()
            stavka['artikl'] = st.session_state.artikl_trenutni
            stavka['kolicina_tražena'] = st.session_state.kolicina_trenutna
            st.session_state.narudžbenica.append(stavka)
            st.success(f"Dodato: {stavka['artikl']} od {izabrani_dob}")
    elif 'trazeni_rezultati' in st.session_state:
        st.warning("Nema dobavljača.")
            
    st.divider()
    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_korpa = pd.DataFrame(st.session_state.narudžbenica)
        
        # Izračunaj iznos
        df_korpa['Iznos'] = df_korpa['kolicina_tražena'] * df_korpa['cena']
        
        # Ovde biramo samo kolone koje želimo da vidimo, bez indeksa
        prikaz = df_korpa[['artikl', 'dobavljac', 'kolicina_tražena', 'cena', 'Iznos']]
        
        # Prikaz bez indeksa (index=False)
        st.dataframe(prikaz, use_container_width=True, hide_index=True)
        
        ukupno = df_korpa['Iznos'].sum()
        st.metric("UKUPNO ZA PLAĆANJE (RSD)", f"{ukupno:,.2f}")
    else:
        st.write("Korpa je prazna.")
        
with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    
    if st.session_state.narudžbenica:
        # SIGURNOSNI KOD: Dodaje 'status' ako nedostaje
        for s in st.session_state.narudžbenica:
            if 'status' not in s:
                s['status'] = 'Čeka'
        
        df_zahtevi = pd.DataFrame(st.session_state.narudžbenica)
        df_zahtevi['Iznos'] = df_zahtevi['kolicina_tražena'] * df_zahtevi['cena']
        
        # Prikaz tabele
        st.dataframe(df_zahtevi[['artikl', 'kolicina_tražena', 'cena', 'Iznos', 'status']], use_container_width=True, hide_index=True)
        # ... (ostatak koda)
        
        # Izbor zahteva za promenu statusa
        izabrani_index = st.number_input("Redni broj zahteva (0-indexed):", min_value=0, max_value=len(st.session_state.narudžbenica)-1)
        
        col1, col2 = st.columns(2)
        if col1.button("✅ Prihvati"):
            st.session_state.narudžbenica[izabrani_index]['status'] = 'Prihvaćeno'
            st.rerun()
        if col2.button("❌ Odbij"):
            st.session_state.narudžbenica[izabrani_index]['status'] = 'Odbijeno'
            st.rerun()
    else:
        st.info("Nema pristiglih zahteva.")
