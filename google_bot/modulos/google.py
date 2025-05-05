from googlesearch import search

def busqueda(query, results=10):
    return list(search(query, num_results=results))