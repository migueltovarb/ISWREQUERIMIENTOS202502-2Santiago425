class CineMovie:
    def __init__(self, codigo, pelicula, hora, precio):
        self.codigo = codigo
        self.pelicula = pelicula
        self.hora = hora
        self.precio = precio
        self.boletos_vendidos = 0

    def get_codigo(self):
        return self.codigo

    def mostrar_datos(self):
        print(f"Codigo: {self.codigo}")
        print(f"Pelicula: {self.pelicula}")
        print(f"Hora: {self.hora}")
        print(f"Precio del boleto: ${self.precio}")
        print(f"Boletos vendidos: {self.boletos_vendidos}\n")


class CineMovieTime:
    def __init__(self):
        self.funciones = []
        self.ventas = []

    def registrar_funcion(self, nueva_funcion):
        self.funciones.append(nueva_funcion)
        print("Funcion registrada correctamente.")

    def listar_funciones(self):
        if not self.funciones:
            print("No hay funciones registradas.")
        else:
            print("Funciones disponibles:")
            for f in self.funciones:
                print(f"{f.codigo} | {f.pelicula} | {f.hora} | ${f.precio}")
            print()

    def vender_boletos(self, codigo_funcion, cantidad):
        funcion_encontrada = None
        for f in self.funciones:
            if f.get_codigo() == codigo_funcion:
                funcion_encontrada = f
                break

        if not funcion_encontrada:
            print("Error: la funcion no existe.")
            return

        if cantidad <= 0:
            print("Error: la cantidad debe ser mayor que cero.")
            return

        total = cantidad * float(funcion_encontrada.precio)
        funcion_encontrada.boletos_vendidos += cantidad
        self.ventas.append({
            "codigo": codigo_funcion,
            "pelicula": funcion_encontrada.pelicula,
            "cantidad": cantidad,
            "total": total
        })
        print(f"Venta registrada correctamente. Total de boletos vendidos: {cantidad}")

    def resumen_ventas(self):
        if not self.ventas:
            print("No hay ventas registradas hoy.")
            return

        total_boletos = sum(v["cantidad"] for v in self.ventas)
        total_dinero = sum(v["total"] for v in self.ventas)

        print("\nResumen de ventas del dia:")
        print(f"Total de boletos vendidos: {total_boletos}")
        print(f"Total dinero recaudado: ${total_dinero:.2f}\n")


def menu():
    print("----- CINE MOVIETIME -----")
    print("1. Registrar nueva funcion")
    print("2. Listar funciones disponibles")
    print("3. Vender boletos")
    print("4. Resumen de ventas del dia")
    print("5. Salir")
    while True:
        try:
            opcion = int(input("Seleccione una opcion (1-5): "))
            if 1 <= opcion <= 5:
                return opcion
            else:
                print("Opcion invalida.")
        except ValueError:
            print("Ingrese un numero valido.")


cine = CineMovieTime()

opcion = menu()
while opcion != 5:
    if opcion == 1:
        codigo = input("Ingrese el codigo de la funcion: ").upper()
        pelicula = input("Ingrese el nombre de la pelicula: ")
        hora = input("Ingrese la hora de la funcion (HH:MM): ")

        while True:
            try:
                precio = float(input("Ingrese el precio del boleto: "))
                if precio <= 0:
                    print("El precio debe ser mayor que cero.")
                    continue
                break
            except ValueError:
                print("Ingrese un valor numerico valido para el precio.")

        nueva_funcion = CineMovie(codigo, pelicula, hora, precio)
        cine.registrar_funcion(nueva_funcion)

    elif opcion == 2:
        cine.listar_funciones()

    elif opcion == 3:
        codigo = input("Ingrese el codigo de la funcion: ").upper()
        try:
            cantidad = int(input("Ingrese la cantidad de boletos: "))
        except ValueError:
            cantidad = 0
            print("Debe ingresar un numero valido.")
        cine.vender_boletos(codigo, cantidad)

    elif opcion == 4:
        cine.resumen_ventas()

    opcion = menu()
