import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self,e):
        anno = self._view._ddAnno.value
        self._model.buildGraph(anno)
        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{Nedges}"))

        bestdriver, best = self._model.getBestDriver()

        self._view.txt_result.controls.append(ft.Text(f"Best driver: {bestdriver}, with score {best}"))
        self._view.update_page()


    def handleCerca(self, e):
        pass

    def fillDDYear(self):
        years = self._model.getAllYears()
        for year in years:
            self._view._ddAnno.options.append(ft.dropdown.Option(year))