import streamlit as st
import pandas as pd

# 1. Definisanje podataka (df_artikli, df_dobavljaci)
# ... [vaš kod za DataFrame-ove] ...

# 2. INICIJALIZACIJA SESSION_STATE (Ovo je kritično)
if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

if 'trazeni_rezultati' not in st.session_state:
    st.session_state.trazeni_rezultati = []

# 3. KONFIGURACIJA STRANICE
st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# Sada slobodno možete koristiti st.session_state.narudžbenica

# ... ostatak vašeg koda gde koristite df_artikli i df_dobavljaci

# Tabovi za uloge
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC (Hotel Moskva)", "🚛 DOBAVLJAČ (Meso-Prom)"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    # Dinamički spisak iz vašeg kataloga
    svi_artikli = [a for sub in [cat.values() for cat in katalog.values()] for sublist in sub for a in sublist]
    artikl_za_izbor = st.selectbox("Izaberite artikl:", df_artikli['Artikl'].unique())
    kolicina = st.number_input("Količina:", min_value=1, value=10)
    
    if st.button("Pronađi dobavljače"):
        st.session_state.trazeni_rezultati = filtriraj_dobavljace(nadji_dobavljace_za_artikl(artikl_za_izbor), kolicina)
        st.session_state.artikl_trenutni = artikl_za_izbor
        st.session_state.kolicina_trenutna = kolicina

    # Prikaz rezultata ako postoje u memoriji
    if 'trazeni_rezultati' in st.session_state and st.session_state.trazeni_rezultati:
        df_rez = pd.DataFrame(st.session_state.trazeni_rezultati)
        st.table(df_rez)
        
        izabrani_dob = st.selectbox("Izaberite dobavljača za potvrdu:", [d['dobavljac'] for d in st.session_state.trazeni_rezultati])
        
        if st.button("Dodaj u narudžbinu"):
            stavka = next(d for d in st.session_state.trazeni_rezultati if d['dobavljac'] == izabrani_dob).copy()
            stavka['artikl'] = st.session_state.artikl_trenutni
            stavka['kolicina_tražena'] = st.session_state.kolicina_trenutna
            st.session_state.narudžbenica.append(stavka)
            st.success(f"Dodato: {stavka['artikl']} od {izabrani_dob}")
    elif 'trazeni_rezultati' in st.session_state:
        st.warning("Nema dobavljača.")
            
    st.divider()
    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_korpa = pd.DataFrame(st.session_state.narudžbenica)
        
        # Izračunaj iznos
        df_korpa['Iznos'] = df_korpa['kolicina_tražena'] * df_korpa['cena']
        
        # Ovde biramo samo kolone koje želimo da vidimo, bez indeksa
        prikaz = df_korpa[['artikl', 'dobavljac', 'kolicina_tražena', 'cena', 'Iznos']]
        
        # Prikaz bez indeksa (index=False)
        st.dataframe(prikaz, use_container_width=True, hide_index=True)
        
        ukupno = df_korpa['Iznos'].sum()
        st.metric("UKUPNO ZA PLAĆANJE (RSD)", f"{ukupno:,.2f}")
    else:
        st.write("Korpa je prazna.")
    st.divider()
    st.subheader("Statusi vaših zahteva")
    if st.session_state.narudžbenica:
        # Osiguravamo da status postoji
        for s in st.session_state.narudžbenica:
            if 'status' not in s: s['status'] = 'Čeka'
        
        df_status = pd.DataFrame(st.session_state.narudžbenica)
        
        # Prikazujemo tabelu samo jednom
        st.dataframe(
            df_status[['artikl', 'status']],
            column_config={
                "status": st.column_config.TextColumn(
                    "Status",
                    help="Status vaše narudžbine",
                    width="small",
                )
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("Nema aktivnih zahteva.")
        
with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")
    
    if st.session_state.narudžbenica:
        # SIGURNOSNI KOD: Dodaje 'status' ako nedostaje
        for s in st.session_state.narudžbenica:
            if 'status' not in s:
                s['status'] = 'Čeka'
        
        df_zahtevi = pd.DataFrame(st.session_state.narudžbenica)
        df_zahtevi['Iznos'] = df_zahtevi['kolicina_tražena'] * df_zahtevi['cena']
        
        # Prikaz tabele
        st.dataframe(df_zahtevi[['artikl', 'kolicina_tražena', 'cena', 'Iznos', 'status']], use_container_width=True, hide_index=True)
                
        # Izbor zahteva za promenu statusa
        izabrani_index = st.number_input("Redni broj zahteva (0-indexed):", min_value=0, max_value=len(st.session_state.narudžbenica)-1)
        
        col1, col2 = st.columns(2)
        
        if col1.button("✅ Prihvati"):
            st.session_state.narudžbenica[izabrani_index]['status'] = 'Prihvaćeno'
            # Postavljamo poruku u session_state da je prikažemo nakon rerun-a
            st.session_state.poruka = "Narudžbina uspešno prihvaćena!"
            st.rerun()
            
        if col2.button("❌ Odbij"):
            st.session_state.narudžbenica[izabrani_index]['status'] = 'Odbijeno'
            st.session_state.poruka = "Narudžbina je odbijena."
            st.rerun()

    # Prikaži poruku ako postoji u session_state
    if 'poruka' in st.session_state:
        st.toast(st.session_state.poruka, icon="ℹ️")
        del st.session_state.poruka # Obriši nakon prikaza        
    else:
        st.info("Nema pristiglih zahteva.")
