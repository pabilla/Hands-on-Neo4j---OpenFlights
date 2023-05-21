import csv
from neo4j import GraphDatabase

uri = "bolt://44.199.210.122:7687"
id = "neo4j"
password = "certification-nameplate-steels"

driver = GraphDatabase.driver(uri, auth=(id, password), encrypted=False)

with open('airports.csv', newline='', encoding='utf-8') as csvfile1, \
        open('routes.csv', newline='', encoding='utf-8') as csvfile2:
    reader1 = csv.reader(csvfile1, delimiter=',', quotechar='"')
    reader2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
    next(reader1)
    next(reader2)

    airports = {}
    for row in reader1:
        print(row)
        query = """
            MERGE (a:Airport {id: $id, nom: $nom, ville: $ville, pays: $pays, ICAO: $ICAO, IATA: $IATA})
        """
        params = {"id": row[0], "nom": row[1], "ville": row[2], "pays": row[3], "ICAO": row[4], "IATA": row[5]}
        with driver.session() as session:
            session.run(query, params)

        airports[row[0]] = row[1]

    for row in reader2:
        print(row)
        source_id = row[3]
        dest_id = row[5]
        source_node = airports.get(source_id)
        dest_node = airports.get(dest_id)
        if source_node is not None and dest_node is not None:
            query = """
                MATCH (source:Airport {id: $source_id})
                MATCH (dest:Airport {id: $dest_id})
                MERGE (source)-[r:Route {Id_Airline: $Id_Airline, Source_Airport_ID: $source_id,
                    Destination_Airport_ID: $dest_id, Stop: $Stop, Equipement: $Equipement}]->(dest)
            """
            params = {"source_id": source_id, "dest_id": dest_id, "Id_Airline": row[1], "Stop": row[7], "Equipement": row[8]}
            with driver.session() as session:
                session.run(query, params)



