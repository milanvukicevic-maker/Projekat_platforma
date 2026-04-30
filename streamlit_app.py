import streamlit as st
import pandas as pd

# Inicijalna baza dobavljača
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Paradajz", "kolicina": 500, "cena": 120, "poeni": 90}
    ])

# Inicijalizacija narudžbenice
if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

st.set_page_config(page_title="KAIZA B2B", layout="wide")

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    artikl_za_izbor = st.selectbox("Izaberite artikl:", ["Ramstek", "Paradajz"]) # Dodajte ostatak iz kataloga
    
    # Pretraga u session_state bazi
    dobavljaci_za_artikl = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
    
    if not dobavljaci_za_artikl.empty:
        # Ovde je bila greška, promenljiva mora da se zove isto:
        st.dataframe(dobavljaci_za_artikl, hide_index=True)
        
        odabrani_dob = st.selectbox("Izaberite dobavljača:", dobavljaci_za_artikl['dobavljac'].unique())
        # ... ostatak koda ...
        tražena_kol = st.number_input("Količina:", min_value=1)
        
        if st.button("Potvrdi narudžbinu"):
            red = st.session_state.df_dobavljaci[(st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & 
                                                 (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)]
            
            if tražena_kol <= red.iloc[0]['kolicina']:
                # 1. Dodaj u narudžbenicu
                stavka = red.iloc[0].to_dict()
                stavka['kolicina_tražena'] = tražena_kol
                stavka['status'] = 'Čeka'
                st.session_state.narudžbenica.append(stavka)
                
                # 2. Smanji zalihe u session_state bazi
                idx = red.index[0]
                st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                
                st.success("Naručeno!")
                st.rerun()
            else:
                st.error("Nedovoljno na stanju!")

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        df_z = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_z[['artikl', 'kolicina_tražena', 'cena', 'status']], hide_index=True)
        izabrani_index = st.number_input("Redni broj zahteva:", min_value=0, max_value=len(st.session_state.narudžbenica)-1)
        col1, col2 = st.columns(2)
        if col1.button("✅ Prihvati"):
            st.session_state.narudžbenica[izabrani_index]['status'] = 'Prihvaćeno'
            st.session_state.poruka = "Prihvaćeno!"
            st.rerun()
        if col2.button("❌ Odbij"):
            st.session_state.narudžbenica[izabrani_index]['status'] = 'Odbijeno'
            st.rerun()
    else: st.info("Nema pristiglih zahteva.")

if 'poruka' in st.session_state:
    st.toast(st.session_state.poruka)
    del st.session_state.poruka
