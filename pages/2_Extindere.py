import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# setari principale pagina
st.set_page_config(
page_title="Farmacia Tei",
page_icon="🦠",
layout="wide", # sa apara pe toata pagina nu doar pe centru
initial_sidebar_state="expanded", # sidebar extints la default
)
st.subheader("🧭 Analiza extinderii în alte județe")

with st.expander("📌 Cum am calculat scorul de extindere?"):
    st.markdown("""
    Scorul de extindere a fost calculat pe baza a trei indicatori:
    - Populație (normalizată),
    - Salariu mediu (normalizat),
    - Numărul de farmacii raportat la 100.000 locuitori.
    """)


# citire geojson + datele tale
gdf = gpd.read_file("data/romania_judete.geojson")  # sau calea ta completă
df = pd.read_excel("data/farmacia_tei_anual.xlsx", sheet_name=1)
df_filtrat = df[df["Judet"].notna()]  # elimină NaN
df_filtrat = df_filtrat[~df_filtrat["Judet"].str.lower().isin(["min", "max", "none"])]
df=df_filtrat

# tratare valorilor extreme (0 și 1)
df["Populatie_norm"] = df["Populatie_norm"].replace({0: 0.01, 1: 0.99})
df["Salariu_Mediu_norm"] = df["Salariu_Mediu_norm"].replace({0: 0.01, 1: 0.99})
df["Farmacii_pe_100k.1"] = df["Farmacii_pe_100k.1"].replace({0: 0.01, 1: 0.99})


st.subheader("📊 Statistici descriptive generale")
st.dataframe(df[["Populatie", "Salariu_Mediu", "Farmacii_pe_100k.1"]].describe())


# normalizare numele județelor
df["Judet"] = df["Judet"].str.lower().str.strip()
gdf["Judet"] = gdf["name"].str.lower().str.strip()

st.subheader("🗺️ Hartă extindere Farmacia Tei pe județe")

# join intre judetele mele si harta
gdf = gdf.merge(df, on="Judet", how="left")

# coloane: imagine | top 3
col1, col2= st.columns([3,1])

with col1:
    # hartă
    fig, ax = plt.subplots(figsize=(10, 8))
    gdf.plot(column="Scor_extindere", cmap="OrRd", legend=True, ax=ax, edgecolor="black")
    #ax.set_title("Scor extindere", fontsize=15)
    ax.axis("off")
    st.pyplot(fig)

# extrage top 3 și bottom 3 direct din gdf
top3 = gdf[["name", "Scor_extindere"]].sort_values(by="Scor_extindere", ascending=False).head(3)
bottom3 = gdf[["name", "Scor_extindere"]].sort_values(by="Scor_extindere", ascending=True).head(3)

with col2:
# afisare
    st.subheader("⭐ Top 3 județe cu potențial ridicat de extindere:")
    for _, row in top3.iterrows():
        st.markdown(f"- {row['name']} (scor: {row['Scor_extindere']:.2f})")

    st.subheader("❌ Top 3 județe cu potențial redus de extindere:")
    for _, row in bottom3.iterrows():
        st.markdown(f"- {row['name']} (scor: {row['Scor_extindere']:.2f})")


# codificare
def codificare_scor(val):
    if val >= 0.7:
        return 2  # potențial mare
    elif val >= 0.5:
        return 1  # potențial mediu
    else:
        return 0  # potențial redus

st.subheader("🌍 Distribuția județelor în funcție de scorul de extindere")
# tip grafic: pie chart
# pregatire date
df["scor_categorie"] = df["Scor_extindere"].apply(codificare_scor)
scoruri = df["scor_categorie"].value_counts().sort_index()
scoruri.index = ["Scăzut", "Mediu", "Ridicat"]
pie_data = scoruri.reset_index()
pie_data.columns = ["Categorie", "Număr județe"]

fig = px.pie(pie_data, values="Număr județe", names="Categorie") # creare grafic
st.plotly_chart(fig)


# functii de grup
st.subheader("🧮 Medii ale populației și salariului mediu în funcție de potențialul de extindere")
medii = df.groupby("scor_categorie")[["Populatie", "Salariu_Mediu"]].mean()
st.dataframe(medii)
