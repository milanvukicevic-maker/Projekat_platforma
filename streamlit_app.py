import streamlit as st
import pandas as pd

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# 1. INICIJALIZACIJA BAZE
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700, "poeni": 90},
        {"dobavljac": "Firma X", "artikl": "Ramstek", "kolicina": 100, "cena": 1600, "poeni": 80}
    ])

if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

# 2. TABOVI
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    
    # Izbor artikla
    artikli = st.session_state.df_dobavljaci['artikl'].unique()
    artikl_za_izbor = st.selectbox("Izaberite artikl:", [""] + list(artikli))
    
    if artikl_za_izbor:
        # Prikaz svih dobavljača za taj artikl
        dostupni = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
        
        if not dostupni.empty:
            st.dataframe(dostupni, hide_index=True)
            
            # Izbor dobavljača direktno iz filtrirane liste
            odabrani_dob = st.selectbox("Izaberite dobavljača:", dostupni['dobavljac'].unique())
            tražena_kol = st.number_input("Količina (kg):", min_value=1)
            
            if st.button("Naruči"):
                # ISPRAVNA PRETRAGA: Tražimo red baš po tom imenu dobavljača i artiklu
                mask = (st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & \
                       (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)
                
                if mask.any():
                    idx = st.session_state.df_dobavljaci[mask].index[0]
                    
                    if tražena_kol <= st.session_state.df_dobavljaci.at[idx, 'kolicina']:
                        # Kreiramo stavku
                        stavka = st.session_state.df_dobavljaci.loc[idx].to_dict()
                        stavka.update({'kolicina_tražena': tražena_kol, 'status': 'Čeka'})
                        
                        st.session_state.narudžbenica.append(stavka)
                        st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                        
                        st.success(f"Naručeno {tražena_kol}kg od {odabrani_dob}!")
                        st.rerun()
                    else:
                        st.error("Nedovoljno na stanju!")
        else:
            st.warning("Nema dobavljača.")

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_korpa = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_korpa[['artikl', 'dobavljac', 'kolicina_tražena', 'status']], hide_index=True)

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        df_z = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_z[['artikl', 'kolicina_tražena', 'status']], hide_index=True)
        
        idx = st.number_input("Redni broj zahteva:", min_value=0, max_value=len(st.session_state.narudžbenica)-1)
        if st.button("✅ Prihvati"):
            st.session_state.narudžbenica[idx]['status'] = 'Prihvaćeno'
            st.rerun()
        if st.button("❌ Odbij"):
            st.session_state.narudžbenica[idx]['status'] = 'Odbijeno'
            st.rerun()
    else:
        st.info("Nema pristiglih zahteva.")
