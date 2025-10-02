# movie-review-recommender

Recommandation de critiques similaires par TF-IDF et similarité cosinus.

## Objectif

Trouve des critiques de films similaires à une critique donnée (même film). Conçu pour suggérer d'autres avis proches sur une page de lecture de critique.

**Exemple** : Un utilisateur lit une critique négative de Fight Club → le système suggère d'autres critiques similaires.

## Données

Deux fichiers CSV fournis :
- `data/fightclub_critique.csv` (~ 5 000 critiques)
- `data/interstellar_critique.csv` (~ 11 000 critiques)

**Colonnes** : `id`, `review_title`, `review_content`, `rating`, `username`

## Structure

```
movie-review-recommender/
├── data/
│   ├── fightclub_critique.csv
│   └── interstellar_critique.csv
├── src/
│   ├── recommender.py    (86 lignes)
│   └── main.py           (17 lignes)
├── requirements.txt
└── README.md
```

**Pipeline** :

**Stack** : Python, pandas, scikit-learn, numpy

```
CSV Input
    │
    ▼
┌─────────────────────────────────────────┐
│  1. Load & Combine                       │
│     titre + contenu                      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  2. Clean Text                           │
│     • Remove HTML tags                   │
│     • Remove URLs                        │
│     • Normalize unicode (accents)        │
│     • Remove punctuation & numbers       │
│     • Lowercase & trim                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  3. Inject Ratings                       │
│     text + "note_X note_X ..." (5x)      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  4. Filter Short Reviews                 │
│     Keep only len(text) >= 50            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  5. TF-IDF Vectorization                 │
│     • n-grams: 1-2                       │
│     • max_features: 50,000               │
│     • min_df: 2                          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  6. Cosine Similarity                    │
│     Compare input review vs all          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  7. Extract Top-K                        │
│     numpy.argpartition (O(n))            │
└─────────────────────────────────────────┘
    │
    ▼
Results (titre, extrait, note, auteur) + score (0-1) (plus proche de 1 = plus similaire)

```

**Pourquoi TF-IDF ?**
- Rapide (pas de GPU requis)
- Interprétable (vocabulaire visible)
- Efficace pour similarité lexicale
- Flexible (intégration des notes)

## Installation

```bash
git clone https://github.com/RomeoCavazza/movie-review-recommender.git
cd movie-review-recommender
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python src/main.py <chemin_csv> <id_critique> [top_k]
```

**Exemple** :
```bash
python src/main.py data/fightclub_critique.csv 20761 3
```

## Note

Projet développé avec assistance IA (Claude/Cursor) pour l'implémentation de la vectorisation TF-IDF, du calcul de similarité cosinus et la rédaction du README.