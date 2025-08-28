import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allNodes = []
        self._grafo = nx.DiGraph()
        self._idMapDrivers = {}

    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, year):
        self._allNodes = DAO.getDriversByYear(year)
        self._grafo.clear()
        self._grafo.add_nodes_from(self._allNodes)
        for driver in self._allNodes:
            self._idMapDrivers[driver.driverID] = driver

        self.allEdges = DAO.getDriversByYearResults(year, self._idMapDrivers)
        for e in self.allEdges:
            self._grafo.add_edge(e[0], e[1], weight = e[2])


    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getBestDriver(self):
        best = 0
        bestdriver = None
        for n in self._grafo.nodes:
            score = 0
            for e_out in self._grafo.out_edges(n, data=True):
                score += e_out[2]["weight"]
            for e_in in self._grafo.in_edges(n, data=True):
                score -= e_in[2]["weight"]

            if score > best:
                 bestdriver = n
                 best = score

        return bestdriver, best