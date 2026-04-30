import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

if "df_dobavljaci" not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "But", "kolicina": 200, "cena": 1400},
    ])

if "narudzbenica" not in st.session_state:
    st.session_state.narudzbenica = []

df_kupci = pd.DataFrame({"Naziv_Firme": ["Hotel Moskva", "Restoran Dunav"]})
df_artikli = pd.DataFrame({"Artikl": ["Ramstek", "But", "Paradajz"]})

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Kupac")

    kupac = st.selectbox("Firma:", [""] + df_kupci["Naziv_Firme"].tolist(), key="kupac_sel")
    artikl = st.selectbox("Artikl:", [""] + df_artikli["Artikl"].tolist(), key="artikl_sel")

    if kupac and artikl:
        mask = st.session_state.df_dobavljaci["artikl"] == artikl
        dostupni = st.session_state.df_dobavljaci.loc[mask].copy()

        if dostupni.empty:
            st.info("Nema dobavljača za izabrani artikl.")
        else:
            dostupni = dostupni.reset_index().rename(columns={"index": "_orig_idx"})
            dostupni["Unos_Količine"] = 0

            with st.form(key="narudzbina_form", clear_on_submit=False):
                edited = st.data_editor(
                    dostupni,
                    hide_index=True,
                    use_container_width=True,
                    num_rows="fixed",
                    disabled=["_orig_idx", "dobavljac", "artikl", "kolicina", "cena"],
                    column_config={
                        "_orig_idx": st.column_config.NumberColumn("ID", disabled=True),
                        "dobavljac": st.column_config.TextColumn("Dobavljač", disabled=True),
                        "artikl": st.column_config.TextColumn("Artikl", disabled=True),
                        "kolicina": st.column_config.NumberColumn("Raspoloživo", disabled=True),
                        "cena": st.column_config.NumberColumn("Cena", disabled=True),
                        "Unos_Količine": st.column_config.NumberColumn("Unos_Količine", min_value=0, step=1),
                    },
                    key="editor_form"
                )

                submitted = st.form_submit_button("Potvrdi narudžbinu")

            if submitted:
                for _, row in edited.iterrows():
                    qty = int(row["Unos_Količine"])
                    if qty <= 0:
                        continue

                    orig_idx = int(row["_orig_idx"])
                    available = int(st.session_state.df_dobavljaci.at[orig_idx, "kolicina"])

                    if qty > available:
                        st.error(f"Nedovoljno zaliha kod {row['dobavljac']}.")
                        continue

                    st.session_state.df_dobavljaci.at[orig_idx, "kolicina"] = available - qty

                    st.session_state.narudzbenica.append({
                        "id": f"{int(time.time())}_{orig_idx}",
                        "kupac": kupac,
                        "artikl": row["artikl"],
                        "dobavljac": row["dobavljac"],
                        "kolicina_tražena": qty,
                        "status": "Čeka",
                    })

                st.success("Narudžbina je sačuvana.")
                st.rerun()

    st.subheader("Narudžbenica")
    if st.session_state.narudzbenica:
        st.dataframe(pd.DataFrame(st.session_state.narudzbenica), hide_index=True, use_container_width=True)
    else:
        st.info("Nema narudžbina.")

with tab_dobavljac:
    st.header("Dobavljač")

    if st.session_state.narudzbenica:
        for i, n in enumerate(st.session_state.narudzbenica):
            c1, c2, c3 = st.columns([5, 1, 1])
            c1.write(f"{n['kupac']} | {n['artikl']} | {n['dobavljac']} | {n['kolicina_tražena']} | {n['status']}")
            if c2.button("✅", key=f"ok_{n['id']}"):
                st.session_state.narudzbenica[i]["status"] = "Prihvaćeno"
                st.rerun()
            if c3.button("❌", key=f"no_{n['id']}"):
                st.session_state.narudzbenica[i]["status"] = "Odbijeno"
                st.rerun()
    else:
        st.info("Nema zahteva.")
