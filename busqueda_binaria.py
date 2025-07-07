import time

def busqueda_binaria(lista, objetivo, clave=lambda x: x):
    inicio = time.time()
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        valor_medio = clave(lista[medio])
        if valor_medio == objetivo:
            fin = time.time()
            return lista[medio], fin - inicio
        elif valor_medio < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    fin = time.time()
    return None, fin - inicio
