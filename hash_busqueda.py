import time

class HashBusqueda:
    def __init__(self):
        self.tabla_hash = {}

    def insertar(self, clave, valor):
        if clave not in self.tabla_hash:
            self.tabla_hash[clave] = valor
            return True
        return False  # ya existe la clave

    def buscar(self, clave):
        inicio = time.time()
        valor = self.tabla_hash.get(clave, None)
        fin = time.time()
        tiempo = fin - inicio
        return valor, tiempo

    def eliminar(self, clave):
        if clave in self.tabla_hash:
            del self.tabla_hash[clave]
            return True
        return False

    def mostrar_todo(self):
        if not self.tabla_hash:
            print("La tabla está vacía.")
        else:
            print("Contenido de la tabla hash:")
            for clave, valor in self.tabla_hash.items():
                print(f"Clave: {clave}, Valor: {valor}")
