import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")

# Inicijalizacija baze
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "But", "kolicina": 200, "cena": 1400}
    ])
if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    odabrani_kupac = st.selectbox("Firma:", [""] + ["Hotel Moskva", "Restoran Dunav"])
    artikl_za_izbor = st.selectbox("Artikl:", [""] + ["Ramstek", "But", "Paradajz"])
    
    if odabrani_kupac and artikl_za_izbor:
        mask = st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor
        # Uzimamo indeks iz originalne baze kako bismo kasnije lako ažurirali
        dostupni = st.session_state.df_dobavljaci[mask].copy()
        dostupni['Unos_Količine'] = 0
        
        # Ključ osigurava da se editor resetuje pri svakoj promeni izbora artikla
        editor_key = f"editor_{artikl_za_izbor}_{odabrani_kupac}"
        editor_data = st.data_editor(dostupni, key=editor_key, hide_index=False)
        
        if st.button("Potvrdi narudžbinu"):
            za_obradu = editor_data[editor_data['Unos_Količine'] > 0]
            for idx, row in za_obradu.iterrows():
                # Ažuriramo stanje u glavnoj bazi koristeći originalni indeks
                st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= row['Unos_Količine']
                # Dodajemo u narudžbenicu
                st.session_state.narudžbenica.append({
                    'id': time.time(),
                    'kupac': odabrani_kupac,
                    'artikl': row['artikl'],
                    'kolicina': row['Unos_Količine'],
                    'status': 'Čeka'
                })
            st.rerun()

with tab_dobavljac:
    for i, n in enumerate(st.session_state.narudžbenica):
        cols = st.columns([3, 1, 1])
        cols[0].write(f"{n['kupac']} traži {n['kolicina']}x {n['artikl']} - Status: {n['status']}")
        if cols[1].button("Prihvati", key=f"p_{n['id']}"):
            st.session_state.narudžbenica[i]['status'] = 'Prihvaćeno'
            st.rerun()
