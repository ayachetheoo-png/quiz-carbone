#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz Empreinte Carbone — Version Web (Streamlit)
Facteurs d'émission : ADEME Base Carbone®
"""

import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Quiz Empreinte Carbone",
    page_icon="🌍",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────────────────────
# FACTEURS D'ÉMISSION (ADEME Base Carbone®)
# Chaque dictionnaire associe un choix lisible à sa valeur d'émission.
# ─────────────────────────────────────────────────────────────────────────────

MOYENNE_FRANCAISE = 9.9   # tCO2e/an — ADEME 2023
OBJECTIF_PARIS    = 2.0   # tCO2e/an — Accords de Paris

# Facteurs par type de voiture (kgCO2e/km)
VOITURE = {
    "Aucune voiture":                         0.000,
    "Essence (ex : Peugeot 208)":            0.218,
    "Diesel (ex : Golf diesel)":             0.195,
    "Hybride (ex : Toyota Yaris)":           0.135,
    "Électrique (ex : Renault Zoé)":         0.027,
    "GPL":                                   0.183,
}

# Consommation estimée selon l'isolation (kWh/m²/an)
ISOLATION = {
    "Très bien isolé (BBC, passif, construction récente)": 80,
    "Bien isolé (après 1975, double vitrage)":            150,
    "Moyennement isolé (1950–1975)":                      220,
    "Mal isolé (avant 1950, simple vitrage)":             350,
}

# Facteurs par mode de chauffage (kgCO2e/kWh)
CHAUFFAGE = {
    "Électricité (radiateurs électriques)": 0.052,
    "Gaz naturel":                          0.227,
    "Fioul domestique":                     0.324,
    "Pompe à chaleur":                      0.017,
    "Bois / granulés":                      0.032,
    "Réseau de chaleur urbain":             0.110,
}

# Émissions par régime alimentaire (kgCO2e/an)
REGIME = {
    "Végétalien / vegan":                         1600,
    "Végétarien (œufs, laitages, pas de viande)": 2000,
    "Flexitarien (viande 1–2 fois/semaine)":       2500,
    "Omnivore (viande 3–5 fois/semaine)":          3000,
    "Gros consommateur (viande chaque jour)":      3500,
}

# Gaspillage alimentaire (kgCO2e/an)
GASPILLAGE = {
    "Minimal — je planifie, peu de déchets":          50,
    "Moyen — dans la moyenne française (~29 kg/an)": 150,
    "Élevé — je jette souvent":                      300,
}

# Origine des aliments (delta kgCO2e/an, peut être négatif)
ORIGINE = {
    "Essentiellement local et de saison":    -200,
    "Mixte (parfois local, parfois importé)":   0,
    "Souvent importé ou hors saison":         300,
}

# Vêtements (kgCO2e/an)
HABITS = {
    "Seconde main uniquement (Vinted, friperies...)":   50,
    "Peu d'achats neufs (< 5 pièces/an)":             100,
    "Modéré (10–15 pièces neuves/an)":                300,
    "Régulier (20–30 pièces/an, fast fashion...)":    600,
    "Très consommateur (> 30 pièces/an)":            1000,
}

# Usage numérique (kgCO2e/an)
NUMERIQUE = {
    "Minimal (peu de streaming, pas de cloud)":    50,
    "Modéré (streaming SD/HD, quelques h/jour)":  150,
    "Intensif (streaming 4K, gaming en ligne...)": 300,
}

# Achats divers (kgCO2e/an)
ACHATS_DIVERS = {
    "Très sobre — uniquement l'essentiel":        200,
    "Modéré — quelques achats plaisir par an":    600,
    "Régulier — nombreux achats variés":         1200,
    "Très consommateur":                         2000,
}

# ─────────────────────────────────────────────────────────────────────────────
# CSS PERSONNALISÉ — style de la page
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Fond général de l'application */
    .stApp { background-color: #f4f9f4; }

    /* Bannière d'en-tête verte */
    .quiz-header {
        background: linear-gradient(135deg, #1b5e20, #388e3c);
        color: white;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 20px;
    }
    .quiz-header h1 { color: white; margin: 0 0 6px 0; font-size: 2rem; }
    .quiz-header p  { color: #c8e6c9; margin: 0; font-size: 1rem; }

    /* Carte de conseil (bordure verte à gauche) */
    .conseil {
        background: #f1f8e9;
        border-left: 4px solid #33691e;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin: 6px 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Bannière de résultat colorée selon le score */
    .banniere {
        border-radius: 12px;
        padding: 18px 22px;
        margin: 16px 0;
        font-size: 1.05rem;
        font-weight: 600;
        line-height: 1.6;
    }
    .banniere-vert  { background:#e8f5e9; color:#1b5e20; border:1.5px solid #a5d6a7; }
    .banniere-jaune { background:#fff8e1; color:#e65100; border:1.5px solid #ffe082; }
    .banniere-rouge { background:#ffebee; color:#b71c1c; border:1.5px solid #ef9a9a; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# EN-TÊTE
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="quiz-header">
    <h1>🌍 Quiz Empreinte Carbone</h1>
    <p>Estimez votre impact climatique annuel en quelques minutes — Facteurs ADEME Base Carbone®</p>
</div>
""", unsafe_allow_html=True)

