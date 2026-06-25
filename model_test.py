from model.model import Model

mdl = Model()
mdl.buildGraph(60)
n, e = mdl.getGraphDetails()
print(f"Nodi : {n}, Archi: {e}")