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
# CSS personnalisé pour style moderne
# -------------------------------
st.markdown(f"""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {colors["bg_light"]};
        padding: 2rem 1rem;
    }}

    /* Metrics styling */
    [data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 600;
        color: {colors["text_dark"]};
    }}

    /* Cards styling */
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

    /* Header styling */
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

    /* Profile section */
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

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Fichier de données
# -------------------------------
DATA_FILE = "data.csv"


def load_data():
    """Charge les données depuis le fichier CSV"""
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, parse_dates=["date"])
            return df
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier CSV : {e}")
            return pd.DataFrame()
    else:
        st.error(f"❌ Le fichier '{DATA_FILE}' est introuvable dans le dossier actuel.")
        st.info("📝 Assurez-vous que le fichier 'habit_data.csv' est présent dans le même dossier que ce script.")
        return pd.DataFrame()


def calculate_score(row):
    """Calcule le score de productivité basé sur les habitudes"""
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

# Vérifier si le DataFrame est vide
if df.empty:
    st.warning("⚠️ Aucune donnée à afficher. Veuillez vérifier votre fichier CSV.")
    st.stop()

# Calculer le score si absent
if "score" not in df.columns:
    df["score"] = df.apply(calculate_score, axis=1)

# Trier par date décroissante
df = df.sort_values("date", ascending=False)

# -------------------------------
# Sidebar avec profil et navigation
# -------------------------------
with st.sidebar:
    # Profil utilisateur
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

    # Navigation
    page = st.radio("Navigation", [
        "📊 Résumé",
        "📋 Missions",
        "💡 Deep Work",
        "☕ Pauses",
        "😴 Sommeil",
        "🏆 Score"
    ], label_visibility="collapsed")

    st.markdown("---")

    # Statistiques rapides sidebar
    st.markdown("### 📈 Stats Rapides")
    recent_score = df.iloc[0]["score"] if not df.empty else 0
    st.metric("Score du jour", f"{recent_score:.1f}",
              f"{recent_score - df.iloc[1]['score']:.1f}" if len(df) > 1 else "0")

    avg_sleep = df["sommeil_duree"].mean()
    st.metric("Sommeil moyen", f"{avg_sleep:.1f}h")

    total_deepwork = df["deep_work_total"].sum() / 60
    st.metric("Deep Work total", f"{total_deepwork:.0f}h")

# -------------------------------
# Page : Résumé
# -------------------------------
if page == "📊 Résumé":
    # Header avec balance
    st.markdown(f"""
    <div class="dashboard-header">
        <div style="font-size: 1rem; color: {colors["text_light"]}; margin-bottom: 0.5rem;">
            Score de productivité global
        </div>
        <div class="balance-display">
            {df["score"].mean():.1f} / 100
        </div>
        <div style="font-size: 0.9rem; color: {colors["text_light"]}; margin-top: 0.5rem;">
            Basé sur {len(df)} jours de suivi
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_missions = df["missions_terminees"].mean()
        st.metric("Missions / jour", f"{avg_missions:.1f}",
                  f"{df.iloc[0]['missions_terminees'] - avg_missions:.1f}")

    with col2:
        avg_deepwork = df["deep_work_total"].mean() / 60
        st.metric("Deep Work / jour", f"{avg_deepwork:.1f}h",
                  f"{(df.iloc[0]['deep_work_total'] / 60) - avg_deepwork:.1f}h")

    with col3:
        avg_sleep = df["sommeil_duree"].mean()
        st.metric("Sommeil moyen", f"{avg_sleep:.1f}h",
                  f"{df.iloc[0]['sommeil_duree'] - avg_sleep:.1f}h")

    with col4:
        avg_energy = df["energie"].mean()
        st.metric("Énergie moyenne", f"{avg_energy:.1f}/5",
                  f"{df.iloc[0]['energie'] - avg_energy:.1f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Graphiques
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Graphique d'évolution du score
        fig_score = go.Figure()
        fig_score.add_trace(go.Scatter(
            x=df["date"].iloc[::-1],
            y=df["score"].iloc[::-1],
            mode='lines+markers',
            name='Score',
            line=dict(color=colors["primary"], width=3),
            marker=dict(size=8, color=colors["primary"]),
            fill='tozeroy',
            fillcolor=f'rgba(113, 196, 239, 0.1)'
        ))

        fig_score.update_layout(
            title="Évolution du Score de Productivité",
            xaxis_title="Date",
            yaxis_title="Score",
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"]),
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig_score, use_container_width=True)

    with col_right:
        # Activités récentes
        st.markdown("### 📅 Activité Récente")

        for i in range(min(5, len(df))):
            row = df.iloc[i]
            date_str = row["date"].strftime("%d %b")

            st.markdown(f"""
            <div class="income-item">
                <div>
                    <div style="font-weight: 600; color: {colors["text_dark"]};">{date_str}</div>
                    <div style="font-size: 0.85rem; color: {colors["text_light"]};">
                        {row['missions_terminees']} missions • {row['deep_work_sessions']} sessions
                    </div>
                </div>
                <div class="income-positive">
                    {row['score']:.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Statistiques détaillées
    st.markdown("### 📊 Statistiques Détaillées")

    col1, col2 = st.columns(2)

    with col1:
        # Répartition des missions
        fig_missions = go.Figure(data=[
            go.Bar(
                x=df["date"].iloc[::-1].tail(14),
                y=df["missions_terminees"].iloc[::-1].tail(14),
                marker_color=colors["primary"],
                name="Missions"
            )
        ])

        fig_missions.update_layout(
            title="Missions Terminées (14 derniers jours)",
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"]),
            height=300
        )

        st.plotly_chart(fig_missions, use_container_width=True)

    with col2:
        # Énergie vs Charge mentale
        fig_energy = go.Figure()

        fig_energy.add_trace(go.Scatter(
            x=df["date"].iloc[::-1].tail(14),
            y=df["energie"].iloc[::-1].tail(14),
            mode='lines+markers',
            name='Énergie',
            line=dict(color=colors["success"], width=2)
        ))

        fig_energy.add_trace(go.Scatter(
            x=df["date"].iloc[::-1].tail(14),
            y=df["charge_mentale"].iloc[::-1].tail(14),
            mode='lines+markers',
            name='Charge mentale',
            line=dict(color=colors["danger"], width=2)
        ))

        fig_energy.update_layout(
            title="Énergie vs Charge Mentale",
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"]),
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig_energy, use_container_width=True)

# -------------------------------
# Page : Missions
# -------------------------------
elif page == "📋 Missions":
    st.title("📋 Missions")

    col1, col2, col3 = st.columns(3)
    with col1:
        total_missions = df["missions_terminees"].sum()
        st.metric("Total Missions", f"{total_missions}")
    with col2:
        avg_missions = df["missions_terminees"].mean()
        st.metric("Moyenne / jour", f"{avg_missions:.1f}")
    with col3:
        best_day = df.loc[df["missions_terminees"].idxmax()]
        st.metric("Meilleur jour", f"{best_day['missions_terminees']}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Graphique
    fig = px.bar(df.tail(30).iloc[::-1], x="date", y="missions_terminees",
                 title="Missions terminées (30 derniers jours)",
                 color_discrete_sequence=[colors["primary"]])
    fig.update_layout(
        plot_bgcolor=colors["bg_light"],
        paper_bgcolor="white",
        font=dict(color=colors["text_dark"])
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tableau
    st.markdown("### 📋 Détail des Missions")
    display_df = df[["date", "missions_terminees"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df.columns = ["Date", "Missions Terminées"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# -------------------------------
# Page : Deep Work
# -------------------------------
elif page == "💡 Deep Work":
    st.title("💡 Deep Work")

    col1, col2, col3 = st.columns(3)
    with col1:
        total_hours = df["deep_work_total"].sum() / 60
        st.metric("Total Heures", f"{total_hours:.0f}h")
    with col2:
        avg_sessions = df["deep_work_sessions"].mean()
        st.metric("Sessions / jour", f"{avg_sessions:.1f}")
    with col3:
        avg_duration = df["deep_work_total"].mean() / df["deep_work_sessions"].mean()
        st.metric("Durée moy. session", f"{avg_duration:.0f}min")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(df.tail(30).iloc[::-1], x="date", y="deep_work_sessions",
                     title="Nombre de sessions",
                     color_discrete_sequence=[colors["accent"]])
        fig.update_layout(
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.line(df.tail(30).iloc[::-1], x="date", y="deep_work_total",
                      title="Durée totale (minutes)",
                      markers=True,
                      color_discrete_sequence=[colors["primary"]])
        fig.update_layout(
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"])
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau
    st.markdown("### 📊 Détail Deep Work")
    display_df = df[["date", "deep_work_sessions", "deep_work_total"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df["deep_work_total"] = (display_df["deep_work_total"] / 60).round(2)
    display_df.columns = ["Date", "Sessions", "Durée (h)"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# -------------------------------
# Page : Pauses
# -------------------------------
elif page == "☕ Pauses":
    st.title("☕ Pauses")

    col1, col2, col3 = st.columns(3)
    with col1:
        total_pauses = df["pauses_count"].sum()
        st.metric("Total Pauses", f"{total_pauses}")
    with col2:
        avg_pauses = df["pauses_count"].mean()
        st.metric("Pauses / jour", f"{avg_pauses:.1f}")
    with col3:
        avg_duration = df["pauses_total"].mean()
        st.metric("Durée moy. totale", f"{avg_duration:.0f}min")

    st.markdown("<br>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["date"].tail(30).iloc[::-1],
        y=df["pauses_count"].tail(30).iloc[::-1],
        name="Nombre de pauses",
        marker_color=colors["success"]
    ))

    fig.add_trace(go.Scatter(
        x=df["date"].tail(30).iloc[::-1],
        y=df["pauses_total"].tail(30).iloc[::-1] / 10,
        name="Durée totale (x10 min)",
        yaxis="y2",
        line=dict(color=colors["warning"], width=2),
        mode='lines+markers'
    ))

    fig.update_layout(
        title="Pauses - Nombre et Durée",
        yaxis=dict(title="Nombre de pauses"),
        yaxis2=dict(title="Durée (x10 min)", overlaying="y", side="right"),
        plot_bgcolor=colors["bg_light"],
        paper_bgcolor="white",
        font=dict(color=colors["text_dark"]),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tableau
    st.markdown("### 📊 Détail Pauses")
    display_df = df[["date", "pauses_count", "pauses_total"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df.columns = ["Date", "Nombre", "Durée (min)"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# -------------------------------
# Page : Sommeil
# -------------------------------
elif page == "😴 Sommeil":
    st.title("😴 Sommeil & Bien-être")

    col1, col2, col3 = st.columns(3)
    with col1:
        avg_sleep = df["sommeil_duree"].mean()
        st.metric("Sommeil moyen", f"{avg_sleep:.1f}h")
    with col2:
        avg_energy = df["energie"].mean()
        st.metric("Énergie moyenne", f"{avg_energy:.1f}/5")
    with col3:
        avg_mental = df["charge_mentale"].mean()
        st.metric("Charge mentale moy.", f"{avg_mental:.1f}/5")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(df.tail(30).iloc[::-1], x="date", y="sommeil_duree",
                      title="Durée du sommeil",
                      markers=True,
                      color_discrete_sequence=[colors["primary"]])
        fig.add_hline(y=7.5, line_dash="dash", line_color="red",
                      annotation_text="Objectif: 7.5h")
        fig.update_layout(
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["date"].tail(30).iloc[::-1],
            y=df["energie"].tail(30).iloc[::-1],
            mode='lines+markers',
            name='Énergie',
            line=dict(color=colors["success"], width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df["date"].tail(30).iloc[::-1],
            y=df["charge_mentale"].tail(30).iloc[::-1],
            mode='lines+markers',
            name='Charge mentale',
            line=dict(color=colors["danger"], width=2)
        ))
        fig.update_layout(
            title="Énergie vs Charge Mentale",
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"]),
            legend=dict(orientation="h")
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tableau
    st.markdown("### 📊 Détail Sommeil")
    display_df = df[["date", "sommeil_duree", "energie", "charge_mentale"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df.columns = ["Date", "Sommeil (h)", "Énergie", "Charge Mentale"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# -------------------------------
# Page : Score
# -------------------------------
elif page == "🏆 Score":
    st.title("🏆 Score de Productivité")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_score = df["score"].mean()
        st.metric("Score moyen", f"{avg_score:.1f}")
    with col2:
        max_score = df["score"].max()
        st.metric("Meilleur score", f"{max_score:.0f}")
    with col3:
        min_score = df["score"].min()
        st.metric("Plus bas score", f"{min_score:.0f}")
    with col4:
        current_score = df.iloc[0]["score"]
        st.metric("Score actuel", f"{current_score:.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Graphique principal
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"].iloc[::-1],
        y=df["score"].iloc[::-1],
        mode='lines+markers',
        name='Score',
        line=dict(color=colors["primary"], width=3),
        marker=dict(size=8, color=colors["primary"]),
        fill='tozeroy',
        fillcolor=f'rgba(113, 196, 239, 0.2)'
    ))

    fig.add_hline(y=avg_score, line_dash="dash", line_color=colors["text_light"],
                  annotation_text=f"Moyenne: {avg_score:.1f}")

    fig.update_layout(
        title="Évolution du Score de Productivité",
        xaxis_title="Date",
        yaxis_title="Score",
        plot_bgcolor=colors["bg_light"],
        paper_bgcolor="white",
        font=dict(color=colors["text_dark"]),
        hovermode='x unified',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Distribution des scores
    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(df, x="score", nbins=20,
                                title="Distribution des scores",
                                color_discrete_sequence=[colors["accent"]])
        fig_hist.update_layout(
            plot_bgcolor=colors["bg_light"],
            paper_bgcolor="white",
            font=dict(color=colors["text_dark"])
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # Tableau des meilleurs jours
        st.markdown("### 🏅 Top 10 Meilleurs Jours")
        top_days = df.nlargest(10, "score")[["date", "score"]].copy()
        top_days["date"] = top_days["date"].dt.strftime("%d/%m/%Y")
        top_days.columns = ["Date", "Score"]
        st.dataframe(top_days, use_container_width=True, hide_index=True)
