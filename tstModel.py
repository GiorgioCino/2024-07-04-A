from model.modello import Model

mdl = Model()
mdl.build_graph2(2004, 'disk')
print (f"Grafo contiene {mdl.getNumNodes()} nodi e {mdl.getNumEdges()} archi")