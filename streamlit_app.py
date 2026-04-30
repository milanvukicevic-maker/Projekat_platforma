import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# --- INICIJALIZACIJA BAZE ---
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "But", "kolicina": 200, "cena": 1400}
    ])
if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

# --- CALLBACK FUNKCIJA (OVO REŠAVA PROBLEM) ---
def procesuiraj():
    # Uzimamo podatke direktno iz stanja editora pre osvežavanja
    editor_data = st.session_state['moj_editor']
    za_obradu = editor_data[editor_data['Unos_Količine'] > 0]
    
    for idx, row in za_obradu.iterrows():
        if row['Unos_Količine'] <= st.session_state.df_dobavljaci.at[idx, 'kolicina']:
            st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= row['Unos_Količine']
            st.session_state.narudžbenica.append({
                'id': time.time(),
                'kupac': st.session_state.temp_kupac,
                'artikl': row['artikl'],
                'kolicina': row['Unos_Količine'],
                'status': 'Čeka'
            })

# --- INTERFEJS ---
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.session_state.temp_kupac = st.selectbox("Firma:", ["", "Hotel Moskva", "Restoran Dunav"])
    artikl_za_izbor = st.selectbox("Artikl:", ["", "Ramstek", "But", "Paradajz"])
    
    if st.session_state.temp_kupac and artikl_za_izbor:
        mask = st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor
        dostupni = st.session_state.df_dobavljaci[mask].copy()
        dostupni['Unos_Količine'] = 0
        
        # Ključ 'moj_editor' se koristi u callback-u
        st.data_editor(dostupni, key='moj_editor', hide_index=False)
        
        # Dugme poziva funkciju PRE nego što se stranica resetuje
        st.button("Potvrdi narudžbinu", on_click=procesuiraj)

with tab_dobavljac:
    st.subheader("Pregled zahteva")
    for i, n in enumerate(st.session_state.narudžbenica):
        cols = st.columns([3, 1, 1])
        cols[0].write(f"{n['kupac']} | {n['artikl']} | {n['kolicina']}kg | {n['status']}")
        if cols[1].button("✅", key=f"p_{i}"):
            st.session_state.narudžbenica[i]['status'] = 'Prihvaćeno'
            st.rerun()
