import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
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
# Palette de couleurs moderne
# -------------------------------
colors = {
    "primary": "#71c4ef",
    "primary_light": "#d4eaf7",
    "primary_dark": "#00668c",
    "accent": "#5b9bd5",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "text_dark": "#1d1c1c",
    "text_light": "#6c757d",
    "bg_light": "#f8f9fa",
    "bg_card": "#ffffff",
    "border": "#e9ecef"
}

# -------------------------------
# CSS personnalisé
# -------------------------------
st.markdown(f"""
<style>
    [data-testid="stSidebar"] {{
        background-color: {colors["bg_light"]};
        padding: 2rem 1rem;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 600;
        color: {colors["text_dark"]};
    }}
    .metric-card {{
        background-color: {colors["bg_card"]};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid {colors["border"]};
        margin-bottom: 1rem;
    }}
    .income-item {{
        background-color: {colors["bg_card"]};
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid {colors["border"]};
    }}
    .income-positive {{
        color: {colors["success"]};
        font-weight: 600;
    }}
    .dashboard-header {{
        background: linear-gradient(135deg, {colors["primary_light"]} 0%, {colors["primary"]} 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: {colors["text_dark"]};
    }}
    .balance-display {{
        font-size: 3rem;
        font-weight: 700;
        color: {colors["text_dark"]};
        margin-top: 0.5rem;
    }}
    .profile-section {{
        text-align: center;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }}
    .profile-name {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {colors["text_dark"]};
        margin-top: 0.5rem;
    }}
    .profile-role {{
        color: {colors["text_light"]};
        font-size: 0.9rem;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Fichier de données
# -------------------------------
DATA_FILE = "data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, parse_dates=["date"])
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier CSV : {e}")
            return pd.DataFrame()
    else:
        st.error(f"Le fichier '{DATA_FILE}' est introuvable.")
        return pd.DataFrame()

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
# Charger les données
# -------------------------------
df = load_data()
if df.empty:
    st.warning("Aucune donnée à afficher. Vérifiez votre fichier CSV.")
    st.stop()

if "score" not in df.columns:
    df["score"] = df.apply(calculate_score, axis=1)

df = df.sort_values("date", ascending=False)

# -------------------------------
# Sidebar avec profil et navigation
# -------------------------------
with st.sidebar:
    st.markdown("""
    <div class="profile-section">
        <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #71c4ef 0%, #00668c 100%); 
                    border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 2rem; font-weight: 600;">HT</span>
        </div>
        <div class="profile-name">Habit Tracker</div>
        <div class="profile-role">Productivity Manager</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio("Navigation", [
        "Résumé",
        "Missions",
        "Deep Work",
        "Pauses",
        "Sommeil",
        "Score"
    ], label_visibility="collapsed")

    st.markdown("---")

    st.markdown("### Stats Rapides")
    recent_score = df.iloc[0]["score"] if not df.empty else 0
    st.metric("Score du jour", f"{recent_score:.1f}",
              f"{recent_score - df.iloc[1]['score']:.1f}" if len(df) > 1 else "0")

    avg_sleep = df["sommeil_duree"].mean()
    st.metric("Sommeil moyen", f"{avg_sleep:.1f}h")

    total_deepwork = df["deep_work_total"].sum() / 60
    st.metric("Deep Work total", f"{total_deepwork:.0f}h")

# -------------------------------
# Pages
# -------------------------------
if page == "Résumé":
    # Code de la page Résumé (inchangé, juste sans emojis)
    # ... ton code existant pour Résumé
    pass

elif page == "Missions":
    # Page Missions
    # ... ton code existant pour Missions
    pass

elif page == "Deep Work":
    # Page Deep Work
    # ... ton code existant pour Deep Work
    pass

elif page == "Pauses":
    # Page Pauses
    # ... ton code existant pour Pauses
    pass

elif page == "Sommeil":
    # Page Sommeil
    # ... ton code existant pour Sommeil
    pass

elif page == "Score":
    # Page Score
    # ... ton code existant pour Score
    pass
