# Movie review recommender

## Objectif

Trouve des critiques de films similaires à une critique donnée (même film). Conçu pour suggérer d'autres avis proches sur une page de lecture de critique.

**Exemple** : Un utilisateur lit une critique négative de Fight Club → le système suggère d'autres critiques similaires.

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
## Choix techniques

Le projet est codé en **Python 3** et repose sur un petit nombre de bibliothèques standards :

- **pandas** : utilisé pour charger les fichiers CSV et manipuler les colonnes (sélection, concaténation du titre + contenu, filtrage des critiques trop courtes).  
- **numpy** : fournit les structures numériques rapides et la fonction `argpartition` qui permet d’extraire le top-K des similarités en temps linéaire au lieu d’un tri complet (utile quand il y a des milliers de critiques).  
- **scikit-learn** : coeur de l’algorithme avec `TfidfVectorizer` pour transformer chaque critique en vecteur pondéré par la fréquence des termes, et `cosine_similarity` pour mesurer la proximité entre critiques.  
- **unicodedata / re (regex)** : nettoient les textes (suppression des accents, ponctuation, HTML, URLs).

### Pourquoi TF-IDF + cosinus ?

- **TF-IDF (Term Frequency – Inverse Document Frequency)** donne une représentation claire : chaque mot/bi-gramme a un poids qui augmente avec sa fréquence dans la critique mais diminue s’il est trop courant dans tout le corpus.  
- Couplé avec la **similarité cosinus**, cela permet de comparer deux critiques sur leur **profil lexical** : plus elles partagent des expressions marquantes (ex. *“combats à mains nues”*, *“rythme lent”*), plus leur score est proche de 1.  
- Contrairement à des embeddings plus lourds (BERT, Sentence-Transformers), TF-IDF a l’avantage d’être :  
  - **rapide** à calculer (même sur 10 000 critiques),  
  - **interprétable** (on peut voir quels mots contribuent au score),  
  - **sans dépendances lourdes** (CPU suffisant, pas besoin de GPU). 

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

Intervention de Claude Sonnet 4.5 pour l'implémentation de la vectorisation TF-ID et le calcul de similarité cosinus (+ rédaction du README.md)
