from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select distinct year from seasons s"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getDriversByYear(year):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.driverId as driverID, d.forename as name, d.surname as surname
                    from drivers d, races r, results re
                    where r.`year` = %s
                    and d.driverId = re.driverId 
                    and r.raceId = re.raceId 
                    and re.`position` is not null"""

        cursor.execute(query, (year, ))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getDriversByYearResults(year, idMapDrivers):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as d1, r2.driverId as d2, count(*) as cnt
                    from results r1, results r2, races r
                    where r1.raceId = r2.raceId 
                    and r.raceId = r1.raceId 
                    and r.`year` = %s
                    and r1.position < r2.position
                    and r1.`position` is not null
                    and r1.`position` is not null
                    group by d1, d2"""

        cursor.execute(query, (year,))

        for row in cursor:
            results.append((idMapDrivers[row["d1"]],idMapDrivers[row["d2"]], row["cnt"]))

        cursor.close()
        conn.close()
        return results