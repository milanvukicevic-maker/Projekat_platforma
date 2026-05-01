import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

# 1. BAZE (Artikli, Kupci, Dobavljači)
if 'df_dobavljaci' not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700, "poeni": 90},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "But", "kolicina": 200, "cena": 1400, "poeni": 85}
    ])

df_artikli = pd.DataFrame({"Artikl": ["Ramstek", "But", "Paradajz"]})
df_kupci = pd.DataFrame({"Naziv_Firme": ["Hotel Moskva", "Restoran Dunav"]})

if 'narudžbenica' not in st.session_state:
    st.session_state.narudžbenica = []

# 2. INTERFEJS
tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")

    odabrani_kupac = st.selectbox(
        "Firma:",
        [""] + list(df_kupci["Naziv_Firme"].unique()),
        key="kupac_select"
    )

    artikl_za_izbor = st.selectbox(
        "Artikl:",
        [""] + list(df_artikli["Artikl"].unique()),
        key="artikl_select"
    )

    if odabrani_kupac and artikl_za_izbor:
        dostupni = st.session_state.df_dobavljaci[
            st.session_state.df_dobavljaci["artikl"] == artikl_za_izbor
        ].copy()

        if not dostupni.empty:
            dostupni = dostupni.reset_index().rename(columns={"index": "_orig_idx"})

            prikaz = dostupni[[
                "dobavljac",
                "artikl",
                "kolicina",
                "cena",
                "_orig_idx"
            ]].copy()

            prikaz.columns = [
                "Dobavljač",
                "Artikl",
                "Raspoloživa količina",
                "Cena",
                "_orig_idx"
            ]

            st.dataframe(
                prikaz[["Dobavljač", "Artikl", "Raspoloživa količina", "Cena"]],
                hide_index=True,
                use_container_width=True
            )

            odabrani_dob = st.selectbox(
                "Dobavljač:",
                dostupni["dobavljac"].unique(),
                key="dobavljac_select"
            )

            tražena_kol = st.number_input(
                "Količina (kg):",
                min_value=1,
                step=1,
                key="kolicina_select"
            )

            if st.button("Naruči", key="naruči_btn"):
                mask = (
                    (st.session_state.df_dobavljaci["dobavljac"] == odabrani_dob) &
                    (st.session_state.df_dobavljaci["artikl"] == artikl_za_izbor)
                )

                if not mask.any():
                    st.error("Odabrani dobavljač nije pronađen.")
                else:
                    idx = st.session_state.df_dobavljaci[mask].index[0]
                    dostupno = st.session_state.df_dobavljaci.at[idx, "kolicina"]

                    if tražena_kol <= dostupno:
                        stavka = st.session_state.df_dobavljaci.loc[idx].to_dict()
                        stavka.update({
                            "id": f"{int(time.time())}_{idx}",
                            "kupac": odabrani_kupac,
                            "kolicina_tražena": tražena_kol,
                            "status": "Čeka",
                            "_orig_idx": idx
                        })

                        st.session_state.narudžbenica.append(stavka)
                        st.success("Narudžbina dodata.")
                        st.rerun()
                    else:
                        st.error("Nedovoljno na stanju!")
        
    st.subheader("Vaša narudžbenica")
    if st.session_state.narudžbenica:
        df_k = pd.DataFrame(st.session_state.narudžbenica)
        prikaz_kupac = df_k[["kupac", "artikl", "kolicina_tražena", "status"]].copy()
        prikaz_kupac.columns = ["Kupac", "Artikl", "Količina", "Status"]
        st.dataframe(prikaz_kupac, hide_index=True, use_container_width=True)

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")

    if st.session_state.narudzbenica:
        df_narudzbenica = pd.DataFrame(st.session_state.narudzbenica)

        prikaz = df_narudzbenica[[
            "kupac",
            "artikl",
            "kolicina_tražena",
            "kolicina",
            "cena",
            "status"
        ]].copy()

        prikaz.columns = [
            "Kupac",
            "Artikl",
            "Količina",
            "Raspoloživa količina",
            "Cena",
            "Status"
        ]

        st.dataframe(prikaz, hide_index=True, use_container_width=True)

        st.subheader("Akcije po narudžbini")
        for i, stavka in enumerate(st.session_state.narudzbenica):
            c1, c2, c3 = st.columns([5, 1, 1])
            c1.write(
                f"{stavka['kupac']} | {stavka['artikl']} | "
                f"{stavka['kolicina_tražena']} | {stavka['kolicina']} | "
                f"{stavka['cena']} | {stavka['status']}"
            )

            if c2.button("✅", key=f"ok_{stavka['id']}"):
                if st.session_state.narudzbenica[i]["status"] != "Prihvaćeno":
                    st.session_state.narudzbenica[i]["status"] = "Prihvaćeno"

                    orig_idx = st.session_state.narudzbenica[i]["_orig_idx"]
                    st.session_state.df_dobavljaci.at[orig_idx, "kolicina"] -= st.session_state.narudzbenica[i]["kolicina_tražena"]

                st.rerun()

            if c3.button("❌", key=f"no_{stavka['id']}"):
                st.session_state.narudzbenica[i]["status"] = "Odbijeno"
                st.rerun()
    else:
        st.info("Nema zahteva.")
