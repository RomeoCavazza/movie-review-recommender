# Data

# Description

**Durée du test**:  ~3h

**Date limite** : 7 jours

**Déroulement :** 

L’exercice ci dessous consiste en deux étapes : 

- La création d’un system design
- L’implémentation de ce system design

Nous estimons le test à 3h, libre à vous de prendre plus/moins de temps pour effectuer ce test.

Si vous utilisez l’IA pour réaliser une partie de votre test, veuillez préciser quels segments de votre test ont été généré par IA. 
**Si nous détectons que vous avez utilisé de l’IA sans nous en avoir informé : vous serez pénalisé.**

**Sujet:**

SensCritique souhaiterait permettre à ses utilisateurs d’afficher les critiques semblable à une critique en cours de lecture. Par exemple : 

- Si je lis une critique sur le film Fight Club, qui raconte que l’utilisateur n’a pas aimé le film parce qu’il y a trop de combats à mains nues (bagarre), nous souhaiterions que l’utilisateur puisse avoir des suggestions de critique qui sont proches ou identiques.

Vous devez créer cet algorithme de recommandation de critique.

## System design

Réaliser le system design de cette fonctionnalité en fournissant : 

- Un schéma d’architecture logicielle/infrastructure expliquant comment votre système fonctionne
- Annoter votre travail en expliquant vos choix (choix des technos etc)

## Implémentation

Une fois votre system design réalisé, implémenter votre solution en respectant les pré-requis ci dessous : 

- Votre code doit être en **Python**
- Votre code doit être disponible sur un **repository github public** (afin que l’on puisse le review)
- Votre code doit recommander des critiques **du même film**

Voici deux extraits de critiques des films Fight Club et Interstellar :

[interstellar_critiques.csv](Data%2027f882bc47288193bf51d583a60c481f/interstellar_critique.csv)

[fightclub_critiques.csv](Data%2027f882bc47288193bf51d583a60c481f/fightclub_critiques.csv)