import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDyears(self):
        years = self._model.get_all_years()

        self._view.ddyear.options.clear()

        for year in years:
            self._view.ddyear.options.append(
                ft.dropdown.Option(str(year))
            )

        self._view.ddyear.value = None
        self._view.update_page()

    def fillDDforme(self,anno):
        forme = self._model.get_all_forme(anno)

        self._view.ddshape.options.clear()

        for forma in forme:
            self._view.ddshape.options.append(
                ft.dropdown.Option(str(forma))
            )

        self._view.ddshape.value = None
        self._view.update_page()

    def handleAnnoSelezionato(self, e):
        anno = int(self._view.ddyear.value)
        self.fillDDforme(anno)

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()

        anno = self._view.ddyear.value
        forma = self._view.ddshape.value

        if anno is None:
            self._view.create_alert("Seleziona una anno.")
            return

        if forma is None:
            self._view.create_alert("Seleziona una forma.")
            return


        n_nodi, n_archi = self._model.build_graph(anno,forma)

        # self.fillDDProducts()

        self._view.txt_result1.controls.append(
            ft.Text("Grafo correttamente creato.")
        )


        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di nodi: {n_nodi}")
        )

        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di archi: {n_archi}")
        )

        sizeCompConn = self._model.getInfoCompConnessa()

        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di componenti debolmente connesse: {sizeCompConn}")
        )

        compMaggiore = self._model.getComponenteMaggiore()

        self._view.txt_result1.controls.append(
            ft.Text(f"Componente debolmente connessa di dimensione maggiore: {len(compMaggiore)} nodi")
        )

        for nodo in compMaggiore:
            self._view.txt_result1.controls.append(
                ft.Text(f"Città: {nodo.city} - Data: {nodo.datetime}")
            )

        self._view.update_page()

    def handle_path(self, e):
        pass
