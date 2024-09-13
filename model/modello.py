from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._list_sightings = []
        self._directed_graph = nx.DiGraph()  # Grafo orientato

    def load_sightings(self):
        self._list_sightings = DAO.get_all_sightings()

    @property #questo decoratore permette di chiamare il metodo come se fosse un attributo
    def list_sightings(self):
        return self._list_sightings

    def get_shapes_by_year(self, year: int):
        # Estrai le forme dagli avvistamenti per l'anno selezionato, escludendo quelle vuote
        shapes = set(
            sighting.shape
            for sighting in self._list_sightings
            if sighting.datetime.year == year and sighting.shape and sighting.shape.strip()
        )
        return shapes

    def build_directed_graph(self, shape: str, year: int):

        # Filtra gli avvistamenti per anno e forma
        filtered_sightings = [s for s in self._list_sightings if s.datetime.year == year and s.shape == shape]

        # Debug: stampa il numero di avvistamenti filtrati
        print(f"Avvistamenti filtrati per l'anno {year} e forma {shape}: {len(filtered_sightings)}")

        # Verifica quali avvistamenti sono stati filtrati
        for sighting in filtered_sightings:
            print(f"id: {sighting.id}, città: {sighting.city}, stato: {sighting.state}, data: {sighting.datetime}")

        # Creazione del grafo
        self._directed_graph.clear()
        for sighting in filtered_sightings:
            self._directed_graph.add_node(sighting)  # Aggiunta come nodo
            for sighting2 in filtered_sightings:
                if sighting.state == sighting2.state and sighting.datetime < sighting2.datetime:
                    self._directed_graph.add_edge(sighting, sighting2)

        # Debug: verifica il numero di nodi nel grafo
        print(f"Numero di nodi nel grafo dopo l'aggiunta: {self._directed_graph.number_of_nodes()}")

    def get_num_of_nodes(self):
        # Restituisce il numero di nodi nel grafo
        return self._directed_graph.number_of_nodes()

    def get_num_of_edges(self):
        # Restituisce il numero di archi nel grafo
        return self._directed_graph.number_of_edges()

    def get_weakly_connected_components(self):
        # Restituisce il numero di componenti debolmente connesse
        return nx.number_weakly_connected_components(self._directed_graph)

    def get_largest_weakly_connected_component(self):
        # Restituisce la componente connessa più grande
        weakly_connected_components = nx.weakly_connected_components(self._directed_graph)
        largest_component = max(weakly_connected_components, key=len)
        return largest_component