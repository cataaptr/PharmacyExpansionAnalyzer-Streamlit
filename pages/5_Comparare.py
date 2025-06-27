import streamlit as st
import pandas as pd

# preluare date
df = pd.read_excel("data/farmacia_tei_anual.xlsx", sheet_name=1)
df_filtrat = df[df["Judet"].notna()]  # elimină NaN
df_filtrat = df_filtrat[~df_filtrat["Judet"].str.lower().isin(["min", "max", "none"])]
df=df_filtrat

st.title("🔍 Comparație între județe")

# selecție județe
col1, col2 = st.columns(2)
with col1:
    judet1 = st.selectbox("Alege primul județ", df["Judet"].unique())
with col2:
    judet2 = st.selectbox("Alege al doilea județ", df["Judet"].unique())

# buton comparare
if st.button("🔁 Compară județele"):
    # validare selecție
    if judet1 == judet2:
        st.info("ℹ️ Ai selectat același județ de două ori. Alege două județe diferite.")
    else:
        # filtrare
        date1 = df[df["Judet"] == judet1].reset_index(drop=True)
        date2 = df[df["Judet"] == judet2].reset_index(drop=True)

        # afișare tabele
        c1, c2 = st.columns(2)
        with c1:
            st.subheader(f"📍 {judet1}")
            st.dataframe(date1[["Populatie", "Salariu_Mediu", "Farmacii_pe_100k.1", "Scor_extindere"]].T)
        with c2:
            st.subheader(f"📍 {judet2}")
            st.dataframe(date2[["Populatie", "Salariu_Mediu", "Farmacii_pe_100k.1", "Scor_extindere"]].T)

        # extragere scoruri
        scor1 = date1["Scor_extindere"].values[0]
        scor2 = date2["Scor_extindere"].values[0]

        # recomandare
        if scor1 > scor2:
            st.success(f"✅ Recomandare: Județul **{judet1}** are un scor mai mare și este mai potrivit pentru extindere.")
        elif scor2 > scor1:
            st.success(f"✅ Recomandare: Județul **{judet2}** are un scor mai mare și este mai potrivit pentru extindere.")
        else:
            st.info("⚖️ Ambele județe au scoruri egale. Se recomandă o analiză calitativă suplimentară.")
