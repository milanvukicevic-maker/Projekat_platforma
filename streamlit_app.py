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

if "kupac" not in st.session_state:
    st.session_state.kupac = ""

if "artikl" not in st.session_state:
    st.session_state.artikl = ""

df_kupci = pd.DataFrame({"Naziv_Firme": ["Hotel Moskva", "Restoran Dunav"]})
df_artikli = pd.DataFrame({"Artikl": ["Ramstek", "But", "Paradajz"]})

def potvrdi_narudzbinu():
    key = st.session_state.get("editor_key")
    if not key:
        return

    state = st.session_state.get(key)
    if state is None:
        return

    edited_rows = state.get("edited_rows", {})
    if not edited_rows:
        return

    trenutno = st.session_state.get("editor_df")
    if trenutno is None or trenutno.empty:
        return

    for row_idx_str, change in edited_rows.items():
        row_idx = int(row_idx_str)
        if row_idx < 0 or row_idx >= len(trenutno):
            continue

        unos = change.get("Unos_Količine", 0)
        if unos is None or unos <= 0:
            continue

        orig_idx = int(trenutno.iloc[row_idx]["_orig_idx"])
        raspolozivo = st.session_state.df_dobavljaci.at[orig_idx, "kolicina"]

        if unos > raspolozivo:
            st.session_state.msg = f"Nedovoljno zaliha kod {trenutno.iloc[row_idx]['dobavljac']}."
            continue

        st.session_state.df_dobavljaci.at[orig_idx, "kolicina"] = raspolozivo - unos

        st.session_state.narudzbenica.append({
            "id": f"{int(time.time())}_{orig_idx}",
            "kupac": st.session_state.kupac,
            "artikl": trenutno.iloc[row_idx]["artikl"],
            "dobavljac": trenutno.iloc[row_idx]["dobavljac"],
            "kolicina_tražena": unos,
            "status": "Čeka",
        })

    st.session_state.msg = "Narudžbina je uneta."
    st.session_state[key]["edited_rows"] = {}

tab_kupac, tab_dobavljac = st.tabs(["🛒 KUPAC", "🚛 DOBAVLJAČ"])

with tab_kupac:
    st.header("Kupac")

    st.session_state.kupac = st.selectbox(
        "Firma:",
        [""] + df_kupci["Naziv_Firme"].tolist(),
        index=0 if st.session_state.kupac == "" else (df_kupci["Naziv_Firme"].tolist().index(st.session_state.kupac) + 1)
    )

    st.session_state.artikl = st.selectbox(
        "Artikl:",
        [""] + df_artikli["Artikl"].tolist(),
        index=0 if st.session_state.artikl == "" else (df_artikli["Artikl"].tolist().index(st.session_state.artikl) + 1)
    )

    if st.session_state.kupac and st.session_state.artikl:
        mask = st.session_state.df_dobavljaci["artikl"] == st.session_state.artikl
        editor_df = st.session_state.df_dobavljaci.loc[mask].copy()

        if editor_df.empty:
            st.info("Nema dobavljača za izabrani artikl.")
        else:
            editor_df = editor_df.reset_index().rename(columns={"index": "_orig_idx"})
            editor_df["Unos_Količine"] = 0

            st.session_state.editor_df = editor_df
            st.session_state.editor_key = f"editor_{st.session_state.kupac}_{st.session_state.artikl}"

            st.data_editor(
                st.session_state.editor_df,
                key=st.session_state.editor_key,
                hide_index=True,
                num_rows="fixed",
                use_container_width=True,
                column_config={
                    "_orig_idx": st.column_config.NumberColumn("ID", disabled=True),
                    "Unos_Količine": st.column_config.NumberColumn("Unos_Količine", min_value=0, step=1),
                    "kolicina": st.column_config.NumberColumn("Raspoloživo", disabled=True),
                    "cena": st.column_config.NumberColumn("Cena", disabled=True),
                    "dobavljac": st.column_config.TextColumn("Dobavljač", disabled=True),
                    "artikl": st.column_config.TextColumn("Artikl", disabled=True),
                },
                disabled=["_orig_idx", "dobavljac", "artikl", "kolicina", "cena"],
            )

            st.button("Potvrdi narudžbinu", on_click=potvrdi_narudzbinu)

    if "msg" in st.session_state:
        st.info(st.session_state.msg)

    st.subheader("Narudžbenica")
    if st.session_state.narudzbenica:
        st.dataframe(pd.DataFrame(st.session_state.narudzbenica), hide_index=True, use_container_width=True)
    else:
        st.write("Nema narudžbina.")

with tab_dobavljac:
    st.header("Dobavljač")
    if st.session_state.narudzbenica:
        for i, n in enumerate(st.session_state.narudzbenica):
            c1, c2, c3 = st.columns([4, 1, 1])
            c1.write(f"{n['kupac']} | {n['artikl']} | {n['dobavljac']} | {n['kolicina_tražena']} | {n['status']}")
            if c2.button("✅", key=f"ok_{n['id']}"):
                st.session_state.narudzbenica[i]["status"] = "Prihvaćeno"
                st.rerun()
            if c3.button("❌", key=f"no_{n['id']}"):
                st.session_state.narudzbenica[i]["status"] = "Odbijeno"
                st.rerun()
    else:
        st.info("Nema zahteva.")
