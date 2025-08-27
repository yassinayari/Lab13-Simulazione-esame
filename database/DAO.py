from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    def getDriversByYear(year):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.driverId  as driverID, d.forename as name, d.surname as surname
                    from drivers d, races r, results re
                    WHERE r.`year` = %s
                    and r.raceId = re.raceId 
                    and d.driverId = re.driverId 
                    and re.`position` is not null"""

        cursor.execute(query, (year,))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getDriverYearResults(year, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as d1, r2.driverId as d2, count(*) as cnt
    				from results as r1, results as r2, races
    				where r1.raceId = r2.raceId
    				and races.raceId = r1.raceId
    				and races.year = %s
    				and r1.position is not null
    				and r2.position is not null 
    				and r1.position < r2.position 
    				group by d1, d2"""

        cursor.execute(query, (year,))

        for row in cursor:
            results.append((idMap[row["d1"]], idMap[row["d2"]], row["cnt"]))

        cursor.close()
        conn.close()
        return results