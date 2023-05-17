from neo4j import GraphDatabase

uri = "bolt://44.199.210.122:7687"
id = "neo4j"
password = "certification-nameplate-steels"

driver = GraphDatabase.driver(uri, auth=(id, password), encrypted=False)

# Obtenir la liste des vols permettant d’effectuer un trajet allant d'une ville a une autre,
def find_vol_direct(tx, ville_depart, ville_arrivee):
    query = """
    MATCH (d:Airport {ville: $ville_depart})-[r:Route]->(a:Airport {ville : $ville_arrivee})
    RETURN ID(r) as Id_Route, r.Stop as Stop, r.Id_Airline as Compagnie
    """
    result = tx.run(query, ville_depart=ville_depart, ville_arrivee=ville_arrivee)
    return result.data()


# with driver.session() as session:
#     vol = session.execute_read(find_vol, "Paris", "London")

# with driver.session() as session:
#    vol = session.execute_read(find_vol, "Kaliningrad", "Moscow")
# print(vol)

def find_vol_indirect(tx, ville_depart, ville_arrivee, nbre_stop):
    query = """
    MATCH (d:Airport {ville: $ville_depart})-[r:Route]->(a:Airport {ville: $ville_arrivee})
    WHERE r.Stop <= $nbre_stop
    RETURN ID(r) as Id_Route, r.Stop as Stop, r.Id_Airline as Compagnie
    """
    result = tx.run(query, ville_depart=ville_depart, ville_arrivee=ville_arrivee, nbre_stop=nbre_stop)
    return result.data()

#AND r.Escale IN [$ville_escale1, $ville_escale2, $ville_escale3, ...]
# Spécifier une compagnie

# comp_souhaitee = input("Compagnie souhaitée :")

def find_compagnie(tx, ville_depart, ville_arrivee, comp_souhaitee):
    query = """
    MATCH (d:Airport {ville: $ville_depart})-[r:Route]->(a:Airport {ville : $ville_arrivee})
    where r.Id_Airline = $comp_souhaitee
    RETURN ID(r) as Id_Route, r.Stop as Stop, r.Id_Airline as Compagnie
    """
    result = tx.run(query, ville_depart=ville_depart, ville_arrivee=ville_arrivee, comp_souhaitee=comp_souhaitee)
    return result.data()


# with driver.session() as session:
#     vol1 = session.execute_read(find_compagnie, "Paris", "London", comp_souhaitee)

# with driver.session() as session:
#    vol = session.execute_read(find_vol, "Kaliningrad", "Moscow")
# print(vol1)

# Spécifier une escale

# stop_souhaite = input("Stop souhaité :")

def find_stop(tx, ville_depart, ville_arrivee, stop_souhaite):
    query = """
    MATCH (d:Airport {ville: $ville_depart})-[r:Route]->(a:Airport {ville : $ville_arrivee})
    where r.Stop = $stop_souhaite
    RETURN ID(r) as Id_Route, r.Stop as Stop, r.Id_Airline as Compagnie
    order by Stop ASC limit 5"""
    result = tx.run(query, ville_depart=ville_depart, ville_arrivee=ville_arrivee, stop_souhaite=stop_souhaite)
    return result.data()


#
# with driver.session() as session:
#     vol2 = session.execute_read(find_compagnie, "Paris", "London", stop_souhaite)

# with driver.session() as session:
#    vol = session.execute_read(find_vol, "Kaliningrad", "Moscow")
# print(vol2)

ville_depart = input("D'où partez-vous ?")
ville_arrivee = input("Où souhaitez-vous aller ?")


def route(tx, ville_depart, ville_arrivee):
    print('Voici les vols disponibles pour votre trajet : \n')
    with driver.session() as session:
        vol = session.execute_read(find_vol_direct, ville_depart, ville_arrivee)
        print(vol)
        comp = input('\n Souhaitez-vous spécifier une compagnie en particulier ? (oui/non)')
        if comp == 'oui':
            comp_souhaitee = input('Quelle est la compagnie avec laquelle vous souhaitez effectuer votre trajet ?')
            vol1 = session.execute_read(find_compagnie, ville_depart, ville_arrivee, comp_souhaitee)
            print(vol1)
        escale = input('\n Souhaitez-vous effecter des escales en particulier ? (oui/non)')
        if escale == 'oui':
            stop_souhaite = input("Dans quelle ville souhaitez-vous effectuer votre escale ? ")
            vol3 = session.execute_read(find_vol_indirect, ville_depart, ville_arrivee, stop_souhaite)
            print(vol3)
with driver.session() as session:
    vol3 = session.execute_read(route, ville_depart, ville_arrivee)
print(vol3)


# def find_compagnie (tx, ville_depart, ville_arrivee, compagnie):
#     query = """
#     MATCH(:Airport{ville:$ville_depart})-[a:Route{Id_Airline:$compagnie}]->(:Airport{ville:$ville_arrivee})
#     RETURN a.Id_Airline"""
#
#     result1 = tx.run(query, ville_depart=ville_depart, ville_arrivee=ville_arrivee, compagnie=compagnie)
#     return result1.data()
#
#
# with driver.session() as session:
#     airline = session.execute_read(find_compagnie, "Kaliningrad", "Moscow", "5067")
#
# print(airline)

