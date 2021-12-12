# api_bottle-computer_science_bibliography
API that offers information on scientific computer publications

# Définition du projet

Le but du projet est de travailler sur la bibliothèque Python Bottle pour proposer
une API pour le site [http:dbpl.uni-trier.de/db/ht/](http:dbpl.uni-trier.de/db/ht/)
sur lequel nous trouvons des publications scientifiques en informatique.

Pour la suite, le but est de réaliser un serveur web qui se sert de cette API Web
développée précédemment, auquel un utilisateur peut s'y connecter et faire des
recherches sur les auteurs et les publications disponibles.

# API Web

Implémente principalement les url suivantes:
- `/authors/<name>` : avec 'name' le nom d'un auteur, qui retourne des informations
    concernant un auteur: nombres de publications dont il est co-auteur, nombre de co-auteurs.
- `/authors/<name>/publications` : avec 'name' le nom d'un auteur, qui liste les publications
    d'un auteur
- `/authors/<name>/publications/<rank>` : avec 'name' le nom d'un auteur, et 'rank'
    un rang parmi 'AStar', 'A', 'B', 'C', 'National', 'NotRanked', qui liste les publications
    d'un auteur correspondant au range fourni en paramètre selon le site CORE.
- `/authors/<name>/coauthors` : avec 'name' le nom de l'auteur, qui liste les co-auteurs
    d'un auteur.
- `/search/authors/<searchString>` : avec 'searchString' une chaine de caractères permettant
    de chercher un auteur. Cette route retourne la liste des auteurs dont le nom contient
    'searchString' (par exemple, `/search/authors/w` retourne la liste de tous les auteurs
    dont le nom contient un 'w' ou un 'W').
- `/authors/<name_origini>/distance/<name_destination>` : avec 'name_origin' et 'name_destination'
    deux nom d'auteurs, qui retourne la distance de collaboration entre les deux auteurs nommés.
    Cette distance est définie comme la longueur du plus petit chemin '(name_origin, auth1, auth2,
    ..., authX, name_destination)', où 'name_origin' et 'auth1' sont co-auteurs, 'auth1' et 'auth2'
    sont co-auteurs, ..., et 'authX' et 'name_destination' sont co-auteurs. EN particulier
    deux co-auteurs sont à distance 1. En plus de retourner la distance, la réponse doit
    contenir le plus court chemin entre les deux auteurs.

l'API ainsi développée présente les caractéristiques suivantes:
- Toutes les erreurs ont le meme format
- Chaque route qui retourne une liste, retourne au maximum 100 éléments et accepte
    des paramètres d'URL `start` et `count` qui permettent d'afficher `count` éléments,
    à partir du `start`-ième élément. Par exemple: `/search/authors/*` retourne les
    100 premiers auteurs, `/search/authors/*?start=100` affiche les 100 suivants, et
    `/search/authors/*?start=200&count=2` affiche les 2 éléments suivants.


# Test unitaire de l'API Web

C'est un programme qui teste le bon fonctionnement de l'API Web développée précédemment.


# Site Web d'utilisation de l'API

Permet d'acceder au via le web, services offert par l'API Web
