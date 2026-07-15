# utils/consola.py
# Helpers de presentacion en consola. Sin emojis (en Windows/cp1252 salen como "?").
# Se usan marcas de texto: [OK], [!], [X].


def separador(char="=", ancho=50):
    print(char * ancho)


def encabezado(titulo):
    separador()
    print(f"   {titulo.upper()}")
    separador()


def pedir_entero(mensaje, minimo=1, maximo=9999):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  [!] Ingrese un numero entre {minimo} y {maximo}.")
        except ValueError:
            print("  [!] Entrada invalida. Solo numeros enteros.")


def pedir_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor >= 0:
                return valor
            print("  [!] El valor no puede ser negativo.")
        except ValueError:
            print("  [!] Formato incorrecto. Ejemplo: 99.50")


def confirmar(mensaje):
    resp = input(f"  {mensaje} (s/n): ").strip().lower()
    return resp == "s"


def imprimir_tabla(headers, filas):
    """Imprime una tabla simple alineada por columnas."""
    if not filas:
        print("  (sin datos)")
        return
    anchos = [
        max(len(str(h)), max((len(str(f[i])) for f in filas), default=0))
        for i, h in enumerate(headers)
    ]
    fmt = "  ".join(f"{{:<{a}}}" for a in anchos)
    print("  " + fmt.format(*headers))
    print("  " + "-" * (sum(anchos) + 2 * len(anchos)))
    for fila in filas:
        print("  " + fmt.format(*[str(c) for c in fila]))


def pausa():
    input("\n  ENTER para continuar...")
