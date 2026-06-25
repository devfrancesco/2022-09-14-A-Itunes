import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._album = []
        self._idMapA = {}
        self._bestPath = []

    def getMaxPath(self, source, minuti):
        if source.Durata > minuti:
            return []  # oppure [] / solleva eccezione, a seconda di come la view gestisce l'errore
        self._bestPath = []
        componente = nx.node_connected_component(self._graph, source)
        parziale = [source]
        self._ricorsione(parziale, minuti, source.Durata, componente)
        return self._bestPath

    def _ricorsione(self, parziale, minuti, peso, componente):
        if len(parziale) > len(self._bestPath):
            self._bestPath = list(parziale)
        nodo_corrente = parziale[-1]
        for connesso in componente:
            if connesso not in parziale:
                peso_nuovo = peso + connesso.Durata
                if peso_nuovo <= minuti:
                    parziale.append(connesso)
                    self._ricorsione(parziale, minuti, peso_nuovo, componente)
                    parziale.pop()

    def buildGraph(self, minuti):
        self._graph.clear()
        self._idMapA = {}
        self._album = DAO.getAllAlbum(minuti)
        for a in self._album:
            self._idMapA[a.AlbumId] = a
        self._graph.add_nodes_from(self._album)
        allEdges = DAO.getAllEdges(minuti, self._idMapA)
        for e in allEdges:
            self._graph.add_edge(e[0], e[1])

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getInfoConnessa(self, album_id):
        source = self._idMapA[int(album_id)]
        conn = nx.node_connected_component(self._graph, source)
        dimesnione = len(conn)
        durata_tot = sum(a.Durata for a in conn)
        return dimesnione, durata_tot

    def getAlbumName(self, id):
        return self._idMapA[int(id)]




