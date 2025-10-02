import sys
from recommender import load_data, find_similar


if len(sys.argv) < 3:
    print("Usage: python main.py <chemin_csv> <id_critique> [top_k]")
    sys.exit(1)

data, reviews, vectors, lookup = load_data(sys.argv[1])
top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5

recommandations = find_similar(sys.argv[2], data, reviews, vectors, lookup, top_k)

for i, c in enumerate(recommandations, 1):
    print(f"{i}. [Score: {c['score']:.3f}] ID {c['id']} | Note: {c['note']}/10 | @{c['auteur']}")
    print(f"   {c['titre']}")
    print(f"   {c['extrait']}\n")
