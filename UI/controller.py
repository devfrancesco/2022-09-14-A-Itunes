import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        self._view.txt_result.controls.clear()
        minuti = self._view._txt_durata.value
        if minuti is None:
            self._view.create_alert("Inserisci i minuti")
            return
        try:
            floatM = float(minuti)
        except ValueError:
            self._view.create_alert("Inserisci un valore float.")
            return
        self._model.buildGraph(floatM)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nNodes}, Archi: {nEdges}"))
        self._view._dd_album.clean()
        self.fillDDAlbum()
        self._view.update_page()

    def handle_analisi_componente(self, e):
        self._view.txt_result.controls.clear()
        album = self._view._dd_album.value #id in str
        if album is None:
            self._view.create_alert("Seleziona un album")
            return
        album_name = self._model.getAlbumName(album)
        dimensione, durata = self._model.getInfoConnessa(album)
        if dimensione == 0:
            self._view.txt_result.controls.append(ft.Text("Nessuna componente connessa trovata"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Componente connesssa - {album_name}"))
        self._view.txt_result.controls.append(ft.Text(f"Dimensione: {dimensione}, Durata: {durata}"))
        self._view.update_page()


    def handle_set_album(self, e):
        self._view.txt_result.controls.clear()
        album = self._view._dd_album.value  # id in str
        if album is None:
            self._view.create_alert("Seleziona un album")
            return
        minuti = self._view._txt_soglia.value
        if minuti is None:
            self._view.create_alert("Seleziona un valore float")
            return
        try:
            floatM = float(minuti)
        except ValueError:
            self._view.create_alert("Seleziona un valore float")
            return
        album_name = self._model.getAlbumName(album)
        bestPath = self._model.getMaxPath(album_name, floatM)
        if bestPath == []:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino massimo"))
            self._view.update_page()
            return
        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{a}"))
        self._view.update_page()

    def fillDDAlbum(self):
        album = self._model._album
        for a in album:
            self._view._dd_album.options.append(ft.dropdown.Option(key=a.AlbumId, text=a)) #id è salvato come str
        self._view.update_page()