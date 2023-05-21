from neo4j import GraphDatabase

uri = "bolt://44.199.210.122:7687"
id = "neo4j"
password = "certification-nameplate-steels"

driver = GraphDatabase.driver(uri, auth=(id, password), encrypted=False)

#Liste des itinéraires réalisable. Tester avec nos programmes
Itinéraire_possible = [
    ["Paris", "London", "Rome", "Dubai", "Tokyo", "New York"],
    ["Paris", "Rome", "Budapest", "Berlin", "Dublin", "Oslo"],
    ["Paris", "Rome", "Dubai", "Moscow", "Washington", "Los Angeles"],
    ["Paris", "London", "Moscow", "Beijing", "Tokyo", "New York"],
    ["Paris", "Mexico City", "Buenos Aires", "Santiago", "New York", "Montreal"]
]

# Fonction pour récupérer les vols directs entre deux villes
def get_direct_flights(tx, departure_city, arrival_city):
    query = """
    MATCH (a:Airport {ville: $departure_city})-[r:Route]->(b:Airport {ville: $arrival_city})
    RETURN a.nom AS departure_nom, b.nom AS arrival_nom, r.Id_Airline AS compagny_id
    """
    result = tx.run(query, departure_city=departure_city, arrival_city=arrival_city)
    return [(record["departure_nom"], record["arrival_nom"], record["compagny_id"]) for record in result]

# Fonction pour récupérer les vols avec une escale entre deux villes
def get_flights_with_stopover(tx, departure_city, arrival_city,stopover):
    query = """
    MATCH (a:Airport {ville: $departure_city})-[r1:Route]->(stopover: Airport  {ville: $stopover})-[r2:Route]->(b:Airport {ville: $arrival_city})
    RETURN a.nom AS departure_nom, stopover.nom AS stopover_nom, b.nom AS arrival_nom, r1.Id_Airline AS compagny_id1,  r2.Id_Airline AS compagny_id2
    """
    result = tx.run(query, departure_city=departure_city, arrival_city=arrival_city, stopover=stopover)
    return [(record["departure_nom"], record["stopover_nom"], record["arrival_nom"], record["compagny_id1"], record["compagny_id2"]) for record in result]

# Fonction pour récupérer les vols avec une escale entre deux villes aléatoirement
def get_flights_with_stopover_random(tx, departure_city, arrival_city):
    query = """
    MATCH (a:Airport {ville: $departure_city})-[r1:Route]->(stopover)-[r2:Route]->(b:Airport {ville: $arrival_city})
    RETURN a.nom AS departure_nom, stopover.nom AS stopover_nom, b.nom AS arrival_nom, r1.Id_Airline AS compagny_id1,  r2.Id_Airline AS compagny_id2
    """
    result = tx.run(query, departure_city=departure_city, arrival_city=arrival_city)
    return [(record["departure_nom"], record["stopover_nom"], record["arrival_nom"], record["compagny_id1"], record["compagny_id2"]) for record in result]

# Fonction principale pour obtenir les vols en fonction des critères donnés
def get_flight_options(departure_city, arrival_city, preferred_airline, stopover, random):
    with driver.session() as session:
        if random:
            if preferred_airline:
                # Recherche avec compagnie aérienne privilégiée
                query = """
                    MATCH (a:Airport {ville: $departure_city})-[r1:Route]->(stopover)-[r2:Route]->(b:Airport {ville: $arrival_city})
                    WHERE r1.Id_Airline = $preferred_airline AND r2.Id_Airline = $preferred_airline
                    RETURN a.nom AS departure_nom, stopover.nom AS stopover_nom, b.nom AS arrival_nom, r1.Id_Airline AS compagny_id1,  r2.Id_Airline AS compagny_id2
                    """
                result = session.run(query, departure_city=departure_city, arrival_city=arrival_city,
                                     preferred_airline=preferred_airline)
                flight_options = [(record["departure_nom"], record["stopover_nom"], record["arrival_nom"], record["compagny_id1"],
                         record["compagny_id2"]) for record in result]
            else:
                # Recherche avec escale aléatoire
                flight_options = get_flights_with_stopover_random(session, departure_city, arrival_city)
        elif stopover and not random:
            if preferred_airline and stopover:
                # Recherche avec compagnie aérienne privilégiée et escale souhaitée
                query = """
                MATCH (a:Airport {ville: $departure_city})-[r1:Route]->(stopover: Airport  {ville: $stopover})-[r2:Route]->(b:Airport {ville: $arrival_city})
                WHERE r1.Id_Airline = $preferred_airline AND r2.Id_Airline = $preferred_airline
                RETURN a.nom AS departure_nom, stopover.nom AS stopover_nom, b.nom AS arrival_nom,  r1.Id_Airline AS compagny_id1,  r2.Id_Airline AS compagny_id2
                """
                result = session.run(query, departure_city=departure_city, arrival_city=arrival_city,
                                     preferred_airline=preferred_airline, stopover=stopover)
                flight_options = [(record["departure_nom"], record["stopover_nom"], record["arrival_nom"], record["compagny_id1"], record["compagny_id2"]) for record in
                                  result]
            elif stopover:
                # Recherche avec escale souhaitée
                flight_options = get_flights_with_stopover(session, departure_city, arrival_city, stopover)
        elif preferred_airline:
            # Recherche avec compagnie aérienne privilégiée
            query = """
            MATCH (a:Airport {ville: $departure_city})-[r:Route]->(b:Airport {ville: $arrival_city})
            WHERE r.Id_Airline = $preferred_airline
            RETURN a.nom AS departure_nom, b.nom AS arrival_nom, r.Id_Airline AS compagny_id
            """
            result = session.run(query, departure_city=departure_city, arrival_city=arrival_city,
                                 preferred_airline=preferred_airline)
            flight_options = [(record["departure_nom"], record["arrival_nom"], record["compagny_id"]) for record in result]
        else:
            # Recherche de vols directs
            flight_options = get_direct_flights(session, departure_city, arrival_city)

    return flight_options

