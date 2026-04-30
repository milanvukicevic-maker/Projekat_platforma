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
        lista = nadji_dobavljace_za_artikl(artikl_za_izbor)
        rezultati = filtriraj_dobavljace(lista, kolicina)
        
        if rezultati:
            df_rez = pd.DataFrame(rezultati)
            st.table(df_rez)
        else:
            st.warning("Nema dobavljača sa traženom količinom.")

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    st.write("Ovde će biti pregled pristiglih zahteva.")
    if st.button("Osveži zahtjeve"):
        st.write("Učitavam...")