col_ref1, col_ref2 = st.columns(2)
col_ref1.info(f"🇫🇷 Moyenne française : **{MOYENNE_FRANCAISE} tCO2e/an**")
col_ref2.success(f"🎯 Objectif Accords de Paris : **{OBJECTIF_PARIS} tCO2e/an**")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# QUESTIONS — 4 ONGLETS
# ─────────────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs(["🚗 Transport", "🏠 Logement", "🍽️ Alimentation", "🛒 Consommation"])

# ── Onglet 1 : Transport ──────────────────────────────────────────────────────
with tab1:
    st.markdown("### 🚗 Voiture personnelle")

    type_voiture = st.selectbox("Type de carburant", list(VOITURE.keys()), key="type_voiture")

    # Le slider des km n'apparaît que si l'utilisateur a une voiture
    km_voiture = 0
    if type_voiture != "Aucune voiture":
        km_voiture = st.slider(
            "Kilomètres parcourus par an", 0, 60000, 12000, step=500,
            key="km_voiture",
            help="Total annuel tous trajets confondus (domicile-travail, vacances...)"
        )

    st.markdown("---")
    st.markdown("### 🚌 Transports en commun")
    km_bus   = st.slider("Bus — km/an",                 0, 20000, 0, step=100, key="km_bus")
    km_train = st.slider("Train (TGV, TER...) — km/an", 0, 50000, 0, step=100, key="km_train")
    km_metro = st.slider("Métro / tramway — km/an",     0, 15000, 0, step=100, key="km_metro")

    st.markdown("---")
    st.markdown("### ✈️ Avion _(entrez le total aller-retour)_")
    st.caption("Paris–Marseille ≈ 750 km A/R | Paris–New York ≈ 11 800 km A/R")
    km_avion_court = st.slider("Court-courrier < 3h (Europe) — km/an",        0, 30000, 0, step=100, key="km_avion_court")
    km_avion_long  = st.slider("Long-courrier > 3h (intercontinental) — km/an", 0, 80000, 0, step=500, key="km_avion_long")

# ── Onglet 2 : Logement ───────────────────────────────────────────────────────
with tab2:
    st.markdown("### 🏠 Caractéristiques du logement")

    surface       = st.slider("Surface (m²)", 5, 300, 70, key="surface")
    nb_personnes  = st.number_input(
        "Personnes dans le logement",
        min_value=1, max_value=15, value=1, key="nb_personnes",
        help="Les émissions du logement sont divisées entre les occupants"
    )
    isolation      = st.selectbox("Niveau d'isolation", list(ISOLATION.keys()), index=1, key="isolation")
    type_chauffage = st.selectbox("Mode de chauffage principal", list(CHAUFFAGE.keys()), key="type_chauffage")

    # Estimation automatique de la consommation selon la surface et l'isolation
    conso_estimee = int(surface * ISOLATION[isolation])
    st.caption(f"Consommation estimée d'après votre isolation : **{conso_estimee} kWh/an**")
    conso = st.number_input(
        "Consommation annuelle réelle (kWh/an) — visible sur vos factures",
        min_value=0, max_value=150000, value=conso_estimee, step=100, key="conso"
    )

