import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

if "df_dobavljaci" not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Ramstek", "kolicina": 500, "cena": 1700, "poeni": 90},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "But", "kolicina": 200, "cena": 1400, "poeni": 85},
        {"dobavljac": "Green Market", "artikl": "Paradajz", "kolicina": 300, "cena": 220, "poeni": 88},
    ])

if "narudzbenica" not in st.session_state:
    st.session_state.narudzbenica = []

df_artikli = pd.DataFrame({"Artikl": ["Ramstek", "But", "Paradajz"]})
df_kupci = pd.DataFrame({"Naziv_Firme": ["Hotel Moskva", "Restoran Dunav"]})

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Upravljačka tabla — KUPAC")

    if "kupac_sel" not in st.session_state:
        st.session_state.kupac_sel = ""
    if "artikl_sel" not in st.session_state:
        st.session_state.artikl_sel = ""
    if "dobavljac_sel" not in st.session_state:
        st.session_state.dobavljac_sel = ""

    st.session_state.kupac_sel = st.selectbox(
        "Firma:",
        [""] + df_kupci["Naziv_Firme"].tolist(),
        key="kupac_widget"
    )

    st.session_state.artikl_sel = st.selectbox(
        "Artikl:",
        [""] + df_artikli["Artikl"].tolist(),
        key="artikl_widget"
    )

    if st.session_state.kupac_sel and st.session_state.artikl_sel:
        dostupni = st.session_state.df_dobavljaci[
            st.session_state.df_dobavljaci["artikl"] == st.session_state.artikl_sel
        ].copy()

        if dostupni.empty:
            st.info("Nema dobavljača za izabrani artikl.")
        else:
            dostupni = dostupni.reset_index().rename(columns={"index": "_orig_idx"})

            st.dataframe(
                dostupni[["dobavljac", "artikl", "kolicina", "cena", "poeni"]],
                hide_index=True,
                use_container_width=True
            )

            st.session_state.dobavljac_sel = st.selectbox(
                "Dobavljač:",
                dostupni["dobavljac"].tolist(),
                key="dobavljac_widget"
            )

            trazena_kol = st.number_input(
                "Količina (kg):",
                min_value=1,
                step=1,
                key="kolicina_widget"
            )

            if st.button("Naruči", key="naruči_btn"):
                mask = (
                    (st.session_state.df_dobavljaci["dobavljac"] == st.session_state.dobavljac_sel) &
                    (st.session_state.df_dobavljaci["artikl"] == st.session_state.artikl_sel)
                )

                if not mask.any():
                    st.error("Odabrani dobavljač nije pronađen.")
                else:
                    idx = st.session_state.df_dobavljaci[mask].index[0]
                    dostupno = int(st.session_state.df_dobavljaci.at[idx, "kolicina"])

                    if int(trazena_kol) <= dostupno:
                        stavka = st.session_state.df_dobavljaci.loc[idx].to_dict()
                        stavka.update({
                            "id": f"{int(time.time())}_{idx}",
                            "kupac": st.session_state.kupac_sel,
                            "artikl": st.session_state.artikl_sel,
                            "kolicina_tražena": int(trazena_kol),
                            "kolicina_preostala": dostupno,
                            "status": "Čeka",
                            "_orig_idx": int(idx),
                        })
                        st.session_state.narudzbenica.append(stavka)
                        st.success("Narudžbina dodata.")
                        st.rerun()
                    else:
                        st.error("Nedovoljno na stanju!")

    st.subheader("Vaša narudžbenica")
    if st.session_state.narudzbenica:
        df_k = pd.DataFrame(st.session_state.narudzbenica)

        df_prihvacene = df_k[df_k["status"] == "Prihvaćeno"].copy()

        if not df_prihvacene.empty:
            df_prihvacene["Ukupno"] = (
                pd.to_numeric(df_prihvacene["kolicina_tražena"], errors="coerce").fillna(0)
                * pd.to_numeric(df_prihvacene["cena"], errors="coerce").fillna(0)
            )

            prikaz_kupac = df_prihvacene[[
                "kupac",
                "artikl",
                "kolicina_tražena",
                "cena",
                "Ukupno",
                "status"
            ]].copy()

            prikaz_kupac.columns = ["Kupac", "Artikl", "Količina", "Cena", "Ukupno", "Status"]

            total_sum = prikaz_kupac["Ukupno"].sum()

            total_row = pd.DataFrame([{
                "Kupac": "",
                "Artikl": "",
                "Količina": "",
                "Cena": "Zbir",
                "Ukupno": total_sum,
                "Status": ""
            }])

            prikaz_sa_totalom = pd.concat([prikaz_kupac, total_row], ignore_index=True)

            st.dataframe(prikaz_sa_totalom, hide_index=True, use_container_width=True)
        else:
            st.info("Nema prihvaćenih narudžbina.")
    else:
        st.info("Nema narudžbina.")

with tab_dobavljac:
    st.header("Upravljačka tabla — DOBAVLJAČ")

    moje_narudzbine = [
        n for n in st.session_state.narudzbenica
        if n.get("dobavljac") == "Meso-Prom d.o.o."
    ]

    if moje_narudzbine:
        df_narudzbenica = pd.DataFrame(moje_narudzbine)

        prikaz = df_narudzbenica[[
            "kupac",
            "artikl",
            "kolicina_tražena",
            "kolicina_preostala",
            "cena",
            "status"
        ]].copy()

        prikaz.columns = [
            "Kupac",
            "Artikl",
            "Količina",
            "Raspoloživo",
            "Cena",
            "Status"
        ]

        st.dataframe(prikaz, hide_index=True, use_container_width=True)

        st.subheader("Akcije po narudžbini")
        for i, stavka in enumerate(st.session_state.narudzbenica):
            if stavka.get("dobavljac") != "Meso-Prom d.o.o.":
                continue

            c1, c2, c3 = st.columns([5, 1, 1])

            c1.write(
                f"{stavka['kupac']} | {stavka['artikl']} | "
                f"{stavka['kolicina_tražena']} | {stavka['kolicina_preostala']} | "
                f"{stavka['cena']} | {stavka['status']}"
            )

            if c2.button("✅", key=f"ok_{stavka['id']}"):
                if st.session_state.narudzbenica[i]["status"] == "Čeka":
                    orig_idx = int(st.session_state.narudzbenica[i]["_orig_idx"])
                    kolicina_za_smanjenje = int(st.session_state.narudzbenica[i]["kolicina_tražena"])
                    trenutno = int(st.session_state.df_dobavljaci.loc[orig_idx, "kolicina"])
                    novo_stanje = trenutno - kolicina_za_smanjenje

                    st.session_state.df_dobavljaci.loc[orig_idx, "kolicina"] = novo_stanje
                    st.session_state.narudzbenica[i]["kolicina_preostala"] = novo_stanje
                    st.session_state.narudzbenica[i]["status"] = "Prihvaćeno"

                st.rerun()

            if c3.button("❌", key=f"no_{stavka['id']}"):
                if st.session_state.narudzbenica[i]["status"] == "Čeka":
                    st.session_state.narudzbenica[i]["status"] = "Odbijeno"
                st.rerun()
    else:
        st.info("Nema zahteva.")
