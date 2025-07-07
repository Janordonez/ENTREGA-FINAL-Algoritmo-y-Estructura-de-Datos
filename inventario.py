import random
import time
from merge_sort import merge_sort
from busqueda_binaria import busqueda_binaria
from hash_busqueda import HashBusqueda

# Función: generar_producto_realista
# Crea un producto con nombre realista del supermercado,
# cantidad aleatoria entre 1 y 100, y código numérico único.

def generar_producto_realista(codigo_num):
    nombres_productos = [
        "Leche", "Pan", "Huevos", "Arroz", "Fideos", "Azúcar", "Aceite", "Sal",
        "Detergente", "Jabón", "Shampoo", "Galletas", "Cereal", "Queso", "Mantequilla",
        "Yogur", "Refresco", "Agua", "Papel Higiénico", "Servilletas", "Carne", "Pollo",
        "Pescado", "Manzanas", "Bananas", "Tomates", "Papas", "Cebolla", "Zanahorias"
    ]
    nombre = random.choice(nombres_productos)
    cantidad = random.randint(1, 100)
    return {'codigo': codigo_num, 'nombre': nombre, 'cantidad': cantidad}

# Función: guardar_inventarios_txt
# Guarda el inventario original y el inventario ordenado en un archivo de texto.
# El archivo se sobrescribe cada vez que se actualiza o visualiza.

def guardar_inventarios_txt(inventario_original, inventario_ordenado, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        # Sección 1: inventario original
        f.write("INVENTARIO ORIGINAL:\n")
        for producto in inventario_original:
            f.write(f"{producto}\n")
        # Sección 2: inventario ordenado
        f.write("\nINVENTARIO ORDENADO POR CÓDIGO:\n")
        for producto in inventario_ordenado:
            f.write(f"{producto}\n")
    # Este archivo servirá como referencia visual para el usuario

# Función: mostrar_desde_txt
# Lee y muestra el contenido del archivo de inventario al usuario.

def mostrar_desde_txt(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print("El archivo de inventario no existe aún.")

# Inicializamos
inventario = []
tabla_hash = HashBusqueda()

try:
    tam = int(input("Ingrese el tamaño del inventario: "))
except ValueError:
    print("Entrada inválida.")
    exit()

# Generación del inventario según el caso seleccionado
print("\nSeleccione el tipo de caso:")
print("1. Mejor caso (ordenado)")
print("2. Caso promedio (aleatorio)")
print("3. Peor caso (orden inverso)")

try:
    caso = int(input("Ingrese una opción (1-3): "))
except ValueError:
    print("Entrada inválida.")
    exit()

# Crea los datos base
inventario = [generar_producto_realista(i + 1) for i in range(tam)]

# Ordena según el caso
if caso == 1:
    inventario.sort(key=lambda x: x['codigo'])                      # Mejor caso: ordenado
elif caso == 2:
    random.shuffle(inventario)                                      # Caso promedio: aleatorio
elif caso == 3:
    inventario.sort(key=lambda x: x['codigo'], reverse=True)        # Peor caso: orden inverso
else:
    print("Opción inválida. Se usará caso promedio por defecto.")
    random.shuffle(inventario)

# Guarda copia del inventario tal como fue generado
inventario_original = inventario.copy()

# Ordena con Merge Sort para uso posterior y mide el tiempo
inicio_orden = time.time()
inventario_ordenado = merge_sort(inventario.copy(), clave=lambda x: x['codigo'])
fin_orden = time.time()

print(f"Tiempo de ordenamiento (Merge Sort): {fin_orden - inicio_orden:.6f} segundos")

# Se guarda el inventario en un archivo de texto
guardar_inventarios_txt(inventario_original, inventario_ordenado, "inventario.txt")
print("Inventario generado y guardado en 'inventario.txt'.\n")
# Se trabaja con la versión ordenada por defecto
inventario = inventario_ordenado

# Se cargan los productos en la tabla hash para búsqueda rápida
for prod in inventario:
    tabla_hash.insertar(prod['codigo'], prod)

while True:
    print("\nMenú:")
    print("1. Buscar producto")
    print("2. Visualizar inventario")
    print("3. Actualizar producto")
    print("4. Salir")
    
    try:
        opcion = int(input("Seleccione una opción: "))
    except ValueError:
        print("Entrada inválida.")
        continue

    # Opción 1: Buscar producto por código usando Hash y Binaria
    if opcion == 1:
        try:
            codigo = int(input("Ingrese el código del producto a buscar: "))
        except ValueError:
            print("Código inválido.")
            continue

        # Búsqueda por hash
        resultado_hash, tiempo_hash = tabla_hash.buscar(codigo)

        # Búsqueda binaria (sobre inventario ordenado)
        resultado_bin, tiempo_bin = busqueda_binaria(inventario, codigo, clave=lambda x: x['codigo'])

        # Resultados comparativos
        print("\n--- Resultado de Búsqueda ---")
        print(f"Hashing:  {resultado_hash}")
        print(f"Tiempo (hash):    {tiempo_hash:.6f} segundos")
        print(f"Binaria:  {resultado_bin}")
        print(f"Tiempo (binaria): {tiempo_bin:.6f} segundos")

    # Opción 2: Visualizar el inventario desde el archivo .txt
    # También actualiza el archivo sobrescribiéndolo
    elif opcion == 2:
        guardar_inventarios_txt(inventario, merge_sort(inventario.copy(), clave=lambda x: x['codigo']), "inventario.txt")
        print("\n--- Visualización desde 'inventario.txt' ---")
        mostrar_desde_txt("inventario.txt")

    # Opción 3: Actualizar la cantidad de un producto existente
    elif opcion == 3:
        try:
            codigo = int(input("Ingrese el código del producto a actualizar: "))
        except ValueError:
            print("Código inválido.")
            continue

        encontrado = False
        # Recorre el inventario para buscar y actualizar
        for prod in inventario:
            if prod['codigo'] == codigo:
                try:
                    nueva_cantidad = int(input(f"Ingrese nueva cantidad para '{prod['nombre']}': "))
                except ValueError:
                    print("Cantidad inválida.")
                    break
                prod['cantidad'] = nueva_cantidad  # Actualiza la cantidad
                tabla_hash.insertar(prod['codigo'], prod)  # Actualiza también en hash
                encontrado = True
                break

        if encontrado:
            print("Producto actualizado.")
            # El archivo .txt se actualiza con los nuevos datos
            guardar_inventarios_txt(inventario, merge_sort(inventario.copy(), clave=lambda x: x['codigo']), "inventario.txt")
        else:
            print("Producto no encontrado.")

    elif opcion == 4:
        print("Saliendo del programa.")
        break
    
    else:
        print("Opción no válida.")
