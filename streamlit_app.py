# =========================================================
# HOME + OPERATIVNI MODUL
# =========================================================

import streamlit as st
import pandas as pd
import time

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="KAIZA",
    layout="wide"
)

# =========================================================
# PASSWORD
# =========================================================

PASSWORD = "796027Mrv"

if "authed" not in st.session_state:
    st.session_state.authed = False

if not st.session_state.authed:

    st.title("KAIZA")

    st.subheader(
        "Signal-driven B2B platforma"
    )

    pwd = st.text_input(
        "Pristupna lozinka",
        type="password"
    )

    if st.button("Pristupi platformi"):

        if pwd == PASSWORD:

            st.session_state.authed = True
            st.rerun()

        else:

            st.error("Pogrešna lozinka.")

    st.stop()

# =========================================================
# DATA
# =========================================================

if "df_dobavljaci" not in st.session_state:

    st.session_state.df_dobavljaci = pd.DataFrame([

        {
            "dobavljac": "Meso-Prom d.o.o.",
            "artikl": "Juneći Ramstek",
            "kolicina": 150,
            "signalna_kolicina": 50,
            "cena": 1850,
            "poeni": 91,
            "signal": "🟢 Stabilan"
        },

        {
            "dobavljac": "Meat Fresh d.o.o.",
            "artikl": "Juneći Ramstek",
            "kolicina": 500,
            "signalna_kolicina": 120,
            "cena": 1700,
            "poeni": 90,
            "signal": "🟢 Stabilan"
        },

        {
            "dobavljac": "Meso-Prom d.o.o.",
            "artikl": "Svinjski file",
            "kolicina": 300,
            "signalna_kolicina": 80,
            "cena": 1220,
            "poeni": 88,
            "signal": "🟢 Stabilan"
        },

        {
            "dobavljac": "Bio Garden",
            "artikl": "Paprika",
            "kolicina": 260,
            "signalna_kolicina": 70,
            "cena": 240,
            "poeni": 84,
            "signal": "🟢 Stabilan"
        },

    ])

if "narudzbenica" not in st.session_state:
    st.session_state.narudzbenica = []

# =========================================================
# HOME SCREEN
# =========================================================

st.title("KAIZA")

st.caption(
    "Signal_driven Operational Intelligence platform"
)

st.divider()

# =========================================================
# KPI
# =========================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Stabilnost mreže",
    "89%"
)

k2.metric(
    "Aktivne narudžbine",
    len(st.session_state.narudzbenica)
)

k3.metric(
    "Kritični artikli",
    len(
        st.session_state.df_dobavljaci[
            st.session_state.df_dobavljaci["signal"]
            == "🔴 Kritično"
        ]
    )
)

k4.metric(
    "Proceduralna odstupanja",
    "-22%"
)

st.divider()

# =========================================================
# SIGNAL CENTER
# =========================================================

st.subheader("📡 Signalni centar")

s1, s2, s3 = st.columns(3)

with s1:

    st.error(
        """
        🔴 Kritično stanje

        Rizik destabilizacije isporuke.
        """
    )

with s2:

    st.warning(
        """
        🟡 Povećano opterećenje

        Količina se približava signalnoj zalihi.
        """
    )

with s3:

    st.success(
        """
        🟢 Stabilno stanje

        Operativni tok stabilan.
        """
    )

st.divider()

# =========================================================
# NETWORK OVERVIEW
# =========================================================

st.subheader("🌐 Pregled mreže")

o1, o2 = st.columns(2)

with o1:

    st.info(
        """
        📦 OPERATIVNI TOK

        Aktivni dobavljači: 18

        Aktivni kupci: 42

        Dnevni protok artikala: 126
        """
    )

with o2:

    st.info(
        """
        📊 ANALITIKA

        Greške procesa: -37%

        Kašnjenja isporuke: -21%

        Operativni tok stabilan.
        """
    )

st.divider()

# =========================================================
# OPERATIVNI MODUL
# =========================================================

st.header("🧭 Operativni modul")

top_left, top_right = st.columns(2)
bottom_left, bottom_right = st.columns(2)

# =========================================================
# KUPAC
# =========================================================

with top_left:

    st.subheader("🍽 KUPAC")

    kupci = [
        "Hotel Moskva",
        "Restoran Dunav",
        "Hotel Park",
        "Villa Breg",
        "Restoran Central"
    ]

    artikli = sorted(
        st.session_state.df_dobavljaci["artikl"].unique()
    )

    kupac = st.selectbox(
        "Kupac",
        [""] + kupci
    )

    artikl = st.selectbox(
        "Artikl",
        [""] + artikli
    )

    if artikl != "":

        dostupni = st.session_state.df_dobavljaci[
            st.session_state.df_dobavljaci["artikl"] == artikl
        ]

        st.write("### Potencijalni dobavljači")

        st.dataframe(
            dostupni[
                [
                    "dobavljac",
                    "artikl",
                    "kolicina",
                    "signalna_kolicina",
                    "cena",
                    "poeni",
                    "signal"
                ]
            ].rename(columns={"kolicina": "raspoloziva kolicina"}),
            hide_index=True,
            use_container_width=True
        )

        dobavljaci_lista = (
            dostupni["dobavljac"]
            .unique()
            .tolist()
        )

        dobavljac = st.selectbox(
            "Dobavljač",
            [""] + dobavljaci_lista
        )

        kolicina = st.number_input(
            "Količina",
            min_value=1,
            step=1
        )

        if st.button("📤 Pošalji narudžbinu"):

            if (
                kupac == ""
                or artikl == ""
                or dobavljac == ""
            ):

                st.warning(
                    "Izaberite kupca, artikl i dobavljača."
                )

            else:

                mask = (
                    (
                        st.session_state.df_dobavljaci["dobavljac"]
                        ==
                        dobavljac
                    )
                    &
                    (
                        st.session_state.df_dobavljaci["artikl"]
                        ==
                        artikl
                    )
                )

                idx = st.session_state.df_dobavljaci[
                    mask
                ].index[0]

                dostupno = int(
                    st.session_state.df_dobavljaci.loc[
                        idx,
                        "kolicina"
                    ]
                )

                if kolicina <= dostupno:

                    stavka = (
                        st.session_state.df_dobavljaci
                        .loc[idx]
                        .to_dict()
                    )

                    stavka.update({

                        "id":
                        f"{int(time.time())}_{idx}",

                        "kupac":
                        kupac,

                        "kolicina_tražena":
                        int(kolicina),

                        "status":
                        "Čeka",

                        "_orig_idx":
                        int(idx)

                    })

                    st.session_state.narudzbenica.append(
                        stavka
                    )

                    st.success(
                        "Narudžbina poslata."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Nedovoljno raspoložive količine."
                    )


