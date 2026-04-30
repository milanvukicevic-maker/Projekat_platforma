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

# Inicijalizacija memorije aplikacije
if 'zahtjevi' not in st.session_state:
    st.session_state.zahtjevi = {}

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# Tabovi za uloge
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC (Hotel Moskva)", "🚛 DOBAVLJAČ (Meso-Prom)"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    artikl_za_izbor = st.selectbox("Izaberite artikl:", ["Ramstek", "Paradajz"])
    kolicina = st.number_input("Količina:", min_value=1, value=10)
    
    if st.button("Pronađi dobavljače"):
        st.write(f"Tražim dobavljače za: {artikl_za_izbor}")
        # Ovde ćemo kasnije dodati funkciju filtriranja

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    st.write("Ovde će biti pregled pristiglih zahteva.")
    if st.button("Osveži zahtjeve"):
        st.write("Učitavam...")
