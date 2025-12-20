import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# -------------------------------
# Configuration de la page
# -------------------------------
st.set_page_config(
    page_title="Habit Tracker Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Chemin robuste vers le CSV
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.csv")

# -------------------------------
# Chargement des données (CACHE)
# -------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    if not os.path.exists(DATA_FILE):
        st.error(f"Fichier introuvable : {DATA_FILE}")
        st.stop()

    try:
        df = pd.read_csv(DATA_FILE, parse_dates=["date"])
        return df
    except Exception as e:
        st.error("Erreur lors de la lecture du fichier CSV")
        st.exception(e)
        st.stop()

# -------------------------------
# Calcul du score
# -------------------------------
def calculate_score(row):
    score = 0
    score += row.get("missions_terminees", 0) * 10
    score += row.get("deep_work_total", 0) / 12
    score -= row.get("interruptions_total", 0) / 6
    score += row.get("pauses_total", 0) / 15
    score += row.get("energie", 3) * 3
    score -= row.get("charge_mentale", 3) * 2
    return round(max(min(score, 100), 0), 2)

# -------------------------------
# Chargement effectif
# -------------------------------
df = load_data()

if df.empty:
    st.warning("Le fichier CSV est vide.")
    st.stop()

if "score" not in df.columns:
    df["score"] = df.apply(calculate_score, axis=1)

df = df.sort_values("date", ascending=False)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.markdown("## Habit Tracker")
    page = st.radio(
        "Navigation",
        ["Résumé", "Missions", "Deep Work", "Pauses", "Sommeil", "Score"],
        label_visibility="collapsed"
    )

# -------------------------------
# PAGE : Résumé (exemple minimal)
# -------------------------------
if page == "Résumé":
    st.title("Résumé")

    st.metric("Score moyen", f"{df['score'].mean():.1f} / 100")
    st.metric("Nombre de jours suivis", len(df))

    fig = px.line(
        df.iloc[::-1],
        x="date",
        y="score",
        markers=True,
        title="Évolution du score"
    )
    st.plotly_chart(fig, use_container_width=True)

# Les autres pages peuvent être recollées telles quelles en dessous
