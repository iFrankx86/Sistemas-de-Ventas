# modulos/analitica.py
# =====================================================================
#  ANALISIS Y TRATAMIENTO DE DATOS  ->  pandas + numpy
# =====================================================================
# Este modulo toma las LISTAS en memoria de la Tienda y las convierte en
# un DataFrame de pandas para analizarlas. Incluye:
#   - Limpieza y transformacion de datos (normalizar texto, fechas, numeros).
#   - Analisis con numpy (estadistica: media, mediana, desviacion, percentiles).
#   - Analisis con pandas (groupby, pivot_table / tabla dinamica).
#   - Exportacion a CSV (tratamiento/persistencia del reporte).
#
# IMPORTANTE: todo sigue siendo EN MEMORIA. pandas y numpy solo PROCESAN los
# datos; no hay base de datos. El DataFrame se construye "al vuelo" cada vez.
#
# Ademas, al final hay una seccion de PROGRAMACION FUNCIONAL (paradigma
# funcional): funciones puras que usan map, filter, reduce, lambda y
# comprehensions, sin bucles ni efectos secundarios.
# =====================================================================

from functools import reduce
import numpy as np
import pandas as pd

# Columnas del DataFrame (orden fijo, legible).
COLUMNAS = [
    "venta_id", "fecha", "cliente", "vendedor", "metodo_pago", "estado",
    "categoria", "producto", "cantidad", "precio_unitario", "subtotal",
]


# =====================================================================
#  1) CONSTRUCCION DEL DATAFRAME (desde las listas en memoria)
# =====================================================================
def ventas_a_dataframe(tienda):
    """
    Convierte las ventas (objetos en memoria) en un DataFrame de pandas.
    Cada LINEA de cada venta se vuelve una FILA (formato 'largo'/tidy).
    Se usa una comprehension anidada (estilo funcional) para aplanar.
    """
    filas = [
        {
            "venta_id":        v.id_venta,
            "fecha":           v.fecha,
            "cliente":         v.cliente.nombre,
            "vendedor":        v.vendedor.nombre,
            "metodo_pago":     v.metodo_pago,
            "estado":          v.estado,
            "categoria":       ln.producto.categoria,
            "producto":        ln.producto.nombre,
            "cantidad":        ln.cantidad,
            "precio_unitario": ln.precio_unitario,
            "subtotal":        ln.subtotal(),
        }
        for v in tienda.ventas      # por cada venta...
        for ln in v.lineas          # ...por cada linea de esa venta
    ]
    df = pd.DataFrame(filas, columns=COLUMNAS)
    return limpiar_dataframe(df)


def limpiar_dataframe(df):
    """
    LIMPIEZA Y TRANSFORMACION de datos (lo que valora la rubrica):
      - Normaliza texto: quita espacios y unifica mayusculas/minusculas.
      - Convierte 'fecha' a tipo datetime real.
      - Fuerza tipos numericos (coerce) y rellena vacios con 0.
      - Crea columnas derivadas ('dia', 'mes') a partir de la fecha.
    Devuelve un DataFrame NUEVO (no modifica el original -> funcion pura).
    """
    if df.empty:
        return df

    df = df.copy()

    # --- normalizar texto ---
    for col in ("cliente", "vendedor", "categoria", "producto"):
        df[col] = df[col].astype(str).str.strip().str.title()
    df["metodo_pago"] = df["metodo_pago"].astype(str).str.strip().str.lower()
    df["estado"]      = df["estado"].astype(str).str.strip().str.lower()

    # --- fechas y numeros (transformacion de tipos) ---
    df["fecha"]           = pd.to_datetime(df["fecha"], errors="coerce")
    df["cantidad"]        = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)
    df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0.0)
    df["subtotal"]        = pd.to_numeric(df["subtotal"], errors="coerce").fillna(0.0)

    # --- columnas derivadas (transformacion) ---
    df["dia"] = df["fecha"].dt.date
    df["mes"] = df["fecha"].dt.to_period("M").astype(str)

    return df


def solo_completadas(df):
    """Filtra el DataFrame para quedarnos con ventas NO anuladas (limpieza)."""
    if df.empty:
        return df
    return df[df["estado"] != "anulada"]


# =====================================================================
#  2) ANALISIS CON NUMPY (estadistica del ticket de venta)
# =====================================================================
def resumen_numpy(df):
    """
    Estadistica descriptiva del 'ticket' (total por venta) usando numpy.
    Primero agrupamos por venta para obtener el total de cada una, y luego
    aplicamos funciones de numpy sobre ese arreglo (np.array).
    Devuelve un diccionario con los indicadores.
    """
    dfc = solo_completadas(df)
    if dfc.empty:
        return {k: 0.0 for k in
                ("n_ventas", "ingreso_total", "ticket_promedio", "ticket_mediana",
                 "desviacion", "ticket_min", "ticket_max", "p25", "p75")}

    # total por venta -> arreglo de numpy
    tickets = dfc.groupby("venta_id")["subtotal"].sum().to_numpy()

    return {
        "n_ventas":        int(tickets.size),
        "ingreso_total":   float(np.sum(tickets)),
        "ticket_promedio": float(np.mean(tickets)),
        "ticket_mediana":  float(np.median(tickets)),
        "desviacion":      float(np.std(tickets)),         # desviacion estandar
        "ticket_min":      float(np.min(tickets)),
        "ticket_max":      float(np.max(tickets)),
        "p25":             float(np.percentile(tickets, 25)),
        "p75":             float(np.percentile(tickets, 75)),
    }


