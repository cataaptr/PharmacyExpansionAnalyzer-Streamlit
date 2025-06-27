import streamlit as st

# setari principale pagina
st.set_page_config(
page_title="Farmacia Tei",
page_icon="🦠",
layout="wide", # sa apara pe toata pagina nu doar pe centru
initial_sidebar_state="expanded", # sidebar extints la default
)


st.title("👨‍⚕️ Despre Farmacia Tei")

# coloane: imagine | text
col1, col2= st.columns([1, 2])  # prima coloană mai îngustă

with col1:
    st.image("data/farmacia_tei_img1.png", width=400)

with col2:
    st.markdown("""Pionieri ai e-commerce-ului pe segmentul de farmacii online și ai conceptului de farmacii de dimensiuni mari, în Romania. 
    Astfel, **Farmaciatei.ro** oferă în acest moment peste 35.000 de produse farmaceutice şi parafarmaceutice, dorind să acopere cât mai multe din nevoile dumneavoastră.""")
    st.markdown("""
    🛒 Pe rafturile acestora se găsesc produse din următoarele categorii:
    - Medicamente OTC
    - Medicamente cu rețetă (disponibile doar cu titlu informativ)
    - Dispozitive medicale
    - Vitamine și suplimente
    - Dermato-cosmetice
    - Îngrijire personală
    - Dietă și wellness
    - Viață sexuală
    - Produse pentru îngrijirea animalelor de companie (VET)
    """)

st.subheader("🛠️ Fondatori")
st.markdown("""
    - **Răzvan Prisecaru** – administrator general  
    - **Elena Prisecaru** – fondatoare, implicată în dezvoltarea brandului  
    """)
st.subheader("📍 Locații actuale")
st.markdown("""
    - București
    - Constanța
    - Pitești
    - Brașov
    - Craiova
    """)