# ── Onglet 3 : Alimentation ───────────────────────────────────────────────────
with tab3:
    st.markdown("### 🍽️ Vos habitudes alimentaires")

    regime     = st.selectbox("Régime alimentaire",        list(REGIME.keys()),     index=3, key="regime")
    gaspillage = st.selectbox("Niveau de gaspillage",      list(GASPILLAGE.keys()), index=1, key="gaspillage")
    origine    = st.selectbox("Origine de vos aliments",   list(ORIGINE.keys()),    index=1, key="origine")

    st.info("💡 1 kg de bœuf ≈ 27 kg CO2e. Réduire la viande rouge est le geste alimentaire le plus efficace.")

# ── Onglet 4 : Consommation ───────────────────────────────────────────────────
with tab4:
    st.markdown("### 👕 Vêtements & textile")
    habits = st.selectbox("Habitudes d'achat vestimentaire", list(HABITS.keys()), index=2, key="habits")

    st.markdown("### 📱 Équipements électroniques _(achetés cette année)_")
    col_e1, col_e2, col_e3 = st.columns(3)
    nb_smartphones = col_e1.number_input("📱 Smartphones", 0, 5, 0, key="smartphones")
    nb_ordis       = col_e2.number_input("💻 Ordinateurs", 0, 3, 0, key="ordis")
    nb_tv          = col_e3.number_input("📺 Télévisions",  0, 3, 0, key="tv")
    st.caption("Smartphone neuf ≈ 70 kg CO2e | Ordinateur ≈ 300 kg | TV ≈ 400 kg")

    st.markdown("### 💻 Usage numérique")
    numerique = st.select_slider(
        "Streaming, cloud, jeux en ligne...",
        options=list(NUMERIQUE.keys()),
        value=list(NUMERIQUE.keys())[1],   # "Modéré" par défaut
        key="numerique"
    )

    st.markdown("### 🛍️ Achats divers _(meubles, sport, bricolage, livres...)_")
    achats_divers = st.selectbox("Volume d'achats divers", list(ACHATS_DIVERS.keys()), index=1, key="achats_divers")

# ─────────────────────────────────────────────────────────────────────────────
# BOUTON DE CALCUL
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
calculer = st.button("🧮 Calculer mon empreinte carbone", use_container_width=True, type="primary")

# ─────────────────────────────────────────────────────────────────────────────
# CALCUL ET AFFICHAGE DES RÉSULTATS
# Le bloc suivant ne s'exécute que si l'utilisateur a cliqué sur le bouton.
# ─────────────────────────────────────────────────────────────────────────────

