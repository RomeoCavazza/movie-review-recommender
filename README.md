# Movie Review Recommender

Recommandation de critiques similaires intra-film (MVP).

## Objectif & scope

Cet outil identifie les critiques similaires à une critique donnée, au sein d'un même film. L'utilisateur consulte une critique sur SensCritique (par exemple, un avis négatif sur Fight Club mentionnant trop de violence) et le système suggère automatiquement d'autres critiques proches thématiquement. Le MVP traite un CSV unique correspondant à un seul film : les recommandations sont donc strictement intra-film. Il s'agit d'un filtrage par contenu basé sur la similarité textuelle, sans collaborative filtering.

## Ressources & données

Le projet utilise deux jeux de données au format CSV :

- `data/fightclub_critique.csv` : 5 021 critiques du film Fight Club
- `data/interstellar_critique.csv` : 11 457 critiques du film Interstellar

Chaque CSV contient les colonnes suivantes :

- `id` : identifiant unique de la critique
- `review_title` : titre de la critique
- `review_content` : corps textuel de la critique
- `rating` : note attribuée (1-10)
- `username` : nom de l'utilisateur
- `user_id` : identifiant utilisateur
- `URL` : lien vers la critique sur SensCritique

Le système concatène `review_title` et `review_content` pour former le texte complet analysé. Les critiques de moins de 50 caractères après nettoyage sont écartées.

## Choix techniques (raisonnés)

Les technologies Python suivantes ont été sélectionnées :

- **pandas** : lecture et manipulation des CSV volumineux (10k+ lignes), filtrage et préparation des données.
- **scikit-learn** : vectorisation TF-IDF avec n-grams (1, 2) pour capturer les expressions courantes, calcul de similarité cosinus entre vecteurs.
- **numpy** : optimisation de la recherche top-K via `argpartition` (complexité O(n) au lieu de O(n log n) pour un tri complet).
- **unicodedata** : normalisation Unicode et suppression des accents pour homogénéiser le texte français.

Justifications du choix TF-IDF pour ce MVP :

- Rapide à entraîner et à interroger (pas de GPU requis).
- Interprétable : on peut identifier les termes clés discriminants.
- Robuste pour une implémentation ~3h sur corpus de taille moyenne.
- Efficace pour la similarité lexicale dans un contexte monolingue (français).

## Schéma de la logique (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│  UTILISATEUR                                                     │
│  Sélectionne une critique (ID) depuis l'interface               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Chargement CSV       │
          │  (film unique)        │
          └──────────┬────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Nettoyage texte      │
          │  - Suppression HTML   │
          │  - Normalisation      │
          │  - Suppression accents│
          │  - Filtrage longueur  │
          └──────────┬────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Vectorisation TF-IDF │
          │  (n-grams 1-2)        │
          │  max_features=50k     │
          └──────────┬────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Similarité cosinus   │
          │  (critique source vs  │
          │   toutes les autres)  │
          └──────────┬────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Extraction top-K     │
          │  (argpartition + tri) │
          │  Filtrage score_min   │
          └──────────┬────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Sortie formatée      │
          │  (liste de tuples     │
          │   ID, score)          │
          └──────────────────────┘
```

## Architecture du dépôt

```
movie-review-recommender/
├── data/
│   ├── fightclub_critique.csv      # Dataset Fight Club (5k critiques)
│   └── interstellar_critique.csv   # Dataset Interstellar (11k critiques)
├── src/
│   ├── recommender.py              # Moteur de recommandation
│   └── main.py                     # Interface CLI
├── .gitignore                      # Exclusions Git
├── requirements.txt                # Dépendances Python
├── shell.nix                       # Configuration Nix Shell
├── consigne.md                     # Énoncé du test technique
└── README.md                       # Documentation (ce fichier)
```

### Description des modules Python

- **`recommender.py`** : classe `Recommandeur` qui encapsule toute la logique métier. Au constructeur, charge le CSV, nettoie les textes (suppression HTML/URLs, normalisation Unicode, retrait accents et ponctuation), filtre les critiques trop courtes, puis construit la matrice TF-IDF. La méthode `recommander(id_critique, top_k, score_min)` calcule la similarité cosinus entre la critique source et toutes les autres, extrait les top-K via `argpartition`, filtre par score minimal et retourne la liste triée des IDs recommandés avec leurs scores.

- **`main.py`** : point d'entrée CLI. Parse les arguments de ligne de commande (chemin CSV, ID critique, nombre de recommandations), instancie `Recommandeur`, appelle la méthode de recherche et affiche les résultats formatés dans le terminal.

## Installation

Clonez le dépôt et accédez au répertoire :

```bash
git clone https://github.com/RomeoCavazza/movie-review-recommender.git
cd movie-review-recommender
```

Créez et activez un environnement virtuel Python :

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate sur Windows
```

Installez les dépendances :

```bash
pip install -r requirements.txt
```

**Alternative avec Nix Shell** (si Nix est installé) :

```bash
nix-shell
# L'environnement avec toutes les dépendances est automatiquement chargé
```

## Utilisation (commandes)

### Recommandation par ID de critique

Syntaxe générale :

```bash
python src/main.py <chemin_csv> <id_critique> [top_k]
```

**Arguments** :

- `<chemin_csv>` : chemin vers le fichier CSV des critiques (ex. `data/fightclub_critique.csv`)
- `<id_critique>` : identifiant numérique de la critique source
- `[top_k]` : nombre de recommandations à retourner (optionnel, défaut : 5)

