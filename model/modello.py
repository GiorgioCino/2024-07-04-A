from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._all_years = DAO.get_all_years()
        self._all_sightings = DAO.get_all_sightings()
        self._id_map_sight ={}
        for sight in self._all_sightings:
            self._id_map_sight[sight.id] = sight

        self._graph = nx.DiGraph()

    def build_graph(self, anno, shape):
        self._graph.clear()

        nodes = DAO.get_all_nodes(anno, shape, self._id_map_sight)
        self._graph.add_nodes_from(nodes)

        archi = []

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                #Prendo i due avvistamenti della coppia
                avvistamento1 = nodes[i]
                avvistamento2 = nodes[j]
                #rendo lo stato dei due avvistamenti
                stato1 = avvistamento1.state      #posso farlo solo se avvistamento 1 è oggetto di sighting
                stato2 = avvistamento2.state

                if stato1 is not None and stato1 != "":#Controllo che lo stato del primo non sia vuoto
                    if stato1 == stato2:#controllo se sono nello stesso stat
                        #Decido il verso dell’arco usando la data
                        if avvistamento1.datetime < avvistamento2.datetime:
                            archi.append((avvistamento1, avvistamento2))

                        elif avvistamento2.datetime < avvistamento1.datetime:
                            archi.append((avvistamento2, avvistamento1))

        for av1, av2 in archi:
            self._graph.add_edge(av1, av2)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def build_graph2(self, anno, shape):
        self._graph.clear()

        nodes = DAO.get_all_nodes(anno, shape, self._id_map_sight)
        self._graph.add_nodes_from(nodes)

        archi = DAO.get_all_edges(anno, shape, self._id_map_sight)

        for av1, av2 in archi:
            self._graph.add_edge(av1, av2)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getNumNodes(self):
        return self._graph.number_of_nodes()
    def getNumEdges(self):
        return self._graph.number_of_edges()

    def get_all_years(self):
        return list(self._all_years)

    def get_all_forme(self,anno):
        forme = DAO.get_all_forme(anno)
        return forme

    def getInfoCompConnessa(self):
        return nx.number_weakly_connected_components(self._graph)

    def getComponenteMaggiore(self):
        componenti = list(nx.weakly_connected_components(self._graph))

        if len(componenti) == 0:
            return []

        componente_max = max(componenti, key=len)

        result = list(componente_max)

        #result.sort(key=lambda nodo: nodo.datetime)

        return result