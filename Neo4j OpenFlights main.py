from neo4j import GraphDatabase

uri = "bolt://44.199.210.122:7687"
id = "neo4j"
password = "certification-nameplate-steels"

driver = GraphDatabase.driver(uri, auth=(id, password), encrypted=False)

#Fonction pour obtenir les vols entre deux villes
def obtenir_vols(ville_depart, ville_arrivee, compagnie=None, escale=None):
    query = """
    MATCH (d:Airport {ville: $ville_depart})-[r:Route]->(a:Airport {ville: $ville_arrivee})
    """

    if compagnie:
        query += "WHERE r.Id_Airline = $compagnie "

    if escale:
        query += "AND r.Stop = $escale "

    query += "RETURN ID(r) as Id_Route, r.Stop as Stop, r.Id_Airline as Compagnie"

    with driver.session() as session:
        result = session.run(query, ville_depart=ville_depart, ville_arrivee=ville_arrivee,
                             compagnie=compagnie, escale=escale)
        return result.data()

# Fonction pour afficher les vols
def afficher_vols(vols):
    print("Vols disponibles :")
    for vol in vols:
        print(f"ID Route : {vol['Id_Route']}, Nombre d'escales : {vol['Stop']}, Compagnie : {vol['Compagnie']}")

# Exemple d'utilisation
# ville_depart = input("Ville de départ : ")
# ville_arrivee = input("Ville d'arrivée : ")
# compagnie = input("Compagnie aérienne privilégiée : ")
# escale = input("Escale souhaitée : ")
#
# vols = obtenir_vols(ville_depart, ville_arrivee, compagnie, escale)
# afficher_vols(vols)

# Fermeture de la connexion à la base de données Neo4j
driver.close()

#Test
escales_tour_monde = [
    ["Paris", "New York", "Los Angeles", "Tokyo", "Paris"],
    ["Paris", "Rome", "Dubai", "Bangkok", "Paris"],
    ["Paris", "Rio de Janeiro", "Cape Town", "Sydney", "Paris"],
    ["Paris", "London", "Moscow", "Beijing", "Paris"],
    ["Paris", "Mexico City", "Buenos Aires", "Santiago", "Paris"]
]

for i, escales in enumerate(escales_tour_monde):
    print(f"Itinéraire {i+1}:")
    for j in range(len(escales)-1):
        vols = obtenir_vols(escales[j], escales[j+1])
        afficher_vols(vols)
    print("")



