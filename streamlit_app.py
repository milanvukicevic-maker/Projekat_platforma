import streamlit as st
import pandas as pd

# 1. PODACI
katalog = {
    "Meso": {"Juneće meso": ["Ramstek", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Rozbif", "File", "Koljenica"],
             "Svinjsko meso": ["Kare", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Trbušina", "Koljenica", "File"]},
    "Povrće": {"Plodovito povrće": ["Paradajz", "Paprika", "Tikvice", "Patlidžan", "Krastavac", "Brokoli", "Karfiol"]}
}

data_artikli = []
for grupa, kategorije in katalog.items():
    for kat, artikli in kategorije.items():
        for art in artikli:
            data_artikli.append({"Grupa": grupa, "Kategorija": kat, "Artikl": art})
df_artikli = pd.DataFrame(data_artikli)

if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 100, "cena": 120, "poeni": 90}
    ])

# 2. INICIJALIZACIJA
if 'narudžbenica' not in st.session_state: st.session_state.narudžbenica = []

# 3. KONFIGURACIJA
st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC (Hotel Moskva)", "🚛 DOBAVLJAČ (Meso-Prom)"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    artikl_za_izbor = st.selectbox("Izaberite artikl:", df_artikli['Artikl'].unique())
    
    dostupni = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
    
    if not dostupni.empty:
        st.dataframe(dostupni, hide_index=True)
        odabrani_dob = st.selectbox("Izaberite dobavljača:", dostupni['dobavljac'].unique())
        tražena_kol = st.number_input("Količina:", min_value=1)
        
        if st.button("Dodaj u narudžbinu"):
            red = st.session_state.df_dobavljaci[(st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & 
                                                 (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)]
            if tražena_kol <= red.iloc[0]['kolicina']:
                stavka = red.iloc[0].to_dict()
                stavka.update({'kolicina_tražena': tražena_kol, 'status': 'Čeka'})
                st.session_state.narudžbenica.append(stavka)
                # Smanjenje zaliha
                idx = red.index[0]
                st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                st.success("Dodato!")
                st.rerun()
            else: st.error("Nema dovoljno na stanju!")
    else: st.warning("Nema dobavljača.")

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
