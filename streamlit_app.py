import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="KAIZA B2B", layout="wide")
st.title("KAIZA B2B Platforma")

if "df_dobavljaci" not in st.session_state:
    st.session_state.df_dobavljaci = pd.DataFrame([
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Juneći Ramstek", "kolicina": 150, "cena": 1850, "poeni": 91},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Juneći Ramstek", "kolicina": 500, "cena": 1700, "poeni": 90},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Svinjski But bk", "kolicina": 200, "cena": 1400, "poeni": 85},
        {"dobavljac": "Green Market", "artikl": "Paradajz", "kolicina": 300, "cena": 220, "poeni": 88},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Piletina file", "kolicina": 120, "cena": 980, "poeni": 87},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Juneći But bk", "kolicina": 350, "cena": 1420, "poeni": 89},
        {"dobavljac": "Green Market", "artikl": "Krastavac", "kolicina": 420, "cena": 180, "poeni": 86},
        {"dobavljac": "Bio Garden", "artikl": "Paprika", "kolicina": 260, "cena": 240, "poeni": 84},
        {"dobavljac": "Fresh Point", "artikl": "Krompir", "kolicina": 500, "cena": 95, "poeni": 82},
        {"dobavljac": "Meso-Prom d.o.o.", "artikl": "Pileći Batak", "kolicina": 180, "cena": 760, "poeni": 88},
        {"dobavljac": "Agro Fresh d.o.o.", "artikl": "Kupus", "kolicina": 200, "cena": 300, "poeni": 80},
        {"dobavljac": "Green Market", "artikl": "Šargarepa", "kolicina": 300, "cena": 280, "poeni": 81},
        {"dobavljac": "Bio Garden", "artikl": "Kupus", "kolicina": 220, "cena": 290, "poeni": 82},
    ])

if "narudzbenica" not in st.session_state:
    st.session_state.narudzbenica = []

df_artikli = pd.DataFrame({
    "Artikl": [
        "Juneći Ramstek",
        "Juneći But bk",
        "Svinjski But bk",
        "Piletina file",
        "Pileći Batak",
        "Paradajz",
        "Krastavac",
        "Paprika",
        "Krompir",
        "Kupus"
        "Šargarepa"
    ]
})

df_kupci = pd.DataFrame({
    "Naziv_Firme": [
        "Hotel Moskva",
        "Restoran Dunav",
        "Hotel Park",
        "Villa Breg",
        "Restoran Central"
    ]
})

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

    moje_narudzbine = st.session_state.narudzbenica

    if moje_narudzbine:
        df_narudzbenica = pd.DataFrame(moje_narudzbine)

        prikaz = df_narudzbenica[[
            "kupac",
            "dobavljac",
            "artikl",
            "kolicina_tražena",
            "kolicina_preostala",
            "cena",
            "status"
        ]].copy()

        prikaz.columns = [
            "Kupac",
            "Dobavljač",
            "Artikl",
            "Količina",
            "Raspoloživo",
            "Cena",
            "Status"
        ]

        st.dataframe(prikaz, hide_index=True, use_container_width=True)

        st.subheader("Akcije po narudžbini")
        for i, stavka in enumerate(st.session_state.narudzbenica):
            c1, c2, c3 = st.columns([5, 1, 1])

            c1.write(
                f"{stavka.get('kupac', '')} | {stavka.get('dobavljac', '')} | "
                f"{stavka.get('artikl', '')} | {stavka.get('kolicina_tražena', '')} | "
                f"{stavka.get('kolicina_preostala', '')} | {stavka.get('cena', '')} | "
                f"{stavka.get('status', '')}"
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