**Exemple 1** : trouver 5 critiques similaires à la critique 20761 de Fight Club

```bash
python src/main.py data/fightclub_critique.csv 20761 5
```

**Exemple 2** : trouver 10 critiques similaires pour Interstellar

```bash
python src/main.py data/interstellar_critique.csv 25246858 10
```

### Sortie attendue

Le programme affiche les résultats dans le terminal sous forme de tableau ASCII :

```
Top 5 critiques similaires à 20761:
  1. ID   21701678  |  Score: 0.595
  2. ID   41298149  |  Score: 0.544
  3. ID  298420055  |  Score: 0.537
  4. ID   16685573  |  Score: 0.494
  5. ID   93289512  |  Score: 0.489
```

Le **score** représente la similarité cosinus (0 à 1) : plus il est proche de 1, plus les critiques sont sémantiquement proches. Les scores inférieurs au seuil minimal (0.10 par défaut) sont filtrés.

## Exemple de sortie (JSON)

Bien que l'interface actuelle soit CLI avec affichage texte, voici à quoi ressemblerait une sortie JSON structurée (évolution future avec API REST) :

```json
{
  "query": {
    "review_id": 20761,
    "film": "Fight Club"
  },
  "recommendations": [
    {
      "id": 21701678,
      "score": 0.595,
      "username": "Alexandre_D",
      "rating": 9,
      "url": "https://senscritique.com/film/fight-club/critique/21701678",
      "snippet": "Film culte des années 90, Fight Club explore la violence masculine..."
    },
    {
      "id": 41298149,
      "score": 0.544,
      "username": "cinephile92",
      "rating": 8,
      "url": "https://senscritique.com/film/fight-club/critique/41298149",
      "snippet": "Un pamphlet anti-consumériste brutal mais nécessaire..."
    },
    {
      "id": 298420055,
      "score": 0.537,
      "username": "Marion_L",
      "rating": 7,
      "url": "https://senscritique.com/film/fight-club/critique/298420055",
      "snippet": "Trop de bagarres à mon goût, mais une mise en scène impeccable..."
    }
  ],
  "metadata": {
    "total_reviews": 5021,
    "processing_time_ms": 124,
    "algorithm": "TF-IDF + cosine similarity"
  }
}
```

## Limites & évolutions

### Limites du MVP

- **Approche lexicale** : TF-IDF capture les mots-clés mais pas la sémantique profonde. Les synonymes, paraphrases et tournures ironiques peuvent être mal captés.
- **Sensibilité à la qualité** : les critiques mal rédigées (fautes, abréviations, SMS speak) réduisent la pertinence.
- **Scalabilité** : matrice TF-IDF chargée en mémoire. Au-delà de 100k critiques, envisager une indexation externe.
- **Monofilm** : chaque CSV correspond à un film unique ; pas de recommandation inter-films.

### Pistes d'évolution

- **Embeddings contextuels** : remplacer TF-IDF par Sentence-BERT (modèle multilingue `paraphrase-multilingual-mpnet-base-v2`) ou CamemBERT fine-tuné pour capturer la sémantique.
- **Indexation vectorielle** : intégrer FAISS (Facebook AI Similarity Search) pour recherche approximative rapide sur millions de critiques.
- **Filtres avancés** : permettre de filtrer par note (ex. recommandations parmi critiques 8+), période, longueur de texte, ton (positif/négatif via analyse de sentiment).
- **API REST** : encapsuler dans FastAPI avec endpoints `/recommend` et `/search`, documentation OpenAPI auto-générée.
- **Pipeline hybride** : combiner filtrage par contenu (TF-IDF/embeddings) et filtrage collaboratif (similarité utilisateur) pour recommandations plus personnalisées.
- **Mise en cache** : utiliser Redis pour stocker les résultats des requêtes fréquentes et réduire la latence.

## Conformité au sujet

Ce projet respecte strictement le cahier des charges du test technique :

- ✅ **Implémentation en Python** : code 100% Python avec librairies standards (pandas, scikit-learn, numpy).
- ✅ **Recommandations intra-film** : chaque CSV correspond à un film unique, le système ne recommande que des critiques du même film.
- ✅ **Repository GitHub public** : code disponible sur https://github.com/RomeoCavazza/movie-review-recommender, avec historique Git propre et documentation complète.

## Usage de l'IA (disclosure)

Conformément aux exigences du test, voici les segments où l'intelligence artificielle a été utilisée :

- **Cadrage du system design** : aide à la structuration de l'architecture (pipeline de nettoyage, choix TF-IDF, optimisations).
- **Rédaction du README** : génération de la structure Markdown, formulation des sections techniques, schéma ASCII.
- **Squelette CLI** : structure de base de `main.py` (parsing arguments, gestion d'erreurs).
- **Commentaires et documentation** : rédaction des docstrings et commentaires inline dans le code.

**Ce qui a été fait manuellement** :

- Implémentation complète de la classe `Recommandeur` (méthodes de nettoyage, vectorisation, recherche top-K).
- Choix des hyperparamètres TF-IDF (n-grams, max_features, min_df) après tests sur les datasets.
- Validation et tests locaux avec les deux CSV (Fight Club, Interstellar).
- Debugging et optimisations (utilisation de `argpartition`, gestion des cas limites).
- Revue et refactoring du code pour cohérence et lisibilité.

Tous les résultats affichés ont été vérifiés sur les datasets réels fournis. Le code a été testé en environnement Nix Shell et fonctionne de manière reproductible.