#Utilisation
tour_du_monde = input("Souhaitez vous faire un tour du monde ? (o/n) : ")
if tour_du_monde == "o":
    departure_city = input('Indiquez la ville de départ : ')
    escale1 = input('Indiquez la ville de la première escale : ')
    escale2 = input('Indiquez la ville de la seconde escale : ')
    escale3 = input('Indiquez la ville de la troisième escale : ')
    escale4 = input('Indiquez la ville de la quatrième escale : ')
    escale5 = input('Indiquez la ville de la cinquième escale : ')
    print("Tour du monde détails :")
    flight_options = get_flight_options(departure_city, escale1, None, None, None)
    print("     -Premier vols possible:")
    for option in flight_options:
        departure_nom, arrival_nom, compagny_id = option
        print(f"        Direct flight: {departure_nom} -> {arrival_nom} with {compagny_id}")
    flight_options = get_flight_options(escale1, escale2, None, None, None)
    print("     -Deuxième vols possible:")
    for option in flight_options:
        departure_nom, arrival_nom, compagny_id = option
        print(f"        Direct flight: {departure_nom} -> {arrival_nom} with {compagny_id}")
    flight_options = get_flight_options(escale2, escale3, None, None, None)
    print("     -Troisième vols possible:")
    for option in flight_options:
        departure_nom, arrival_nom, compagny_id = option
        print(f"        Direct flight: {departure_nom} -> {arrival_nom} with {compagny_id}")
    flight_options = get_flight_options(escale3, escale4, None, None, None)
    print("     -Quatrième vols possible:")
    for option in flight_options:
        departure_nom, arrival_nom, compagny_id = option
        print(f"        Direct flight: {departure_nom} -> {arrival_nom} with {compagny_id}")
    flight_options = get_flight_options(escale4, escale5, None, None, None)
    print("     -Cinquième vols possible:")
    for option in flight_options:
        departure_nom, arrival_nom, compagny_id = option
        print(f"        Direct flight: {departure_nom} -> {arrival_nom} with {compagny_id}")
    flight_options = get_flight_options(escale5, departure_city, None, None, None)
    print("     -Vols retour possible:")
    for option in flight_options:
        departure_nom, arrival_nom, compagny_id = option
        print(f"        Direct flight: {departure_nom} -> {arrival_nom} with {compagny_id}")


else:
    print("Vous ne souhaitez pas faire de tour du monde. Merci de préciser votre voyage.")
    departure_city = input('\nIndiquez la ville de départ : ')
    arrival_city = input("Indiquez la ville d'arrivé : ")
    preferred_airline = None
    random = None
    stopover = None
    comp = input('Souhaitez-vous spécifier une compagnie en particulier ? (o/n) : ')
    if comp == 'o':
        preferred_airline = input('Quelle est la compagnie avec laquelle vous souhaitez effectuer votre trajet ? : ')
    escale = input('Souhaitez-vous faire une esacle ? (o/n) : ')
    if escale == 'o':
        stopover = input("Avez-vous une ville de prédiléction pour votre escale ? Si oui, laquelle ? (n / Ville) : ")
        if stopover == "n":
            random = "Ok"

    flight_options = get_flight_options(departure_city, arrival_city, preferred_airline, stopover, random)
    #Réponse à la demande
    print("Flight options:")
    for option in flight_options:
        if len(option) == 3:
            departure_nom, arrival_nom, compagny_id = option
            print(f"Direct flight: {departure_nom} -> {arrival_nom} with {compagny_id}")
        elif len(option) == 5:
            departure_nom, stopover_nom, arrival_nom, compagny_id1, compagny_id2 = option
            print(f"Flight with stopover: {departure_nom} -> {stopover_nom} -> {arrival_nom} with {compagny_id1} and {compagny_id2}")
        else:
            print("Aucun vol disponible")

# Fermeture de la connexion à la base de données Neo4j
driver.close()