from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import re
import unicodedata


def remove_accents(text):
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("ascii", "ignore").decode("ascii")


def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"https?://\S+|@\S+", " ", text)
    text = text.lower()
    text = remove_accents(text)
    text = re.sub(r"[^\w\s]|\d+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_data(csv_path):
    df = pd.read_csv(csv_path, encoding="utf-8")
    
    title = df.get("review_title", "").fillna("")
    content = df.get("review_content", "").fillna("")
    df["text"] = (title + " " + content).apply(clean_text)
    
    # On injecte la note dans le texte pour influencer la similarité
    # Une critique notée 10/10 aura "note_10" répété 5 fois dans son vecteur
    rating = df.get("rating")
    df["text_rating"] = df.apply(
        lambda row: row["text"] + (f" note_{int(row['rating'])}" * 5 if pd.notna(row.get("rating")) else ""),
        axis=1
    )
    
    df = df[df["text"].str.len() >= 50].reset_index(drop=True)
    df["id_str"] = df["id"].astype(str)
    
    reviews = df[["id", "id_str", "text_rating"]]
    
    # TF-IDF : on transforme le texte en vecteurs numériques
    # n-grams 1-2 = mots seuls + paires de mots (ex: "très bon")
    # max 50k features pour pas exploser la mémoire
    vectors = TfidfVectorizer(max_features=50000, ngram_range=(1, 2), min_df=2).fit_transform(reviews["text_rating"])
    
    lookup = {row["id_str"]: i for i, row in reviews.iterrows()}
    
    return df, reviews, vectors, lookup


def find_similar(review_id, data, reviews, vectors, lookup, top_k=5, min_score=0.10):
    idx = lookup.get(str(review_id))
    if idx is None:
        return []
    
    # Calcule la similarité entre la critique demandée et toutes les autres
    scores = cosine_similarity(vectors[idx], vectors).flatten()
    scores[idx] = -1.0
    
    # On prend un buffer plus grand que top_k au cas où certaines critiques
    # seraient filtrées par le min_score
    buffer_size = min(top_k + 20, len(scores))
    
    # argpartition = optimisation numpy pour extraire les top-K sans tout trier
    # O(n) au lieu de O(n log n)
    top_indices = np.argpartition(scores, -buffer_size)[-buffer_size:]
    sorted_indices = top_indices[np.argsort(scores[top_indices])[::-1]]
    
    results = []
    for i in sorted_indices:
        if len(results) >= top_k:
            break
        if scores[i] < min_score:
            continue
        
        review_id = int(reviews.loc[i, "id"])
        review = data[data["id"] == review_id].iloc[0]
        
        title = str(review.get("review_title", "")).strip()
        content = str(review.get("review_content", "")).strip()
        excerpt = content[:150] + "..." if len(content) > 150 else content
        
        rating = review.get("rating")
        rating_value = int(rating) if pd.notna(rating) else None
        
        author = str(review.get("username", "Anonyme")).strip()
        
        results.append({
            "id": review_id,
            "score": round(float(scores[i]), 3),
            "titre": title,
            "extrait": excerpt,
            "note": rating_value,
            "auteur": author
        })
    
    return results
