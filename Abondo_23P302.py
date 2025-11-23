import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# Fichier de stockage
# -----------------------------
DATA_FILE = "chantiers.xlsx"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Chantier","Avancement","Sécurité","Propreté","Commentaire"])
    df_init.to_excel(DATA_FILE, index=False)

# -----------------------------
# Page principale
# -----------------------------
st.title("📋 Collecte de données sur l'état d'un chantier")
st.write("Remplissez le formulaire ci-dessous pour enregistrer l'état du chantier.")

# Formulaire
with st.form("form_chantier"):
    chantier = st.text_input("Nom du chantier")
    avancement = st.slider("Avancement (%)", min_value=0, max_value=100, step=5)
    securite = st.selectbox("Sécurité", ["Très bonne", "Bonne", "Moyenne", "Faible"])
    proprete = st.selectbox("Propreté", ["Très propre", "Propre", "Moyenne", "Sale"])
    commentaire = st.text_area("Commentaire (optionnel)")
    submit = st.form_submit_button("Enregistrer")

# Enregistrement des données
if submit:
    if not chantier:
        st.error("Le nom du chantier est obligatoire.")
    else:
        try:
            df = pd.read_excel(DATA_FILE)
        except:
            df = pd.DataFrame(columns=["Chantier","Avancement","Sécurité","Propreté","Commentaire"])
        
        new_row = pd.DataFrame({
            "Chantier":[chantier],
            "Avancement":[avancement],
            "Sécurité":[securite],
            "Propreté":[proprete],
            "Commentaire":[commentaire]
        })
        df = pd.concat([df,new_row], ignore_index=True)
        df.to_excel(DATA_FILE, index=False)
        st.success("✅ Données enregistrées !")

# -----------------------------
# Affichage des diagrammes
# -----------------------------
def plot_bar(variable, title):
    try:
        df_plot = pd.read_excel(DATA_FILE)
        if variable not in df_plot.columns or df_plot[variable].empty:
            st.info(f"Aucune donnée pour {variable}.")
            return
        counts = df_plot[variable].value_counts()
        fig, ax = plt.subplots()
        ax.bar(counts.index, counts.values, color="#69b3a2")
        ax.set_ylabel("Nombre d'observations")
        ax.set_title(title)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    except:
        st.info("Pas encore de données.")

st.subheader("📈 Aperçu des résultats")
plot_bar("Avancement", "Distribution de l'avancement")
plot_bar("Sécurité", "État de la sécurité")
plot_bar("Propreté", "État de la propreté")