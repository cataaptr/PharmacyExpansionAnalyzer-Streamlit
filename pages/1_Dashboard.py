import streamlit as st
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

st.title("📈 Dashboard")

df = pd.read_excel("data/farmacia_tei_anual.xlsx")
df_latest = df[df["An"] == df["An"].max()] # preluare valori pt an 2024

col1, col2, col3 = st.columns(3)
col1.metric("📈 Cifra de afaceri", f'{df_latest["Cifra de Afaceri (RON)"].values[0]:,.0f} RON',border=True)
col2.metric("💰 Profit net", f'{df_latest["Profit Net (RON)"].values[0]:,.0f} RON',border=True)
col3.metric("👥 Angajați", f'{df_latest["Nr. Angajati"].values[0]}',border=True)

col1, col2= st.columns(2)
with col1:
    # chart type: Matplotlib
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot(df["An"], df["Cifra de Afaceri (RON)"], label="Cifra de afaceri")
    ax.plot(df["An"], df["Profit Net (RON)"], label="Profit net")
    ax.set_xlabel("An")
    ax.set_ylabel("Valori (RON)")
    ax.set_title("Evoluția cifrei de afaceri și profitului")
    ax.legend()
    st.pyplot(fig)

with col2:
    fig = px.line(df, x="An", y="Nr. Angajati", title="Evoluția numărului de angajați (2014–2023)",
              markers=True, labels={"Nr. Angajati": "Număr angajați"})
    st.plotly_chart(fig)

st.subheader("📊 Concluzii financiare și operaționale")
st.markdown("""
Evoluția Farmaciei Tei între 2014 și 2023 arată o **creștere accelerată** atât a cifrei de afaceri, cât și a profitului net.

- **Cifra de afaceri** a crescut, depășind 1 miliard RON în 2023.
- **Profitul net** a crescut semnificativ, dar mai lent, ceea ce sugerează investiții constante și expansiune.
- Numărul de **angajați** a crescut de la 0 în 2014 la peste 660 în 2023, confirmând extinderea activității la nivel național.

Acești indicatori susțin ideea că Farmacia Tei are capacitatea financiară și operațională pentru a continua extinderea în alte județe.
""")


