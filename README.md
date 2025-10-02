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

Le projet utilise trois briques principales en Python :

- **pandas** pour lire et préparer les CSV,  
- **numpy** pour les calculs rapides,  
- **scikit-learn** pour la vectorisation TF-IDF et le calcul de similarité cosinus.

### Pourquoi TF-IDF ?

**TF-IDF (Term Frequency – Inverse Document Frequency)** transforme chaque critique en vecteur de nombres.  
- **TF (Term Frequency)** : plus un mot apparaît dans une critique, plus il pèse lourd.  
- **IDF (Inverse Document Frequency)** : plus un mot est répandu dans tout le corpus (*film*, *acteur*, *bien*), moins il compte.  

Ainsi, les mots vraiment caractéristiques d’une critique (ex. *“bagarres”*, *“rythme lent”*) ressortent plus que les mots génériques.  

En comparant ces vecteurs avec la **similarité cosinus** :  
- Score proche de **1** → critiques très proches lexicalement.  
- Score proche de **0** → critiques différentes.  

```
Entrée CSV
│
▼
┌─────────────────────────────────────────┐
│ 1. Chargement & combinaison │
│ titre + contenu │
└─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 2. Nettoyage du texte │
│ • Suppression balises HTML │
│ • Suppression URLs │
│ • Normalisation unicode (accents) │
│ • Suppression ponctuation & chiffres │
│ • Passage en minuscules │
└─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 3. Injection de la note │
│ texte + "note_X note_X ..." (5x) │
└─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 4. Filtrage des critiques courtes │
│ Conserver uniquement len(text) ≥ 50 │
└─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 5. Vectorisation TF-IDF │
│ • n-grams : 1-2 │
│ • max_features : 50 000 │
│ • min_df : 2 │
└─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 6. Similarité cosinus │
│ Comparaison critique vs toutes │
└─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────┐
│ 7. Extraction du Top-K │
│ numpy.argpartition (O(n)) │
└─────────────────────────────────────────┘
│
▼
Résultats : (titre, extrait, note, auteur) + score de similarité cosinus (0 à 1)
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

Claude Sonnet 4.5 utilisé en renfort sur la logique la vectorisation TF-ID et le calcul de similarité cosinus.
