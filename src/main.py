import sys
from recommender import Recommandeur


### INTERFACE CLI ###
# Parse les arguments de la ligne de commande, instancie le recommandeur,
# exécute la recherche de similarité et affiche les résultats formatés.

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <chemin_csv> <id_critique> [top_k]")
        sys.exit(1)

    chemin_csv = sys.argv[1]
    id_critique = sys.argv[2]
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    recommandeur = Recommandeur(chemin_csv)
    recommandations = recommandeur.recommander(id_critique, top_k=top_k)

    if not recommandations:
        print(f"\nAucune recommandation pour l'ID: {id_critique}")
    else:
        print(f"\nTop {len(recommandations)} critiques similaires à {id_critique}:")
        for rang, (id_rec, score) in enumerate(recommandations, start=1):
            print(f"  {rang}. ID {id_rec:>10}  |  Score: {score:.3f}")


### POINT D'ENTRÉE ###

if __name__ == "__main__":
    main()