# =====================================================================
#  3) ANALISIS CON PANDAS (agrupaciones y tabla dinamica)
# =====================================================================
def ventas_por_categoria(df):
    """groupby por categoria: suma unidades e ingresos, ordenado por ingresos."""
    dfc = solo_completadas(df)
    if dfc.empty:
        return pd.DataFrame(columns=["categoria", "unidades", "ingresos"])
    return (dfc.groupby("categoria")
               .agg(unidades=("cantidad", "sum"),
                    ingresos=("subtotal", "sum"))
               .sort_values("ingresos", ascending=False)
               .reset_index())


def ventas_por_vendedor(df):
    """groupby por vendedor: cuenta ventas distintas e ingresos generados."""
    dfc = solo_completadas(df)
    if dfc.empty:
        return pd.DataFrame(columns=["vendedor", "ventas", "ingresos"])
    return (dfc.groupby("vendedor")
               .agg(ventas=("venta_id", "nunique"),
                    ingresos=("subtotal", "sum"))
               .sort_values("ingresos", ascending=False)
               .reset_index())


def ventas_por_metodo(df):
    """groupby por metodo de pago: ingresos por cada forma de pago."""
    dfc = solo_completadas(df)
    if dfc.empty:
        return pd.DataFrame(columns=["metodo_pago", "ingresos"])
    return (dfc.groupby("metodo_pago")
               .agg(ingresos=("subtotal", "sum"))
               .sort_values("ingresos", ascending=False)
               .reset_index())


def tabla_dinamica_categoria_metodo(df):
    """
    TABLA DINAMICA (pivot_table): filas=categoria, columnas=metodo de pago,
    valores=suma de subtotales, con totales por fila y columna (margins).
    Es el equivalente en pandas de la 'matriz' hecha a mano en tienda.py.
    """
    dfc = solo_completadas(df)
    if dfc.empty:
        return pd.DataFrame()
    return pd.pivot_table(
        dfc, values="subtotal", index="categoria", columns="metodo_pago",
        aggfunc="sum", fill_value=0.0, margins=True, margins_name="TOTAL",
    )


def top_productos(df, n=5):
    """Los N productos con mas unidades vendidas (groupby + sort + head)."""
    dfc = solo_completadas(df)
    if dfc.empty:
        return pd.DataFrame(columns=["producto", "unidades", "ingresos"])
    return (dfc.groupby("producto")
               .agg(unidades=("cantidad", "sum"),
                    ingresos=("subtotal", "sum"))
               .sort_values("unidades", ascending=False)
               .head(n)
               .reset_index())


# =====================================================================
#  4) EXPORTACION (tratamiento/persistencia del reporte)
# =====================================================================
def exportar_csv(df, ruta="reporte_ventas.csv"):
    """Guarda el DataFrame en un archivo CSV. Devuelve la ruta usada."""
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    return ruta


# =====================================================================
#  5) PROGRAMACION FUNCIONAL (paradigma funcional)
#     Funciones PURAS: reciben datos, devuelven un valor y no modifican nada.
#     Usan map, filter, reduce, lambda y comprehensions (sin bucles for).
# =====================================================================
def ingreso_total_funcional(ventas):
    """
    reduce + map + filter + lambda:
      filter -> descarta anuladas
      map    -> obtiene el total de cada venta
      reduce -> acumula la suma
    """
    completadas = filter(lambda v: not v.esta_anulada(), ventas)   # FILTER
    totales     = map(lambda v: v.total(), completadas)            # MAP
    return reduce(lambda acumulado, x: acumulado + x, totales, 0.0)  # REDUCE


def nombres_clientes_mayuscula(clientes):
    """map + lambda: transforma cada nombre a MAYUSCULAS sin bucle explicito."""
    return list(map(lambda c: c.nombre.upper(), clientes))


def productos_caros(productos, umbral):
    """filter + lambda: se queda solo con productos cuyo precio >= umbral."""
    return list(filter(lambda p: p.precio >= umbral, productos))


def ingresos_por_metodo_funcional(ventas):
    """
    Comprehensions (set y dict) + reduce:
    Devuelve {metodo: ingreso_total} sin usar pandas, en estilo funcional puro.
    """
    completadas = [v for v in ventas if not v.esta_anulada()]        # list comprehension
    metodos     = {v.metodo_pago for v in completadas}               # set comprehension
    return {
        metodo: reduce(lambda a, v: a + v.total(),
                       filter(lambda v: v.metodo_pago == metodo, completadas),
                       0.0)
        for metodo in metodos                                        # dict comprehension
    }
