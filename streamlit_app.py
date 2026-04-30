import streamlit as st
import pandas as pd

# 1. PODACI (Katalozi)
katalog = {
    "Meso": {"Juneće meso": ["Ramstek", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Rozbif", "File", "Koljenica"],
             "Svinjsko meso": ["Kare", "But", "Plećka", "Rebra", "Vrat", "Lungić", "Trbušina", "Koljenica", "File"]},
    "Povrće": {"Plodovito povrće": ["Paradajz", "Paprika", "Tikvice", "Patlidžan", "Krastavac", "Brokoli", "Karfiol"]}
}

df_artikli = pd.DataFrame([{"Grupa": g, "Kategorija": k, "Artikl": a} 
                           for g, kat in katalog.items() for k, arts in kat.items() for a in arts])

df_dobavljaci = pd.DataFrame([
    {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
    {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Paradajz", "kolicina": 500, "cena": 120, "poeni": 90}
])

# 2. FUNKCIJE
def nadji_dobavljace(artikl):
    return df_dobavljaci[df_dobavljaci['artikl'] == artikl]

def filtriraj_dobavljace(df, trazena):
    return df[df['kolicina'] >= trazena].sort_values(by='poeni', ascending=False)

# 3. INICIJALIZACIJA
if 'narudžbenica' not in st.session_state: st.session_state.narudžbenica = []

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# 4. INTERFEJS
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC (Hotel Moskva)", "🚛 DOBAVLJAČ (Meso-Prom)"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")
    artikl_za_izbor = st.selectbox("Izaberite artikl:", df_artikli['Artikl'].unique())
    kolicina = st.number_input("Količina:", min_value=1, value=10)
    
    if st.button("Pronađi dobavljače"):
        st.session_state.trazeni_rezultati = filtriraj_dobavljace(nadji_dobavljace(artikl_za_izbor), kolicina).to_dict('records')
        st.session_state.artikl_trenutni = artikl_za_izbor
        st.session_state.kolicina_trenutna = kolicina

    if 'trazeni_rezultati' in st.session_state and st.session_state.trazeni_rezultati:
        df_rez = pd.DataFrame(st.session_state.trazeni_rezultati)
        st.write("Dostupni dobavljači za vašu količinu:")
        
        # Prikazujemo sve dostupne dobavljače kao listu gde kupac može dodavati redom
        for idx, row in df_rez.iterrows():
            with st.expander(f"{row['dobavljac']} — Cena: {row['cena']} RSD (Na stanju: {row['kolicina']})"):
                kolicina_za_ovog = st.number_input(f"Koliko uzimate od {row['dobavljac']}?", 
                                                 min_value=0, max_value=int(row['kolicina']), 
                                                 key=f"kolicina_{idx}")
                if st.button(f"Dodaj u korpu od {row['dobavljac']}", key=f"btn_{idx}"):
                    if kolicina_za_ovog > 0:
                        stavka = row.to_dict()
                        stavka['artikl'] = st.session_state.artikl_trenutni
                        stavka['kolicina_tražena'] = kolicina_za_ovog
                        stavka['status'] = 'Čeka'
                        st.session_state.narudžbenica.append(stavka)
                        st.success(f"Dodato {kolicina_za_ovog}kg od {row['dobavljac']}")

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_k = pd.DataFrame(st.session_state.narudžbenica)
        df_k['Iznos'] = df_k['kolicina_tražena'] * df_k['cena']
        st.dataframe(df_k[['artikl', 'dobavljac', 'kolicina_tražena', 'cena', 'Iznos', 'status']], hide_index=True)
        st.metric("UKUPNO (RSD)", f"{df_k['Iznos'].sum():,.2f}")
    else: st.write("Korpa je prazna.")

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
