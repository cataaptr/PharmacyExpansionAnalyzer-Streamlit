import streamlit as st
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler

# setari principale pagina
st.set_page_config(
page_title="Farmacia Tei",
page_icon="🦠",
layout="wide", # sa apara pe toata pagina nu doar pe centru
initial_sidebar_state="expanded", # sidebar extints la default
)

st.title("🧮 Analiză de regresie")

st.markdown("""
Pentru a înțelege mai bine factorii care influențează **scorul de extindere**, am aplicat un model de regresie multiplă.  
Acesta estimează `Scor_extindere` pe baza a trei variabile explicative:

- `Populatie_scaled`
- `Salariu_Mediu_scaled`
- `Farmacii_pe_100k.1` (numărul de farmacii raportat la 100k locuitori)

Modelul a fost construit cu ajutorul pachetului `statsmodels`.
""")

# citire date pagina cu farmacii
df = pd.read_excel("data/farmacia_tei_anual.xlsx", sheet_name=1)

# eliminare valori invalide (MIN, MAX, etc.)
df = df[df["Judet"].notna()]
df = df[~df["Judet"].isin(["MIN", "MAX"])]

# extrage min/max pentru normalizare manuală
pop_min, pop_max = df["Populatie"].min(), df["Populatie"].max()
sal_min, sal_max = df["Salariu_Mediu"].min(), df["Salariu_Mediu"].max()
farm_min, farm_max = df["Farmacii_pe_100k.1"].min(), df["Farmacii_pe_100k.1"].max()

# aplicare scalare - pt a aduce datele pe acelasi scara
scaler = MinMaxScaler()
df[["Populatie_scaled", "Salariu_Mediu_scaled"]] = scaler.fit_transform(
    df[["Populatie", "Salariu_Mediu"]]
)

# definire variabile pt model
X = df[["Populatie_scaled", "Salariu_Mediu_scaled", "Farmacii_pe_100k.1"]]
y = df["Scor_extindere"] # variabila pe care vrem sa o estimam
X = sm.add_constant(X)

# eliminare valori lipsa
data = pd.concat([X, y], axis=1).dropna()
X = data.drop("Scor_extindere", axis=1)
y = data["Scor_extindere"]

# construire model
model = sm.OLS(y, X).fit()


st.subheader("🔍 Estimare scor pentru un județ ipotetic")

# Limite reale din setul tău de date (le poți ajusta după nevoie)
pop_min, pop_max = df["Populatie"].min(), df["Populatie"].max()
sal_min, sal_max = df["Salariu_Mediu"].min(), df["Salariu_Mediu"].max()

# input user
pop_real = st.number_input("Populație (locuitori)", min_value=200000, value=500000, max_value=700000)
sal_real = st.number_input("Salariu mediu (RON)", min_value=4000, value=4500,max_value=6000)
farm_total = st.number_input("Număr total farmacii în județ", min_value=20, max_value=500, value=30)

farm_per_100k = (farm_total / pop_real) * 100000 if pop_real > 0 else 0

# normalizare manuală
pop_norm = (pop_real - pop_min) / (pop_max - pop_min)
sal_norm = (sal_real - sal_min) / (sal_max - sal_min)

FARM_MIN = 0
FARM_MAX = 150  # poți ajusta în funcție de ce consideri ca fiind „saturație”

farm_norm = (farm_per_100k - FARM_MIN) / (FARM_MAX - FARM_MIN)
farm_norm = max(0, min(farm_norm, 1))  # scor între 0 și 1





# scor compozit
scor = 0.4 * pop_norm + 0.3 * sal_norm + 0.3 * (1 - farm_norm)
scor = max(0, min(scor, 1))  # pentru siguranță, scorul e între 0 și 1

# scalare
pop_scaled = scaler.transform([[pop_real, sal_real]])[0][0]
sal_scaled = scaler.transform([[pop_real, sal_real]])[0][1]

# pregatire date
input_data = pd.DataFrame({
    "const": [1.0],
    "Populatie_scaled": [pop_scaled],
    "Salariu_Mediu_scaled": [sal_scaled],
    "Farmacii_pe_100k.1": [farm_per_100k]
})


# estimare scor
real_pred = model.predict(input_data)[0]
display_pred = max(0, real_pred)

# buton
if st.button("Calculează scorul"):
    st.markdown(f"📌 **Scor estimat (normalizat):** `{scor*100:.2f}` %")
    st.markdown(f"📊 **Scor estimat (regresie):** `{real_pred * 100:.2f}` %")