import streamlit as st
import pandas as pd

# Podaci
svi_dobavljaci = [
    {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
    {"dobavljac": "Agro-Klanica Petrović", "artikl": "Ramstek", "kolicina": 120, "cena": 1780, "poeni": 87},
    {"dobavljac": "Premium Meat Co.", "artikl": "Ramstek", "kolicina": 200, "cena": 1950, "poeni": 94},
    {"dobavljac": "Meso-Prom d.o.o.", "artikl": "But", "kolicina": 300, "cena": 1200, "poeni": 91},
    {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Paradajz", "kolicina": 500, "cena": 120, "poeni": 90},
    {"dobavljac": "Mlekara Zlatibor", "artikl": "Beli sir", "kolicina": 500, "cena": 680, "poeni": 92},
    {"dobavljac": "Farma Nikolić", "artikl": "Pileći file", "kolicina": 300, "cena": 650, "poeni": 89}
]

st.set_page_config(layout="wide")
st.title("LOBO B2B Platforma - Prototip")

st.subheader("Trenutni katalog dobavljača")
df_dobavljaci = pd.DataFrame(svi_dobavljaci)
st.dataframe(df_dobavljaci, use_container_width=True)

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