# =========================================================
# DOBAVLJAČ
# =========================================================

with top_right:

    st.subheader("🚛 DOBAVLJAČ")

    if st.session_state.narudzbenica:

        # =========================================
        # ZAHTEVI ZA OBRADU
        # =========================================

        st.write("### Aktivni zahtevi")

        for i, stavka in enumerate(
            st.session_state.narudzbenica
        ):

            if stavka["status"] != "Čeka":
                continue

            with st.container(border=True):

                st.write(
                    f"""
                    Kupac: {stavka['kupac']}

                    Artikl: {stavka['artikl']}

                    Količina: {stavka['kolicina_tražena']}

                    Status: {stavka['status']}
                    """
                )

                c1, c2 = st.columns(2)

                # =====================================
                # PRIHVATI
                # =====================================

                if c1.button(
                    "✅ Prihvati",
                    key=f"ok_{stavka['id']}"
                ):

                    if stavka["status"] == "Čeka":

                        orig_idx = stavka["_orig_idx"]

                        trenutno = int(
                            st.session_state
                            .df_dobavljaci
                            .loc[orig_idx, "kolicina"]
                        )

                        signalna = int(
                            st.session_state
                            .df_dobavljaci
                            .loc[
                                orig_idx,
                                "signalna_kolicina"
                            ]
                        )

                        nova_kolicina = (
                            trenutno
                            -
                            int(
                                stavka[
                                    "kolicina_tražena"
                                ]
                            )
                        )

                        # UPDATE KOLIČINE

                        st.session_state.df_dobavljaci.loc[
                            orig_idx,
                            "kolicina"
                        ] = nova_kolicina

                        # UPDATE SIGNALA

                        if nova_kolicina <= signalna:

                            novi_signal = "🔴 Kritično"

                        elif (
                            nova_kolicina
                            <=
                            signalna * 1.5
                        ):

                            novi_signal = "🟡 Upozorenje"

                        else:

                            novi_signal = "🟢 Stabilan"

                        st.session_state.df_dobavljaci.loc[
                            orig_idx,
                            "signal"
                        ] = novi_signal

                        # STATUS

                        st.session_state.narudzbenica[i][
                            "status"
                        ] = "Prihvaćeno"

                        st.rerun()

                # =====================================
                # ODBIJ
                # =====================================

                if c2.button(
                    "❌ Odbij",
                    key=f"no_{stavka['id']}"
                ):

                    if stavka["status"] == "Čeka":

                        st.session_state.narudzbenica[i][
                            "status"
                        ] = "Odbijeno"

                        st.rerun()

        # =========================================
        # ISPORUČENE NARUDŽBINE
        # =========================================

        st.divider()

        st.write("### 📦 Prihvaćene narudžbine dobavljača")

        df_isporuke = pd.DataFrame(
            st.session_state.narudzbenica
        )

        df_isporuke = df_isporuke[
            df_isporuke["status"] == "Prihvaćeno"
        ]

        if not df_isporuke.empty:

            df_isporuke["Ukupno"] = (
                df_isporuke["kolicina_tražena"]
                *
                df_isporuke["cena"]
            )

            prikaz_isporuke = df_isporuke[
                [
                    "dobavljac",
                    "kupac",
                    "artikl",
                    "kolicina_tražena",
                    "cena",
                    "Ukupno"
                ]
            ].copy()

            prikaz_isporuke.columns = [
                "Dobavljač",
                "Kupac",
                "Artikl",
                "Količina",
                "Cena",
                "Ukupno"
            ]

            st.dataframe(
                prikaz_isporuke,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "Nema realizovanih isporuka."
            )

    else:

        st.info("Nema zahteva.")



# =========================================================
# STANJE SISTEMA
# =========================================================

with bottom_right:

    st.subheader("📦 Stanje sistema")

    st.dataframe(
        st.session_state.df_dobavljaci[
            [
                "dobavljac",
                "artikl",
                "kolicina",
                "signalna_kolicina",
                "signal",
                "poeni"
            ]
        ].rename(columns={"kolicina": "raspoloziva kolicina"}),
        hide_index=True,
        use_container_width=True
    )

    st.info(
        """
        ℹ️ SIGNAL STABILNOSTI

        Signal predstavlja procenu operativne
        stabilnosti artikla u mreži.

        Kada količina padne ispod signalnog
        praga povećava se rizik:
        - kašnjenja,
        - proceduralnih odstupanja,
        - i destabilizacije isporuke.
        """
    )

st.divider()

st.caption(
    "KAIZA • Signal-driven operational intelligence"
)
