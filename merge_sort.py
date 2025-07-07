def merge_sort(lista, clave=lambda x: x):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio], clave)
    derecha = merge_sort(lista[medio:], clave)

    return fusionar(izquierda, derecha, clave)

def fusionar(izquierda, derecha, clave):
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if clave(izquierda[i]) <= clave(derecha[j]):
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado
