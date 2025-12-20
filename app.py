import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
# Palette de couleurs
# -------------------------------
colors = {
    "primary": "#71c4ef",
    "primary_light": "#d4eaf7",
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
    st.warning("Aucune donnée à afficher.")
    st.stop()

# Calculer le score si absent
if "score" not in df.columns:
    df["score"] = df.apply(calculate_score, axis=1)

df = df.sort_values("date", ascending=False)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.markdown("### Profil")
    st.markdown("**Habit Tracker**  \nProductivity Manager")
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
    
    # Statistiques rapides
    recent_score = df.iloc[0]["score"] if len(df) > 0 else 0
    st.metric("Score du jour", f"{recent_score:.1f}")
    st.metric("Sommeil moyen", f"{df['sommeil_duree'].mean():.1f}h")
    st.metric("Deep Work total", f"{df['deep_work_total'].sum() / 60:.0f}h")

# -------------------------------
# Pages
# -------------------------------

# Résumé
if page == "Résumé":
    st.markdown(f"### Score de productivité moyen: {df['score'].mean():.1f}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Missions / jour", f"{df['missions_terminees'].mean():.1f}")
    col2.metric("Deep Work / jour", f"{(df['deep_work_total'].mean()/60):.1f}h")
    col3.metric("Sommeil moyen", f"{df['sommeil_duree'].mean():.1f}h")
    col4.metric("Énergie moyenne", f"{df['energie'].mean():.1f}/5")
    
    # Graphique Score
    fig_score = go.Figure()
    fig_score.add_trace(go.Scatter(
        x=df["date"].iloc[::-1],
        y=df["score"].iloc[::-1],
        mode='lines+markers',
        line=dict(color=colors["primary"])
    ))
    st.plotly_chart(fig_score, use_container_width=True)

# Missions
elif page == "Missions":
    st.title("Missions")
    st.metric("Total Missions", f"{df['missions_terminees'].sum()}")
    st.metric("Moyenne / jour", f"{df['missions_terminees'].mean():.1f}")
    st.metric("Meilleur jour", f"{df.loc[df['missions_terminees'].idxmax()]['missions_terminees']}")
    
    fig = px.bar(df.tail(30).iloc[::-1], x="date", y="missions_terminees",
                 color_discrete_sequence=[colors["primary"]])
    st.plotly_chart(fig, use_container_width=True)
    
    display_df = df[["date", "missions_terminees"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df.columns = ["Date", "Missions Terminées"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# Deep Work
elif page == "Deep Work":
    st.title("Deep Work")
    st.metric("Total Heures", f"{df['deep_work_total'].sum() / 60:.0f}h")
    st.metric("Sessions / jour", f"{df['deep_work_sessions'].mean():.1f}")
    st.metric("Durée moy. session", f"{(df['deep_work_total'].mean() / df['deep_work_sessions'].mean()):.0f}min")
    
    fig_sessions = px.bar(df.tail(30).iloc[::-1], x="date", y="deep_work_sessions",
                          color_discrete_sequence=[colors["accent"]])
    st.plotly_chart(fig_sessions, use_container_width=True)
    
    fig_total = px.line(df.tail(30).iloc[::-1], x="date", y="deep_work_total",
                        markers=True, color_discrete_sequence=[colors["primary"]])
    st.plotly_chart(fig_total, use_container_width=True)

# Pauses
elif page == "Pauses":
    st.title("Pauses")
    st.metric("Total Pauses", f"{df['pauses_count'].sum()}")
    st.metric("Pauses / jour", f"{df['pauses_count'].mean():.1f}")
    st.metric("Durée moyenne", f"{df['pauses_total'].mean():.0f}min")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["date"].tail(30).iloc[::-1],
        y=df["pauses_count"].tail(30).iloc[::-1],
        name="Nombre de pauses",
        marker_color=colors["success"]
    ))
    fig.add_trace(go.Scatter(
        x=df["date"].tail(30).iloc[::-1],
        y=df["pauses_total"].tail(30).iloc[::-1]/10,
        name="Durée (x10 min)",
        yaxis="y2",
        line=dict(color=colors["warning"], width=2),
        mode='lines+markers'
    ))
    fig.update_layout(
        yaxis=dict(title="Nombre de pauses"),
        yaxis2=dict(title="Durée (x10 min)", overlaying="y", side="right"),
        plot_bgcolor=colors["bg_light"],
        paper_bgcolor="white",
        font=dict(color=colors["text_dark"])
    )
    st.plotly_chart(fig, use_container_width=True)

# Sommeil
elif page == "Sommeil":
    st.title("Sommeil & Bien-être")
    st.metric("Sommeil moyen", f"{df['sommeil_duree'].mean():.1f}h")
    st.metric("Énergie moyenne", f"{df['energie'].mean():.1f}/5")
    st.metric("Charge mentale moyenne", f"{df['charge_mentale'].mean():.1f}/5")
    
    fig_sleep = px.line(df.tail(30).iloc[::-1], x="date", y="sommeil_duree",
                        markers=True, color_discrete_sequence=[colors["primary"]])
    st.plotly_chart(fig_sleep, use_container_width=True)

# Score
elif page == "Score":
    st.title("Score de Productivité")
    st.metric("Score moyen", f"{df['score'].mean():.1f}")
    st.metric("Meilleur score", f"{df['score'].max():.0f}")
    st.metric("Plus bas score", f"{df['score'].min():.0f}")
    
    fig_score = px.line(df.iloc[::-1], x="date", y="score",
                        markers=True, color_discrete_sequence=[colors["primary"]])
    st.plotly_chart(fig_score, use_container_width=True)
