# modulos/constantes.py
# Constantes del sistema definidas como TUPLAS (coleccion inmutable).
# Una tupla se escribe entre parentesis: (a, b, c). A diferencia de una lista,
# NO se puede modificar despues de creada -> ideal para valores fijos del sistema.
# Al centralizarlas aqui, todos los modulos usan la MISMA fuente de datos.


# --- Metodos de pago validos (TUPLA inmutable) ---
# Se recorre en el menu de venta y se valida contra ella en los reportes.
METODOS_PAGO = ("efectivo", "tarjeta", "transferencia")


# --- Estados posibles de una venta (TUPLA) ---
ESTADOS_VENTA = ("completada", "anulada")


# --- Rango de IDs permitido al pedir un id por consola (TUPLA de 2 valores) ---
# Se "desempaqueta" asi:  minimo, maximo = RANGO_IDS
RANGO_IDS = (1, 99999)