if calculer:

    # ── Calcul des émissions par poste ────────────────────────────────────────

    # Transport (kgCO2e → tCO2e)
    t_transport = (
        km_voiture      * VOITURE[type_voiture]
        + km_bus        * 0.0297
        + km_train      * 0.00573
        + km_metro      * 0.00329
        + km_avion_court * 0.258
        + km_avion_long  * 0.187 * 2.0   # ×2 pour le forçage radiatif en altitude
    ) / 1000

    # Logement : émissions du chauffage divisées par le nombre d'occupants
    t_logement = (conso * CHAUFFAGE[type_chauffage] / nb_personnes) / 1000

    # Alimentation : régime + gaspillage + origine (peut être négatif)
    t_alimentation = (REGIME[regime] + GASPILLAGE[gaspillage] + ORIGINE[origine]) / 1000

    # Consommation : vêtements + électronique + numérique + achats divers
    t_consommation = (
        HABITS[habits]
        + nb_smartphones * 70    # kgCO2e par smartphone neuf (ADEME)
        + nb_ordis       * 300   # kgCO2e par ordinateur neuf
        + nb_tv          * 400   # kgCO2e par télévision neuve
        + NUMERIQUE[numerique]
        + ACHATS_DIVERS[achats_divers]
    ) / 1000

    total = t_transport + t_logement + t_alimentation + t_consommation

    # ── Métriques de comparaison ──────────────────────────────────────────────
    st.markdown("## 📊 Votre bilan carbone")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌍 Votre empreinte",    f"{total:.1f} t CO₂e/an")
    col2.metric(
        "🇫🇷 Moyenne française", f"{MOYENNE_FRANCAISE} t",
        delta=f"{total - MOYENNE_FRANCAISE:+.1f} t", delta_color="inverse"
    )
    col3.metric(
        "🎯 Objectif Paris",    f"{OBJECTIF_PARIS} t",
        delta=f"{total - OBJECTIF_PARIS:+.1f} t",    delta_color="inverse"
    )

    # ── Graphique en barres horizontales ──────────────────────────────────────
    # Ordre inversé pour que Transport soit en haut
    categories = ["🛒 Consommation", "🍽️ Alimentation", "🏠 Logement", "🚗 Transport"]
    valeurs    = [t_consommation, t_alimentation, t_logement, t_transport]
    couleurs   = ["#ffa726", "#66bb6a", "#42a5f5", "#ef5350"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=valeurs, y=categories,
        orientation="h",
        marker_color=couleurs,
        text=[f"  {v:.2f} t" for v in valeurs],
        textposition="outside",
        cliponaxis=False,
    ))

    # Ligne verticale : moyenne française
    fig.add_vline(
        x=MOYENNE_FRANCAISE, line_dash="dash", line_color="#1565c0", line_width=2,
        annotation_text=f"Moy. FR ({MOYENNE_FRANCAISE} t)",
        annotation_position="top right",
        annotation_font_color="#1565c0",
    )
    # Ligne verticale : objectif Paris
    fig.add_vline(
        x=OBJECTIF_PARIS, line_dash="dash", line_color="#2e7d32", line_width=2,
        annotation_text=f"Objectif Paris ({OBJECTIF_PARIS} t)",
        annotation_position="top left",
        annotation_font_color="#2e7d32",
    )

    x_max = max(max(valeurs) * 1.35, MOYENNE_FRANCAISE * 1.2, 12.0)
    fig.update_layout(
        title=dict(text=f"Répartition — Total : {total:.1f} tCO₂e/an", font_size=14),
        xaxis=dict(title="tCO₂e/an", range=[0, x_max]),
        height=300,
        margin=dict(l=10, r=90, t=50, b=20),
        showlegend=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f4f9f4",
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Message personnalisé selon le score ───────────────────────────────────
    if total <= OBJECTIF_PARIS:
        st.markdown(
            '<div class="banniere banniere-vert">🌍 <strong>Exceptionnel !</strong> '
            "Vous êtes déjà sous l'objectif des Accords de Paris (2 t). "
            "Vous faites partie des Français les moins émetteurs. Bravo !</div>",
            unsafe_allow_html=True
        )
    elif total <= 5.0:
        st.markdown(
            '<div class="banniere banniere-vert">👍 <strong>Bien !</strong> '
            "Votre empreinte est nettement inférieure à la moyenne française. "
            "Quelques ajustements supplémentaires et vous vous rapprochez de l'objectif !</div>",
            unsafe_allow_html=True
        )
    elif total <= MOYENNE_FRANCAISE:
        st.markdown(
            f'<div class="banniere banniere-jaune">⚠️ <strong>Attention !</strong> '
            f"Vous êtes dans la moyenne française ({MOYENNE_FRANCAISE} t) — "
            f"mais c'est encore bien au-dessus de l'objectif Paris (2 t). "
            f"Il reste une marge d'amélioration importante.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="banniere banniere-rouge">🚨 <strong>Alerte !</strong> '
            f"Votre empreinte dépasse la moyenne française ({MOYENNE_FRANCAISE} t). "
            f"Des changements significatifs sont nécessaires.</div>",
            unsafe_allow_html=True
        )

    # Affichage de la réduction nécessaire pour atteindre l'objectif Paris
    reduction = max(0.0, total - OBJECTIF_PARIS)
    if reduction > 0:
        pct = (reduction / total * 100) if total > 0 else 0
        st.markdown(
            f"Pour atteindre l'objectif Paris, il faudrait réduire de "
            f"**{reduction:.1f} tCO₂e/an** (soit −{pct:.0f}% de votre empreinte actuelle)."
        )

    # ── Conseils personnalisés ─────────────────────────────────────────────────
    st.markdown("## 💡 Conseils personnalisés")

    # On identifie les 2 postes les plus émetteurs pour cibler les conseils
    postes = {
        "Transport":    t_transport,
        "Logement":     t_logement,
        "Alimentation": t_alimentation,
        "Consommation": t_consommation,
    }
    postes_tries = sorted(postes.items(), key=lambda x: x[1], reverse=True)

    # Banque de conseils par poste
    banque_conseils = {
        "Transport": [
            "🚲 Remplacez 2 trajets/semaine en voiture par le vélo ou la marche.",
            "🚆 Le train émet 45× moins que l'avion : privilégiez-le pour les trajets < 4h.",
            "🚗 Le covoiturage divise vos émissions par le nombre de passagers.",
            "✈️ Un A/R Paris–New York équivaut à 1,5 an de trajets domicile-travail.",
            "⚡ Votre prochain véhicule : envisagez l'électrique ou le vélo cargo.",
        ],
        "Logement": [
            "🌡️ Baisser le chauffage de 1 °C réduit la facture (et les émissions) de 7 %.",
            "🪟 L'isolation est l'investissement le plus rentable : combles, double vitrage.",
            "🔌 Passez à un fournisseur d'électricité verte (Enercoop, Ilek...).",
            "🚿 2 minutes de moins sous la douche = 12 kg CO₂ et 20 € économisés/an.",
            "💡 Les ampoules LED consomment 5× moins que les halogènes.",
        ],
        "Alimentation": [
            "🥩 Réduire la viande rouge est le geste alimentaire le plus efficace.",
            "🐟 2 fois/semaine, remplacez la viande par des légumineuses ou du poisson.",
            "🌱 Préférez les produits de saison : des tomates en hiver viennent du Maroc.",
            "🛒 Planifiez vos repas pour réduire le gaspillage (liste de courses, congélateur).",
            "🧀 Les produits laitiers ont un impact souvent sous-estimé : modérez les quantités.",
        ],
        "Consommation": [
            "📱 Garder son smartphone 1 an de plus évite ~70 kgCO₂e de fabrication.",
            "👕 Achetez d'occasion (Vinted, friperies, Leboncoin) plutôt que neuf.",
            "🔧 Faites réparer plutôt que remplacer (Repair Café, ressourceries).",
            "📦 Évitez la livraison express : elle multiplie les camionnettes en ville.",
            "🎮 Le streaming 4K consomme 3× plus que le HD : réglez la qualité vidéo.",
        ],
    }

    emojis_postes = {
        "Transport":    "🚗",
        "Logement":     "🏠",
        "Alimentation": "🍽️",
        "Consommation": "🛒",
    }

    # Affichage des conseils pour les 2 postes les plus émetteurs
    for rang, (poste, valeur) in enumerate(postes_tries[:2], start=1):
        with st.expander(
            f"Priorité n°{rang} — {emojis_postes[poste]} {poste} ({valeur:.2f} tCO₂e/an)",
            expanded=True
        ):
            for conseil in banque_conseils[poste]:
                st.markdown(f'<div class="conseil">{conseil}</div>', unsafe_allow_html=True)

    # ── Ressources ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📚 Pour aller plus loin")
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.markdown("🌐 **[nosgestesclimat.fr](https://nosgestesclimat.fr)**\nSimulateur complet ADEME")
    col_r2.markdown("🃏 **[fresqueduclimat.org](https://fresqueduclimat.org)**\nAtelier collaboratif 3h")
    col_r3.markdown("📖 **[agirpourlatransition.ademe.fr](https://agirpourlatransition.ademe.fr)**\nGuide ADEME")

# ─────────────────────────────────────────────────────────────────────────────
# PIED DE PAGE
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption(
    "Facteurs d'émission : ADEME Base Carbone® | "
    "Moyenne française : ADEME 2023 | "
    "Objectif Paris : GIEC 2018"
)
