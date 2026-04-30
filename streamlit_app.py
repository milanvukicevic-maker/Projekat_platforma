import streamlit as st
import pandas as pd

# 1. DINAMIČKO UČITAVANJE (Nema više hardkodiranih podataka)
@st.cache_data
def ucitaj_podatke():
    df_art = pd.read_csv("artikli.csv")
    df_dob = pd.read_csv("dobavljaci.csv")
    return df_art, df_dob

df_artikli, df_dobavljaci_baza = ucitaj_podatke()

# Inicijalizacija baze u session_state radi promene stanja
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = df_dobavljaci_baza

if 'narudžbenica' not in st.session_state: st.session_state.narudžbenica = []

# 2. KONFIGURACIJA
st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    artikl_za_izbor = st.selectbox("Izaberite artikl:", df_artikli['Artikl'].unique())
    
    dostupni = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
    
    if not dostupni.empty:
        st.dataframe(dostupni, hide_index=True)
        odabrani_dob = st.selectbox("Izaberite dobavljača:", dostupni['dobavljac'].unique())
        tražena_kol = st.number_input("Količina:", min_value=1)
        
        if st.button("Potvrdi narudžbinu"):
            red = st.session_state.df_dobavljaci[(st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & 
                                                 (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)]
            if tražena_kol <= red.iloc[0]['kolicina']:
                stavka = red.iloc[0].to_dict()
                stavka.update({'kolicina_tražena': tražena_kol, 'status': 'Čeka'})
                st.session_state.narudžbenica.append(stavka)
                # Ažuriranje zaliha u session_state
                idx = red.index[0]
                st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                st.success("Naručeno!")
                st.rerun()
            else: st.error("Nedovoljno na stanju!")
    else: st.warning("Nema dobavljača za ovaj artikl.")

# ... (ostatak koda za tab_dobavljac ostaje isti kao u prethodnoj verziji)

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_korpa = pd.DataFrame(st.session_state.narudžbenica)
        df_korpa['Iznos'] = df_korpa['kolicina_tražena'] * df_korpa['cena']
        st.dataframe(df_korpa[['artikl', 'dobavljac', 'kolicina_tražena', 'cena', 'Iznos', 'status']], hide_index=True)
    
with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        df_z = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_z[['artikl', 'kolicina_tražena', 'cena', 'status']], hide_index=True)
        idx = st.number_input("Redni broj zahteva:", min_value=0, max_value=len(st.session_state.narudžbenica)-1)
        if st.button("✅ Prihvati"):
            st.session_state.narudžbenica[idx]['status'] = 'Prihvaćeno'
            st.rerun()
    else: st.info("Nema zahteva.")

if 'poruka' in st.session_state:
    st.toast(st.session_state.poruka)
    del st.session_state.poruka
