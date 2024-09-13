import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_year_dropdown(self):
        # Carica tutti gli avvistamenti nel model
        self._model.load_sightings()

        # Estrai gli anni dagli avvistamenti
        years = set()
        for sighting in self._model.list_sightings:
            years.add(sighting.datetime.year)

        # Ordina gli anni in modo decrescente
        sorted_years = sorted(years, reverse=True)

        # Popola il menù a tendina con gli anni ordinati
        self._view.ddyear.options.clear()
        for year in sorted_years:
            self._view.ddyear.options.append(ft.dropdown.Option(str(year)))

        # Aggiorna la vista
        self._view.update_page()

    def fill_shape_dropdown(self, e=None):  # Aggiungi 'e' come secondo parametro
        # Ottieni l'anno selezionato
        selected_year = int(self._view.ddyear.value)

        # Filtra gli avvistamenti per l'anno selezionato
        shapes = self._model.get_shapes_by_year(selected_year)

        # Ordina le forme alfabeticamente e popola il menù a tendina
        self._view.ddshape.options.clear()
        for shape in sorted(shapes):
            self._view.ddshape.options.append(ft.dropdown.Option(shape))

        # Aggiorna la vista
        self._view.update_page()

    def handle_graph(self, e):
        # Pulire i risultati precedenti
        # Pulire i risultati precedenti
        self._view.txt_result1.controls.clear()

        # Ottieni l'anno e la forma selezionati
        selected_year = int(self._view.ddyear.value)
        selected_shape = self._view.ddshape.value

        # Costruisci il grafo orientato basato sugli avvistamenti
        self._model.build_directed_graph(selected_shape, selected_year)

        # Debug: verifica se il numero di nodi è corretto
        num_vertices = self._model.get_num_of_nodes()
        print(f"Numero di vertici nel grafo: {num_vertices}")

        # Ottieni il numero di archi e componenti connesse
        num_edges = self._model.get_num_of_edges()
        num_components = self._model.get_weakly_connected_components()

        # Stampa i risultati
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {num_vertices}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {num_edges}"))
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {num_components} componenti connesse"))

        # Ottieni e stampa la componente connessa più grande
        largest_component = self._model.get_largest_weakly_connected_component()
        self._view.txt_result1.controls.append(
            ft.Text(f"La componente connessa più grande è costituita da {len(largest_component)} nodi:"))

        for sighting in largest_component:
            self._view.txt_result1.controls.append(
                ft.Text(
                    f"id:{sighting.id} - {sighting.city} [{sighting.state}], {sighting.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            )

        # Aggiorna la vista
        self._view.update_page()

    def handle_path(self, e):
        pass
