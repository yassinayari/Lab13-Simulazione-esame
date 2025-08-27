import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapDrivers = {}


    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, anno):
        self._grafo.clear()
        drivers = DAO.getDriversByYear(anno)
        self._grafo.add_nodes_from(drivers)
        for d in drivers:
            self._idMapDrivers[d.driverID] = d

        edges = DAO.getDriverYearResults(anno, self._idMapDrivers)
        for e in edges:
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




