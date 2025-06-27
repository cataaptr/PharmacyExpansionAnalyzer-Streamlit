import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import plotly.express as px

# setari principale pagina
st.set_page_config(
page_title="Farmacia Tei",
page_icon="🦠",
layout="wide", # sa apara pe toata pagina nu doar pe centru
initial_sidebar_state="expanded", # sidebar extints la default
)


st.title("⚡ Clusterizarea județelor pe baza indicatorilor")

st.markdown("""
Am aplicat algoritmul de **KMeans** pentru a identifica grupuri de județe similare în funcție de:
- populație (scalată),
- salariul mediu (scalat),
- numărul de farmacii la 100.000 locuitori.

Această tehnică ajută la identificarea automată a regiunilor cu caracteristici comune, fără o variabilă țintă.
""")

# citire date
df = pd.read_excel("data/farmacia_tei_anual.xlsx", sheet_name=1)
df = df[df["Judet"].notna()]
df = df[~df["Judet"].isin(["MIN", "MAX"])]

# aplicare scalare
scaler = MinMaxScaler()
df[["Populatie_scaled", "Salariu_Mediu_scaled"]] = scaler.fit_transform(
    df[["Populatie", "Salariu_Mediu"]]
)

# selectare coloane pentru clusterizare
X = df[["Populatie_scaled", "Salariu_Mediu_scaled", "Farmacii_pe_100k.1"]].dropna()

# aplicare KMeans pe datele fără NaN
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X)

# initializare cu NaN și completare doar acolo unde avem date ok
df["Cluster"] = pd.NA
df.loc[X.index, "Cluster"] = cluster_labels


# afisare date sub formă tabelară
st.subheader("📋 Județele și grupul din care fac parte")
st.dataframe(df[["Judet", "Populatie", "Salariu_Mediu", "Farmacii_pe_100k.1", "Cluster"]].sort_values(by="Cluster"))

# grafic per cluster
st.subheader("📊 Distribuția județelor pe clustere")

# Pregătim datele
cluster_counts = df["Cluster"].value_counts().sort_index().reset_index()
cluster_counts.columns = ["Cluster", "Număr_județe"]

# Creăm graficul
fig = px.bar(cluster_counts, x="Cluster", y="Număr_județe",
             title="Distribuția județelor în clustere",
             labels={"Cluster": "Cluster ID", "Număr_județe": "Număr județe"},
             text="Număr_județe")

fig.update_layout(xaxis=dict(type='category'))
st.plotly_chart(fig)
