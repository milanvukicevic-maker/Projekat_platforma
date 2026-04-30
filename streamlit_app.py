import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

@st.cache_data
def ucitaj_baze():
    artikli_data = "Grupa,Kategorija,Artikl\nMeso,Juneće meso,Ramstek\nMeso,Juneće meso,But\nPovrće,Plodovito povrće,Paradajz"
    kupci_data = "Kupac_ID,Naziv_Firme,Lokacija,Kontakt\nK001,Hotel Moskva,Beograd,office@moskva.rs\nK002,Restoran Dunav,Novi Sad,info@dunav.rs"
    dobavljaci_data = "dobavljac,artikl,kolicina,cena,poeni\nMeso-Prom d.o.o.,Ramstek,150,1850,91\nAgro Fresh d.o.o.,Paradajz,500,120,90\nMeso-Prom d.o.o.,But,200,1400,85"
    return pd.read_csv(io.StringIO(artikli_data)), pd.read_csv(io.StringIO(kupci_data)), pd.read_csv(io.StringIO(dobavljaci_data))

df_artikli, df_kupci, df_dobavljaci_original = ucitaj_baze()

if 'df_dobavljaci' not in st.session_state: st.session_state.df_dobavljaci = df_dobavljaci_original
if 'narudžbenica' not in st.session_state: st.session_state.narudžbenica = []

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    
    # 1. Kupac: Dodajemo praznu opciju na početak
    odabrani_kupac = st.selectbox("Izaberite vašu firmu:", [""] + list(df_kupci['Naziv_Firme'].unique()))
    
    if odabrani_kupac:
        artikl_za_izbor = st.selectbox("Izaberite artikl:", [""] + list(df_artikli['Artikl'].unique()))
        
        if artikl_za_izbor:
            # Filtriramo dobavljače za izabrani artikl
            dostupni = st.session_state.df_dobavljaci[st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor]
            
            if not dostupni.empty:
                # Prikazujemo tabelu sa trenutnim stanjem
                st.dataframe(dostupni, hide_index=True)
                
                # Omogućavamo izbor dobavljača iz filtrirane liste
                odabrani_dob = st.selectbox("Dobavljač:", dostupni['dobavljac'].unique())
                tražena_kol = st.number_input("Količina (kg):", min_value=1)
                
                if st.button("Potvrdi i smanji zalihe"):
                    # Pronalazimo indeks u originalnom DataFrame-u (session_state)
                    # Koristimo .loc za sigurno filtriranje
                    mask = (st.session_state.df_dobavljaci['dobavljac'] == odabrani_dob) & \
                           (st.session_state.df_dobavljaci['artikl'] == artikl_za_izbor)
                    
                    if mask.any():
                        idx = st.session_state.df_dobavljaci[mask].index[0]
                        raspolozivo = st.session_state.df_dobavljaci.at[idx, 'kolicina']
                        
                        if tražena_kol <= raspolozivo:
                            # 1. Priprema stavke
                            stavka = st.session_state.df_dobavljaci.loc[idx].to_dict()
                            stavka.update({'kupac': odabrani_kupac, 'kolicina_tražena': tražena_kol, 'status': 'Čeka'})
                            
                            # 2. Ažuriranje narudžbenice
                            st.session_state.narudžbenica.append(stavka)
                            
                            # 3. Smanjenje zaliha
                            st.session_state.df_dobavljaci.at[idx, 'kolicina'] -= tražena_kol
                            
                            st.success(f"Uspešno naručeno {tražena_kol}kg od {odabrani_dob}.")
                            st.rerun()
                        else:
                            st.error(f"Nedovoljno na stanju! Raspoloživo: {raspolozivo}kg.")
            else:
                st.warning("Trenutno nema dobavljača za ovaj artikl.")
        else:
            st.info("Molimo izaberite artikl iz kataloga.")

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_korpa = pd.DataFrame(st.session_state.narudžbenica)
        df_korpa['Iznos'] = df_korpa['kolicina_tražena'] * df_korpa['cena']
        st.dataframe(df_korpa[['artikl', 'dobavljac', 'kolicina_tražena', 'cena', 'Iznos', 'status']], hide_index=True)

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    if st.session_state.narudžbenica:
        df_z = pd.DataFrame(st.session_state.narudžbenica)
        st.dataframe(df_z[['artikl', 'kupac', 'kolicina_tražena', 'cena', 'status']], hide_index=True)
        idx = st.number_input("Redni broj zahteva:", min_value=0, max_value=len(st.session_state.narudžbenica)-1)
        if st.button("✅ Prihvati"):
            st.session_state.narudžbenica[idx]['status'] = 'Prihvaćeno'
            st.rerun()
        if st.button("❌ Odbij"):
            st.session_state.narudžbenica[idx]['status'] = 'Odbijeno'
            st.rerun()
    else:
        st.info("Nema zahteva.")
