# Information_Retrieval

Le troisième projet de l’enseignement TALN a pour objectif la mise en place d’un système de recherche d’information sur des données non structurées (documents textuels). Le projet est composé d’un corpus de données et d’un algorithme de recherche d’information. Le corpus de documents est composé de 10 articles portant sur le thème du Covid-19. Nous allons pouvoir interroger le système avec des requêtes portant sur les informations dans les documents. Le programme renvoie une liste des documents les plus pertinents par rapport à la requête.

Le projet est développé en Python 3.10 avec l’IDE Visual Studio. Le projet se décompose en quatre parties : d’abord la construction d’un corpus de documents sur le Covid-19, le but de cette partie est d’obtenir un fichier texte pour chaque article qui va être scrapper sur le web. Le contenu de ce fichier texte doit comporter seulement les éléments les plus importants de la page, c’est-à-dire l’article en lui-même. 

Pour cette partie, j’ai essayé plusieurs approches. Cette tâche est importante pour la suite, car s’ils nous manquent des parties ou des paragraphes de l’article, on va perdre de l’information et réduire la pertinence des résultats pour les différentes requêtes. J’ai testé d’abord le plugin Beautiful Soup . Sur les pages des articles, on obtient des informations inutiles (liens, pages de login). J’ai décidé de choisir le plugin trafilatura d’après l’article « Bien choisir son outil d’extraction de contenu à partir du Web » (Gaël Lejeune, Adrien Barbaresi) . C’est un des outils les plus efficaces pour extraire le contenu pertinent d’un article par exemple. 

Une fonction du programme créé les fichiers textes contenants les articles présents sur les pages. On va réaliser une étape de traitement des données (segmentation, élimination des mots-vides, normalisation) pour construire une matrice d’incidence. La matrice d’incidence est représentée par un dictionnaire qui pour chaque terme (clé) associe un tableau (valeur) avec les fréquences pour chaque document. Un autre dictionnaire représente un index inversé avec le numéro du document dans lequel apparaît chaque terme.
La dernière étape est l’implémentation d’un algorithme de recherche sur nos dictionnaires. Une fonction qui prend en paramètre les deux dictionnaires et la requête permet de réaliser cette fonctionnalité. 
