import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# 1. BAZE (Artikli, Kupci, Dobavljači)
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700, "poeni": 90},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "But", "kolicina": 200, "cena": 1400, "poeni": 85}
    ])

df_artikli = pd.DataFrame({"Artikl": ["Ramstek", "But", "Paradajz"]})
df_kupci = pd.DataFrame({"Naziv_Firme": ["Hotel Moskva", "Restoran Dunav"]})

if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

# 2. INTERFEJS
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    odabrani_kupac = st.selectbox("Firma:", [""] + list(df_kupci['Naziv_Firme'].unique()))
    artikl_za_izbor = st.selectbox("Artikl:", [""] + list(df_artikli['Artikl'].unique()))
    
    if odabrani_kupac and artikl_za_izbor:
        dostupni = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
        if not dostupni.empty:
            st.dataframe(dostupni, hide_index=True)
            odabrani_dob = st.selectbox("Dobavljač:", dostupni['dobavljac'].unique())
            tražena_kol = st.number_input("Količina (kg):", min_value=1)
            
            if st.button("Naruči"):
                mask = (st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)
                idx = st.session_state.df_dobavljaci[mask].index[0]
                if tražena_kol <= st.session_state.df_dobavljaci.at[idx, 'kolicina']:
                    stavka = st.session_state.df_dobavljaci.loc[idx].to_dict()
                    stavka.update({'id': f"{int(time.time())}", 'kupac': odabrani_kupac, 'kolicina_tražena': tražena_kol, 'status': 'Čeka'})
                    st.session_state.narudžbenica.append(stavka)
                    st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                    st.success("Dodato!")
                    st.rerun()
                else: st.error("Nedovoljno na stanju!")

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_k = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_k[['artikl', 'dobavljac', 'kolicina_tražena', 'status']], hide_index=True)

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        for i, stavka in enumerate(st.session_state.narudžbenica):
            cols = st.columns([3, 1, 1])
            cols[0].write(f"{stavka['kupac']} | {stavka['artikl']} ({stavka['kolicina_tražena']}kg) | {stavka['status']}")
            if cols[1].button("✅", key=f"p_{stavka['id']}_{i}"):
                st.session_state.narudžbenica[i]['status'] = 'Prihvaćeno'
                st.rerun()
            if cols[2].button("❌", key=f"o_{stavka['id']}_{i}"):
                st.session_state.narudžbenica[i]['status'] = 'Odbijeno'
                st.rerun()
    else: st.info("Nema zahteva.")
