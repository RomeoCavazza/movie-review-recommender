### IMPORTS ###
# sklearn     : Vectorisation TF-IDF + similarité cosinus
# pandas      : Chargement CSV et manipulation de dataframes
# numpy       : Optimisation argpartition (O(n) au lieu de O(n log n))
# re/unicodedata : Nettoyage et normalisation de texte

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import re
import unicodedata


### NORMALISATION UNICODE ###
# Décompose les caractères accentués en caractères de base plus modificateurs,
# puis encode en ASCII en supprimant les modificateurs.

def supprimer_accents(texte: str) -> str:
    normalise = unicodedata.normalize("NFKD", texte)
    ascii_seulement = normalise.encode("ascii", "ignore").decode("ascii")
    return ascii_seulement


### PIPELINE DE NETTOYAGE ###
# Applique une série de transformations pour normaliser le texte brut :
# supprime les balises HTML et URLs, convertit en minuscules, retire les accents,
# élimine la ponctuation et les chiffres, normalise les espaces multiples.

def nettoyer_texte(texte):
    if not isinstance(texte, str):
        return ""
    
    texte = re.sub(r"<[^>]+>", " ", texte)
    texte = re.sub(r"https?://\S+|@\S+", " ", texte)
    texte = texte.lower()
    texte = supprimer_accents(texte)
    texte = re.sub(r"[^\w\s]|\d+", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    
    return texte


### RECOMMANDEUR - Filtrage par Contenu ###
# Charge les critiques depuis un CSV, les prétraite, construit une matrice TF-IDF
# et permet de rechercher les critiques similaires par similarité cosinus.

class Recommandeur:

    def __init__(self, chemin_csv: str):
        # Chargement du CSV
        dataframe = pd.read_csv(chemin_csv, encoding="utf-8")

        # Préparation du texte
        colonne_titre = dataframe.get("review_title", pd.Series([""] * len(dataframe)))
        colonne_contenu = dataframe.get("review_content", pd.Series([""] * len(dataframe)))
        texte_combine = (colonne_titre.fillna("") + " " + colonne_contenu.fillna("")).str.strip()

        dataframe["texte_brut"] = texte_combine
        dataframe["texte_propre"] = dataframe["texte_brut"].apply(nettoyer_texte)

        # Filtrage des critiques
        LONGUEUR_MIN = 50
        dataframe = dataframe[dataframe["texte_propre"].str.len() >= LONGUEUR_MIN].copy()

        dataframe["id_str"] = dataframe["id"].astype(str)
        self.df_critiques = dataframe[["id", "id_str", "texte_propre"]].reset_index(drop=True)

        # Vectorisation TF-IDF
        self.vectoriseur = TfidfVectorizer(
            max_features=50000,
            ngram_range=(1, 2),
            min_df=2
        )
        self.matrice_tfidf = self.vectoriseur.fit_transform(self.df_critiques["texte_propre"])

        # Index de recherche
        self.id_vers_index = {
            id_critique: index
            for index, id_critique in enumerate(self.df_critiques["id_str"])
        }

    ### RECHERCHE K-PLUS PROCHES VOISINS ###
    # Calcule les scores de similarité cosinus entre une critique source et toutes
    # les autres, utilise argpartition pour extraire les k meilleures en O(n),
    # filtre par score minimal et retourne la liste triée.

    def recommander(self, id_critique, top_k=5, score_min=0.10):
        # Validation de l'ID
        id_critique_str = str(id_critique)

        if id_critique_str not in self.id_vers_index:
            return []

        index_source = self.id_vers_index[id_critique_str]

        # Calcul de similarité
        scores_similarite = cosine_similarity(
            self.matrice_tfidf[index_source],
            self.matrice_tfidf
        ).flatten()

        scores_similarite[index_source] = -1.0

        # Optimisation argpartition
        nombre_critiques = len(scores_similarite)
        taille_buffer = top_k + 20
        k_partition = min(taille_buffer, nombre_critiques)

        indices_non_tries = np.argpartition(scores_similarite, -k_partition)[-k_partition:]
        indices_tries = indices_non_tries[np.argsort(scores_similarite[indices_non_tries])[::-1]]

        # Construction des résultats
        resultats = []
        for index in indices_tries:
            if len(resultats) >= top_k:
                break

            score = scores_similarite[index]
            if score < score_min:
                continue

            ligne_critique = self.df_critiques.loc[index]
            id_critique_int = int(ligne_critique["id"]) if pd.notna(ligne_critique["id"]) else None

            resultats.append((id_critique_int, round(float(score), 3)))

        return resultats
