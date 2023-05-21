# Hands on Neo4j - OpenFlights

<!-- TOC -->
* [Hands on Neo4j - OpenFlights](#hands-on-neo4j---openflights)
  * [About the app](#about-the-app)
  * [Data importation](#data-importation)
<!-- TOC -->

## About the app
Cette app est une démo des capacités du Neo4j Graph Data Science (GDS). 

## Data importation

La première partie de notre code effectue l'import de données à partir de fichiers CSV dans une base de données Neo4j. Voici une explication du code :

* Le code utilise les modules `csv` pour lire les fichiers CSV et `neo4j` pour interagir avec la base de données Neo4j.
* Une URI est spécifiée pour se connecter à la base de données Neo4j. Elle indique l'adresse et le port du serveur Neo4j.
* Les identifiants (`id` et `password`) sont spécifiés pour l'authentification à la base de données.
* Un objet `driver` est créé en utilisant l'URI et les identifiants pour établir une connexion à la base de données Neo4j.
* Deux fichiers CSV sont ouverts : "airports.csv" et "routes.csv". Ils contiennent les données des aéroports et des routes respectivement.
* Les fichiers CSV sont lus en utilisant les objets `csv.reader`. La fonction `next` est utilisée pour passer la première ligne des fichiers qui contient les en-têtes.
* Une boucle est utilisée pour traiter chaque ligne du fichier "airports.csv". Les données de chaque ligne sont extraites et utilisées pour construire une requête Cypher `CREATE` pour créer un nœud de type "Airport" dans la base de données Neo4j. Les paramètres de la requête sont définis à partir des valeurs de la ligne courante du fichier CSV. La requête est exécutée dans une session Neo4j, ce qui crée les nœuds correspondants dans la base de données. De plus, les correspondances entre les identifiants d'aéroport et les noms d'aéroport sont stockées dans le dictionnaire `airports`.
* Une autre boucle est utilisée pour traiter chaque ligne du fichier "routes.csv". Les données de chaque ligne sont extraites et utilisées pour construire une requête Cypher `CREATE` pour créer une relation de type "Route" entre les nœuds d'aéroport correspondants dans la base de données Neo4j. Les paramètres de la requête sont définis à partir des valeurs de la ligne courante du fichier CSV. La requête est exécutée dans une session Neo4j, ce qui crée les relations correspondantes dans la base de données.

En résumé, ce code importe les données des fichiers CSV dans une base de données Neo4j en créant des nœuds de type "Airport" et des relations de type "Route" entre ces nœuds.
