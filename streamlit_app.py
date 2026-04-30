import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# 1. INICIJALIZACIJA PODATAKA
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700, "poeni": 90},
        {"dobavljac": "Firma X", "artikl": "But", "kolicina": 100, "cena": 1960, "poeni": 80}
    ])

if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

# 2. TABOVI
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    
    artikli = st.session_state.df_dobavljaci['artikl'].unique()
    artikl_za_izbor = st.selectbox("Izaberite artikl:", [""] + list(artikli))
    
    if artikl_za_izbor:
        dostupni = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
        
        if not dostupni.empty:
            st.dataframe(dostupni, hide_index=True)
            odabrani_dob = st.selectbox("Izaberite dobavljača:", dostupni['dobavljac'].unique())
            tražena_kol = st.number_input("Količina (kg):", min_value=1)
            
            if st.button("Naruči"):
                mask = (st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & \
                       (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)
                idx = st.session_state.df_dobavljaci[mask].index[0]
                
                if tražena_kol <= st.session_state.df_dobavljaci.at[idx, 'kolicina']:
                    # STVARAMO STAVKU SA JEDINSTVENIM ID-JEM
                    stavka = st.session_state.df_dobavljaci.loc[idx].to_dict()
                    stavka.update({
                        'id': f"{int(time.time())}_{odabrani_dob}",
                        'kolicina_tražena': tražena_kol, 
                        'status': 'Čeka'
                    })
                    st.session_state.narudžbenica.append(stavka)
                    st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                    st.success(f"Naručeno {tražena_kol}kg!")
                    st.rerun()
                else:
                    st.error("Nedovoljno na stanju!")

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_korpa = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_korpa[['artikl', 'dobavljac', 'kolicina_tražena', 'status']], hide_index=True)

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        # Prikaz stavki sa nezavisnim dugmadima
        for i, stavka in enumerate(st.session_state.narudžbenica):
            cols = st.columns([2, 1, 1, 1])
            cols[0].write(f"{stavka['artikl']} ({stavka['kolicina_tražena']}kg) od {stavka['dobavljac']}")
            cols[1].write(f"Status: {stavka['status']}")
            
            # KORISTIMO ID ZA KLJUČ DA DUGME BUDE NEZAVISNO
            if cols[2].button("✅", key=f"p_{stavka['id']}"):
                st.session_state.narudžbenica[i]['status'] = 'Prihvaćeno'
                st.rerun()
            if cols[3].button("❌", key=f"o_{stavka['id']}"):
                st.session_state.narudžbenica[i]['status'] = 'Odbijeno'
                st.rerun()
    else:
        st.info("Nema pristiglih zahteva.")
