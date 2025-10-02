# Movie Review Recommender

Système de recommandation de critiques de films basé sur la similarité de contenu (Content-Based Filtering).

## 📋 Description

Ce projet implémente un moteur de recommandation qui identifie les critiques similaires à partir d'une critique source. Le système utilise la vectorisation TF-IDF et la similarité cosinus pour trouver les critiques les plus proches sémantiquement.

**Cas d'usage** : Sur une plateforme comme SensCritique, lorsqu'un utilisateur lit une critique (ex : un avis négatif sur Fight Club à cause des scènes de violence), le système suggère automatiquement d'autres critiques similaires sur le même film.

## 🛠️ Architecture Technique

### Pipeline de Traitement

1. **Prétraitement du texte**
   - Suppression des balises HTML et URLs
   - Normalisation (minuscules, suppression des accents)
   - Élimination de la ponctuation et chiffres
   - Filtrage par longueur minimale (50 caractères)

2. **Vectorisation TF-IDF**
   - Extraction de caractéristiques avec n-grams (1,2)
   - Max features : 50 000
   - Min document frequency : 2

3. **Calcul de similarité**
   - Similarité cosinus entre vecteurs TF-IDF
   - Optimisation avec `argpartition` (O(n) au lieu de O(n log n))
   - Filtrage par score minimal (seuil : 0.10)

### Choix Techniques

- **Python 3** : Écosystème riche en librairies ML/NLP
- **scikit-learn** : Implémentation robuste et optimisée de TF-IDF
- **pandas** : Manipulation efficace de datasets CSV volumineux
- **numpy** : Calculs vectoriels optimisés pour les grandes matrices

## 🚀 Installation

### Option 1 : Nix Shell (recommandé)

```bash
nix-shell
```

### Option 2 : Environment virtuel Python

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## 📖 Usage

### Interface CLI

```bash
python src/main.py <chemin_csv> <id_critique> [top_k]
```

**Paramètres :**
- `chemin_csv` : Chemin vers le fichier CSV des critiques
- `id_critique` : ID de la critique source
- `top_k` (optionnel) : Nombre de recommandations à retourner (défaut : 5)

### Exemples

```bash
# Recommander 5 critiques similaires sur Fight Club
python src/main.py data/fightclub_critique.csv 20761 5

# Recommander 10 critiques similaires sur Interstellar
python src/main.py data/interstellar_critique.csv 25246858 10
```

### Exemple de sortie

```
Top 5 critiques similaires à 20761:
  1. ID   21701678  |  Score: 0.595
  2. ID   41298149  |  Score: 0.544
  3. ID  298420055  |  Score: 0.537
  4. ID   16685573  |  Score: 0.494
  5. ID   93289512  |  Score: 0.489
```

## 📊 Format des Données

Les fichiers CSV doivent contenir les colonnes suivantes :
- `id` : Identifiant unique de la critique
- `review_title` : Titre de la critique
- `review_content` : Contenu textuel de la critique

## 🔧 API Programmatique

```python
from recommender import Recommandeur

# Initialisation
recommandeur = Recommandeur("data/fightclub_critique.csv")

# Recherche de critiques similaires
resultats = recommandeur.recommander(
    id_critique=20761,
    top_k=5,
    score_min=0.10
)

# Résultat : [(id_critique, score_similarite), ...]
```

## 📁 Structure du Projet

```
movie-review-recommender/
├── src/
│   ├── recommender.py    # Moteur de recommandation (classe principale)
│   └── main.py           # Interface CLI
├── data/
│   ├── fightclub_critique.csv
│   └── interstellar_critique.csv
├── requirements.txt      # Dépendances Python
├── shell.nix            # Configuration Nix
├── consigne.md          # Énoncé du test technique
└── README.md            # Documentation
```

## ⚡ Optimisations

- **argpartition** : Algorithme O(n) pour extraire les top-k éléments (vs O(n log n) pour un tri complet)
- **Filtrage précoce** : Élimination des critiques trop courtes avant vectorisation
- **Buffer de recherche** : Récupération de top_k+20 candidats pour garantir top_k résultats après filtrage

## 🔮 Évolutions Possibles

### Court terme
- Ajout de tests unitaires (pytest)
- Support de plusieurs films dans un seul dataset
- Export des résultats (JSON, CSV)
- API REST avec FastAPI

### Long terme
- Indexation vectorielle avec FAISS pour datasets massifs (>1M critiques)
- Fine-tuning d'embeddings contextuels (Sentence-BERT, CamemBERT)
- Pipeline de recommandation hybride (contenu + filtrage collaboratif)
- Mise en cache Redis pour requêtes fréquentes
- Déploiement containerisé (Docker + Kubernetes)

## 📝 Notes Techniques

**Pourquoi TF-IDF plutôt que Word2Vec/BERT ?**
- Interprétabilité : on peut identifier les termes clés
- Performance : vectorisation ultra-rapide même sur 10k+ critiques
- Simplicité : pas besoin de GPU ni de modèles pré-entraînés
- Efficacité : pour ce cas d'usage (similarité textuelle), TF-IDF reste très performant

**Limitations connues**
- Ne capture pas la sémantique profonde (ex : synonymes, négations complexes)
- Nécessite un recalcul complet lors de l'ajout de nouvelles critiques
- Mémoire : matrice TF-IDF peut être volumineuse pour datasets >100k critiques

## 📄 Licence

Projet réalisé dans le cadre d'un test technique.

## 👤 Auteur

Développé avec IA assistée (segments générés spécifiés conformément aux consignes du test).

