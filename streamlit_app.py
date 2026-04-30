import streamlit as st
import pandas as pd
import os

# 1. KONFIGURACIJA I UČITAVANJE
st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

@st.cache_data
def ucitaj_baze():
    # Učitava fajlove ako postoje
    return pd.read_csv("artikli.csv"), pd.read_csv("kupci.csv"), pd.read_csv("dobavljaci.csv")

# Učitavanje podataka
df_artikli, df_kupci, df_dobavljaci_original = ucitaj_baze()

# Inicijalizacija zaliha u session_state da bi promene trajale tokom sesije
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = df_dobavljaci_original

if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

# 2. TABOVI
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    
    # Izbor kupca
    odabrani_kupac = st.selectbox("Izaberite vašu firmu:", df_kupci['Naziv_Firme'].unique())
    
    # Izbor artikla
    artikl_za_izbor = st.selectbox("Izaberite artikl:", df_artikli['Artikl'].unique())
    
    # Pretraga dobavljača iz "žive" session_state baze
    dostupni = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
    
    if not dostupni.empty:
        st.dataframe(dostupni, hide_index=True)
        odabrani_dob = st.selectbox("Izaberite dobavljača:", dostupni['dobavljac'].unique())
        tražena_kol = st.number_input("Količina (kg):", min_value=1)
        
        if st.button("Potvrdi i smanji zalihe"):
            red = st.session_state.df_dobavljaci[(st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & 
                                                 (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)]
            
            if tražena_kol <= red.iloc[0]['kolicina']:
                # Dodavanje u narudžbinu
                stavka = red.iloc[0].to_dict()
                stavka.update({'kupac': odabrani_kupac, 'kolicina_tražena': tražena_kol, 'status': 'Čeka'})
                st.session_state.narudžbenica.append(stavka)
                
                # Smanjenje zaliha u "živoj" bazi
                idx = red.index[0]
                st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                
                st.success(f"Naručeno {tražena_kol}kg od {odabrani_dob}.")
                st.rerun()
            else:
                st.error("Nedovoljno na stanju!")
    else:
        st.warning("Nema dostupnih dobavljača za ovaj artikl.")

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_korpa = pd.DataFrame(st.session_state.narudžbenica)
        df_korpa['Iznos'] = df_korpa['kolicina_tražena'] * df_korpa['cena']
        st.dataframe(df_korpa[['artikl', 'dobavljac', 'kolicina_tražena', 'cena', 'Iznos', 'status']], hide_index=True)
    
with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        df_z = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_z[['artikl', 'kupac', 'kolicina_tražena', 'status']], hide_index=True)
        
        idx = st.number_input("Redni broj zahteva (0-indexed):", min_value=0, max_value=len(st.session_state.narudžbenica)-1)
        if st.button("✅ Prihvati"):
            st.session_state.narudžbenica[idx]['status'] = 'Prihvaćeno'
            st.rerun()
    else:
        st.info("Nema pristiglih zahteva.")
