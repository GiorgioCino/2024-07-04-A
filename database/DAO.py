from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(s.`datetime`) AS Anno 
FROM sighting s 
ORDER BY Anno DESC
"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Anno"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_forme(anno):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT s.shape
                FROM sighting s
                WHERE s.shape IS NOT NULL
                  AND s.shape != ''
                  AND YEAR(s.`datetime`) = %s
                ORDER BY s.shape
            """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def get_all_nodes(anno,forma, id_map_sight):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.id, s.country 
FROM sighting s 
where s.shape = %s
      and year(s.`datetime`) = %s
 """
            cursor.execute(query, (forma, anno))

            for row in cursor:
                result.append(id_map_sight[row["id"]])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_edges(anno, shape, id_map_sightings):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT 
            s1.id AS av1,
            s2.id AS av2
        FROM sighting s1, sighting s2
        WHERE s1.state = s2.state
          AND s1.state IS NOT NULL
          AND s1.state != ''

          AND YEAR(s1.`datetime`) = %s
          AND YEAR(s2.`datetime`) = %s

          AND s1.shape = %s
          AND s2.shape = %s

          AND s1.`datetime` < s2.`datetime`
    """

        cursor.execute(query, (anno, anno, shape, shape))

        for row in cursor:
            av1 = id_map_sightings[row["av1"]]
            av2 = id_map_sightings[row["av2"]]

            result.append((av1, av2))

        cursor.close()
        conn.close()
        return result





