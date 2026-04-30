import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# 1. BAZE
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
        # Filtriramo bazu
        mask = st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor
        dostupni = st.session_state.df_dobavljaci[mask].copy()
        
        if not dostupni.empty:
            dostupni['Unos_Količine'] = 0
            editor = st.data_editor(dostupni, hide_index=False, column_config={"Unos_Količine": st.column_config.NumberColumn(min_value=0)})
            
            if st.button("Potvrdi i naruči"):
                # Pronalazimo promene direktno kroz editor
                for idx, row in editor.iterrows():
                    kol = row['Unos_Količine']
                    if kol > 0:
                        # Pronađi originalni red u session_state bazi
                        orig_idx = idx 
                        if kol <= st.session_state.df_dobavljaci.at[orig_idx, 'kolicina']:
                            stavka = st.session_state.df_dobavljaci.loc[orig_idx].to_dict()
                            stavka.update({'id': f"{time.time()}_{orig_idx}", 'kupac': odabrani_kupac, 'kolicina_tražena': kol, 'status': 'Čeka'})
                            
                            st.session_state.narudžbenica.append(stavka)
                            st.session_state.df_dobavljaci.at[orig_idx, 'kolicina'] -= kol
                        else:
                            st.error(f"Nedovoljno zaliha kod {row['dobavljac']}!")
                st.rerun()

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        for i, stavka in enumerate(st.session_state.narudžbenica):
            cols = st.columns([4, 1, 1])
            cols[0].write(f"{stavka['kupac']} | {stavka['artikl']} ({stavka['kolicina_tražena']}kg) | Status: {stavka['status']}")
            if cols[1].button("✅", key=f"p_{stavka['id']}"):
                st.session_state.narudžbenica[i]['status'] = 'Prihvaćeno'
                st.rerun()
            if cols[2].button("❌", key=f"o_{stavka['id']}"):
                st.session_state.narudžbenica[i]['status'] = 'Odbijeno'
                st.rerun()
    else: st.info("Nema zahteva.")
