# 📊 Habit Tracker Dashboard

Un tableau de bord interactif moderne pour suivre vos habitudes de travail quotidiennes et analyser votre productivité.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Objectif

Permettre aux utilisateurs de suivre leurs habitudes quotidiennes de travail, visualiser leur progression sur un dashboard interactif et analyser leur efficacité de manière structurée.

## ✨ Fonctionnalités Principales

### 📈 Suivi des Habitudes
- **Missions** : Suivi des tâches accomplies quotidiennement
- **Deep Work** : Nombre de sessions et durée totale de travail concentré
- **Pauses** : Gestion et suivi des temps de repos
- **Interruptions** : Analyse du temps subi et des perturbations
- **Sommeil** : Durée et qualité perçue
- **Bien-être** : Énergie perçue et charge mentale

### 🎨 Dashboard Interactif
- **Vue Résumé** : Aperçu global avec métriques clés et graphiques d'évolution
- **Pages dédiées** : Analyse détaillée pour chaque catégorie d'habitudes
- **Graphiques interactifs** : Visualisations dynamiques avec Plotly
- **Statistiques en temps réel** : Moyennes, tendances et comparaisons

### 🏆 Score de Productivité
Calcul automatique basé sur :
- Missions accomplies
- Sessions de Deep Work
- Qualité des pauses
- Interruptions subies
- Qualité du sommeil
- Énergie et charge mentale

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. **Clonez le repository**
```bash
git clone https://github.com/votre-username/habit-tracker-dashboard.git
cd habit-tracker-dashboard
```

2. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

3. **Préparez vos données**
   
   Créez un fichier `habit_data.csv` avec les colonnes suivantes :
   - `date` : Date au format YYYY-MM-DD
   - `missions_terminees` : Nombre de missions terminées (int)
   - `deep_work_sessions` : Nombre de sessions deep work (int)
   - `deep_work_total` : Durée totale en minutes (int)
   - `pauses_count` : Nombre de pauses (int)
   - `pauses_total` : Durée totale des pauses en minutes (int)
   - `interruptions_count` : Nombre d'interruptions (int)
   - `interruptions_total` : Durée totale des interruptions en minutes (int)
   - `sommeil_duree` : Durée du sommeil en heures (float)
   - `energie` : Niveau d'énergie perçue (1-5, int)
   - `charge_mentale` : Charge mentale perçue (1-5, int)

4. **Lancez l'application**
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📁 Structure du Projet

```
habit-tracker-dashboard/
│
├── app.py                  # Application principale Streamlit
├── habit_data.csv          # Fichier de données (à créer)
├── requirements.txt        # Dépendances Python
└── README.md              # Documentation
```

## 📊 Exemple de Fichier CSV

```csv
date,missions_terminees,deep_work_sessions,deep_work_total,pauses_count,pauses_total,interruptions_count,interruptions_total,sommeil_duree,energie,charge_mentale
2024-01-01,3,4,240,5,75,2,30,7.5,4,3
2024-01-02,2,3,180,4,60,3,45,7.0,3,4
2024-01-03,4,5,300,6,90,1,15,8.0,5,2
```

## 🎨 Aperçu du Design

Le dashboard utilise une palette de couleurs moderne inspirée des meilleures pratiques UI/UX :
- **Bleu clair** (#d4eaf7) : Fond des cartes principales
- **Bleu primaire** (#71c4ef) : Éléments interactifs et graphiques
- **Bleu foncé** (#00668c) : Accents et navigation
- **Gris clair** (#f8f9fa) : Arrière-plans
- **Blanc** : Cartes et conteneurs

## 📈 Calcul du Score

Le score de productivité est calculé selon la formule :

```python
score = (missions × 10) + 
        (deep_work_minutes / 12) - 
        (interruptions_minutes / 6) + 
        (pauses_minutes / 15) + 
        (energie × 3) - 
        (charge_mentale × 2)
```

Le score est normalisé entre 0 et 100.

## 🛠️ Technologies Utilisées

- **Python 3.8+** : Langage de programmation
- **Streamlit** : Framework pour l'interface utilisateur
- **Pandas** : Manipulation et analyse des données
- **Plotly** : Visualisations interactives
- **NumPy** : Calculs numériques

## 🔮 Évolutions Futures

- [ ] Intégration avec l'API Notion pour synchronisation automatique
- [ ] Export des rapports en PDF
- [ ] Système de rappels et notifications
- [ ] Vue Kanban pour les missions
- [ ] Matrice d'Eisenhower interactive
- [ ] Prédictions et recommandations basées sur l'IA
- [ ] Mode multi-utilisateurs avec authentification
- [ ] Graphiques comparatifs avec d'autres périodes

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

Créé avec ❤️ pour améliorer la productivité quotidienne

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile sur GitHub !
