# main.py
# Sistema de Ventas - UTP
# 100% en memoria (listas/arrays + POO). SIN base de datos.
# Los datos se cargan al iniciar (datos_iniciales) y se pierden al cerrar.

from datetime import datetime

from modulos.datos_iniciales import crear_tienda_demo
from modulos.personas        import demo_polimorfismo
from modulos.constantes      import METODOS_PAGO, RANGO_IDS   # TUPLAS del sistema
from modulos                 import analitica                 # pandas + numpy
from utils.consola           import (encabezado, separador, confirmar,
                                     pedir_entero, pedir_decimal,
                                     imprimir_tabla, pausa)


# =====================================================
#  MENU PRINCIPAL
# =====================================================
def mostrar_menu():
    separador("=", 50)
    print("        SISTEMA DE VENTAS  -  UTP")
    separador("=", 50)
    print("   1. Gestionar productos")
    print("   2. Gestionar clientes")
    print("   3. Registrar venta")
    print("   4. Historial de ventas")
    print("   5. Inventario / stock")
    print("   6. Buscar producto o cliente")
    print("   7. Reportes")
    print("   8. Vendedores")
    print("   9. Demo POO (polimorfismo)")
    print("  10. Analisis de datos (pandas + numpy)")
    print("   0. Salir")
    separador("=", 50)


def main():
    tienda = crear_tienda_demo()          # <-- la Tienda con datos iniciales

    print("\n  Bienvenido al Sistema de Ventas - UTP")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    alertas_al_iniciar(tienda)

    while True:
        print()
        mostrar_menu()
        op = input("   Seleccione una opcion: ").strip()

        if   op == "1": menu_productos(tienda)
        elif op == "2": menu_clientes(tienda)
        elif op == "3": menu_registrar_venta(tienda); pausa()
        elif op == "4": menu_historial(tienda)
        elif op == "5": menu_inventario(tienda)
        elif op == "6": menu_busqueda(tienda); pausa()
        elif op == "7": menu_reportes(tienda)
        elif op == "8": menu_vendedores(tienda)
        elif op == "9": demo_polimorfismo(); pausa()
        elif op == "10": menu_analitica(tienda)
        elif op == "0":
            if confirmar("  Desea salir?"):
                print("\n  Hasta luego.\n")
                break
        else:
            print("  [!] Opcion invalida.")


# =====================================================
#  PRODUCTOS
# =====================================================
def menu_productos(tienda):
    while True:
        encabezado("Gestionar Productos")
        print("  1. Listar productos")
        print("  2. Agregar producto")
        print("  3. Buscar producto")
        print("  4. Eliminar producto")
        print("  0. Volver")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            _listar_productos(tienda)
        elif op == "2":
            _agregar_producto(tienda)
        elif op == "3":
            termino = input("  Nombre o ID: ").strip()
            res = tienda.buscar_productos(termino)
            if res:
                for p in res:
                    print(" ", p.mostrar())
            else:
                print("  No se encontro ningun producto.")
        elif op == "4":
            _eliminar_producto(tienda)
        elif op == "0":
            break
        else:
            print("  [!] Opcion invalida.")
        pausa()


def _listar_productos(tienda):
    encabezado("Listado de Productos")
    prods = tienda.listar_productos()
    if not prods:
        print("  No hay productos registrados.")
        return
    for p in prods:
        print(" ", p.mostrar())
    print(f"\n  Total: {len(prods)} producto(s)")


def _agregar_producto(tienda):
    encabezado("Agregar Producto")
    nombre    = input("  Nombre     : ").strip()
    categoria = input("  Categoria  : ").strip()
    precio    = pedir_decimal("  Precio S/  : ")
    stock     = pedir_entero("  Stock      : ", 0, 99999)
    stock_min = pedir_entero("  Stock min. : ", 0, 99999)
    p = tienda.agregar_producto(nombre, categoria, precio, stock, stock_min)
    print(f"\n  [OK] Producto '{p.nombre}' creado con ID {p.id_prod}.")


def _eliminar_producto(tienda):
    encabezado("Eliminar Producto")
    _listar_productos(tienda)
    id_prod = pedir_entero("\n  ID a eliminar: ")
    if confirmar(f"  Eliminar producto ID {id_prod}?"):
        if tienda.eliminar_producto(id_prod):
            print("  [OK] Producto eliminado (baja logica).")
        else:
            print("  [!] No existe ese producto.")


# =====================================================
#  CLIENTES
# =====================================================
def menu_clientes(tienda):
    while True:
        encabezado("Gestionar Clientes")
        print("  1. Listar clientes")
        print("  2. Agregar cliente")
        print("  3. Buscar cliente")
        print("  0. Volver")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            _listar_clientes(tienda)
        elif op == "2":
            _agregar_cliente(tienda)
        elif op == "3":
            termino = input("  Nombre o DNI/RUC: ").strip()
            res = tienda.buscar_clientes(termino)
            if res:
                for c in res:
                    print(" ", c.mostrar_info())
            else:
                print("  No se encontro ningun cliente.")
        elif op == "0":
            break
        else:
            print("  [!] Opcion invalida.")
        pausa()


def _listar_clientes(tienda):
    encabezado("Listado de Clientes")
    clientes = tienda.listar_clientes()
    if not clientes:
        print("  No hay clientes registrados.")
        return
    filas = [[c.id_cliente, c.nombre, c.dni_o_ruc, c.telefono] for c in clientes]
    imprimir_tabla(["ID", "Nombre", "DNI/RUC", "Telefono"], filas)


def _agregar_cliente(tienda):
    encabezado("Agregar Cliente")
    nombre    = input("  Nombre completo : ").strip()
    dni       = input("  DNI/RUC         : ").strip()
    telefono  = input("  Telefono        : ").strip()
    email     = input("  Email           : ").strip()
    direccion = input("  Direccion       : ").strip()
    cli = tienda.agregar_cliente(nombre, dni, telefono, email, direccion)
    if cli:
        print(f"\n  [OK] Cliente '{cli.nombre}' registrado con ID {cli.id_cliente}.")
    else:
        print(f"  [!] Ya existe un cliente con DNI/RUC {dni}.")


# =====================================================
#  VENTAS
# =====================================================
def menu_registrar_venta(tienda):
    encabezado("Registrar Venta")

    # 1. Cliente
    clientes = tienda.listar_clientes()
    if not clientes:
        print("  [!] No hay clientes. Registre uno primero.")
        return
    print("  -- Clientes --")
    for c in clientes:
        print(f"  {c.id_cliente}. {c.nombre} - {c.dni_o_ruc}")
    id_min, id_max = RANGO_IDS               # desempaquetado de TUPLA
    cid = pedir_entero("\n  ID de cliente: ", id_min, id_max)
    cliente = tienda.obtener_cliente(cid)
    if not cliente:
        print("  [!] Cliente no encontrado."); return

    # 2. Vendedor
    vendedores = tienda.listar_vendedores()
    if not vendedores:
        print("  [!] No hay vendedores registrados."); return
    print("\n  -- Vendedores --")
    for v in vendedores:
        print(f"  {v.id_vendedor}. {v.nombre} ({v.codigo})")
    vid = pedir_entero("\n  ID de vendedor: ", id_min, id_max)
    vendedor = tienda.obtener_vendedor(vid)
    if not vendedor:
        print("  [!] Vendedor no encontrado."); return

    # 3. Items (lista/array del carrito)
    items = []
    while True:
        print("\n  -- Productos disponibles --")
        for p in tienda.listar_productos():
            print(" ", p.mostrar())
        id_prod = pedir_entero("\n  ID de producto (0 para terminar): ", 0, 99999)
        if id_prod == 0:
            if not items:
                print("  [!] Debe agregar al menos un producto.")
                continue
            break
        prod = tienda.obtener_producto(id_prod)
        if not prod:
            print("  [!] Producto no encontrado.")
            continue
        # cuanto de este producto ya esta en el carrito
        ya_en_carrito = sum(it["cantidad"] for it in items
                            if it["producto"].id_prod == prod.id_prod)
        disponible = prod.stock - ya_en_carrito
        if disponible <= 0:
            print(f"  [!] Sin stock disponible para '{prod.nombre}'.")
            continue
        cantidad = pedir_entero(f"  Cantidad (max {disponible}): ", 1, disponible)
        items.append({"producto": prod, "cantidad": cantidad})
        print(f"  [OK] '{prod.nombre}' x{cantidad} agregado.")

    # 4. Metodo de pago (se recorre la TUPLA constante METODOS_PAGO)
    print("\n  Metodos de pago:")
    for i, m in enumerate(METODOS_PAGO, start=1):     # enumerar la tupla
        print(f"    {i}. {m.capitalize()}")
    opcion = pedir_entero("  Seleccione metodo: ", 1, len(METODOS_PAGO))
    metodo = METODOS_PAGO[opcion - 1]                 # indexar la tupla

    # 5. Confirmar y registrar
    total = sum(it["producto"].precio * it["cantidad"] for it in items)
    print(f"\n  Total a pagar: S/ {total:.2f}")
    if confirmar("  Confirmar venta?"):
        venta = tienda.registrar_venta(cliente, vendedor, items, metodo)
        if venta:
            print("\n" + venta.mostrar_comprobante())
            print(f"\n  [OK] Venta #{venta.id_venta} registrada.")
        else:
            print("  [!] No se pudo registrar (stock insuficiente).")
    else:
        print("  [X] Venta cancelada.")


def menu_historial(tienda):
    while True:
        encabezado("Historial de Ventas")
        print("  1. Ver todas las ventas")
        print("  2. Ver detalle de una venta")
        print("  3. Anular una venta")
        print("  0. Volver")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            ventas = tienda.listar_ventas()
            if not ventas:
                print("  No hay ventas registradas.")
            for v in ventas:
                print(f"  #{v.id_venta}  {v.fecha_str()}  "
                      f"Cliente: {v.cliente.nombre:<16} "
                      f"Vend: {v.vendedor.nombre:<14} "
                      f"S/{v.total():>9.2f}  [{v.estado}]")
        elif op == "2":
            vid = pedir_entero("  ID de venta: ")
            v = tienda.obtener_venta(vid)
            if v:
                print("\n" + v.mostrar_comprobante())
            else:
                print("  [!] Venta no encontrada.")
        elif op == "3":
            vid = pedir_entero("  ID de venta a anular: ")
            if confirmar(f"  Anular venta #{vid}?"):
                r = tienda.anular_venta(vid)
                if r == "ok":
                    print(f"  [OK] Venta #{vid} anulada y stock restituido.")
                elif r == "ya_anulada":
                    print("  [!] La venta ya estaba anulada.")
                else:
                    print("  [!] Venta no encontrada.")
        elif op == "0":
            break
        else:
            print("  [!] Opcion invalida.")
        pausa()


# =====================================================
#  INVENTARIO
# =====================================================
def alertas_al_iniciar(tienda):
    bajos = tienda.productos_stock_bajo()
    if bajos:
        print(f"\n  [!] ALERTA: {len(bajos)} producto(s) con stock bajo:")
        for p in bajos:
            print(f"      - {p.nombre} (stock: {p.stock}, minimo: {p.stock_minimo})")


def menu_inventario(tienda):
    while True:
        encabezado("Inventario / Stock")
        print("  1. Ver stock actual")
        print("  2. Ver alertas de stock bajo")
        print("  3. Ajustar stock manualmente")
        print("  0. Volver")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            encabezado("Stock Actual")
            for p in tienda.listar_productos():
                print(" ", p.mostrar())
        elif op == "2":
            bajos = tienda.productos_stock_bajo()
            if not bajos:
                print("  [OK] Todos los productos tienen stock suficiente.")
            for p in bajos:
                print(f"  {p.nombre:<22} stock: {p.stock}  min: {p.stock_minimo}")
        elif op == "3":
            _ajustar_stock(tienda)
        elif op == "0":
            break
        else:
            print("  [!] Opcion invalida.")
        pausa()


def _ajustar_stock(tienda):
    encabezado("Ajuste Manual de Stock")
    for p in tienda.listar_productos():
        print(" ", p.mostrar())
    id_prod = pedir_entero("\n  ID del producto: ")
    print("  Positivo = entrada, negativo = salida.")
    try:
        cantidad = int(input("  Cantidad: "))
    except ValueError:
        print("  [!] Cantidad invalida.")
        return
    if confirmar(f"  Ajustar stock en {cantidad:+d}?"):
        if tienda.ajustar_stock(id_prod, cantidad):
            print("  [OK] Ajuste registrado.")
        else:
            print("  [!] No se pudo ajustar (producto inexistente o stock negativo).")


# =====================================================
#  VENDEDORES
# =====================================================
def menu_vendedores(tienda):
    while True:
        encabezado("Vendedores")
        print("  1. Listar vendedores")
        print("  2. Agregar vendedor")
        print("  0. Volver")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            for v in tienda.listar_vendedores():
                print(" ", v.mostrar_info())
        elif op == "2":
            nombre   = input("  Nombre  : ").strip()
            codigo   = input("  Codigo  : ").strip()
            telefono = input("  Telefono: ").strip()
            v = tienda.agregar_vendedor(nombre, codigo, telefono)
            print(f"  [OK] Vendedor '{v.nombre}' creado con ID {v.id_vendedor}.")
        elif op == "0":
            break
        else:
            print("  [!] Opcion invalida.")
        pausa()


# =====================================================
#  BUSQUEDA RAPIDA
# =====================================================
def menu_busqueda(tienda):
    encabezado("Busqueda Rapida")
    termino = input("  Buscar nombre, ID o DNI: ").strip()
    print("\n  -- Productos --")
    prods = tienda.buscar_productos(termino)
    if prods:
        for p in prods:
            print(" ", p.mostrar())
    else:
        print("  (sin coincidencias)")
    print("\n  -- Clientes --")
    clis = tienda.buscar_clientes(termino)
    if clis:
        for c in clis:
            print(" ", c.mostrar_info())
    else:
        print("  (sin coincidencias)")


# =====================================================
#  REPORTES
# =====================================================
def menu_reportes(tienda):
    while True:
        encabezado("Reportes")
        print("  1. Ventas por periodo")
        print("  2. Productos mas vendidos")
        print("  3. Cliente top")
        print("  4. Ranking de vendedores")
        print("  5. Matriz ventas: categoria x metodo de pago")
        print("  0. Volver")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            fi = input("  Fecha inicio (YYYY-MM-DD): ").strip()
            ff = input("  Fecha fin    (YYYY-MM-DD): ").strip()
            r = tienda.reporte_periodo(fi or None, ff or None)
            print(f"\n  Ventas: {r['total_ventas']}  |  "
                  f"Ingresos: S/ {r['ingresos']:.2f}")
        elif op == "2":
            ranking = tienda.productos_mas_vendidos()
            if not ranking:
                print("  Sin ventas aun.")
            else:
                filas = [[i + 1, prod.nombre, unidades]
                         for i, (prod, unidades) in enumerate(ranking)]
                imprimir_tabla(["#", "Producto", "Unidades"], filas)
        elif op == "3":
            top = tienda.cliente_top()
            if top:
                print(f"\n  {top[0].nombre} - S/ {top[1]:.2f}")
            else:
                print("  Sin datos aun.")
        elif op == "4":
            ranking = tienda.ranking_vendedores()
            filas = [[i + 1, v.nombre, v.ventas_realizadas,
                      f"S/ {v.monto_acumulado:.2f}"]
                     for i, v in enumerate(ranking)]
            imprimir_tabla(["#", "Vendedor", "Ventas", "Acumulado"], filas)
        elif op == "5":
            _matriz_categoria_pago(tienda)
        elif op == "0":
            break
        else:
            print("  [!] Opcion invalida.")
        pausa()


def _matriz_categoria_pago(tienda):
    """Imprime la MATRIZ (array 2D) de ventas: categoria x metodo de pago."""
    encabezado("Matriz: Categoria x Metodo de Pago")
    categorias, metodos, matriz, tot_fila, tot_col = \
        tienda.matriz_ventas_categoria_pago()

    if not categorias:
        print("  No hay productos/categorias.")
        return

    # cabecera: una columna por metodo de pago + columna TOTAL
    headers = ["Categoria"] + [m.capitalize() for m in metodos] + ["TOTAL"]
    filas = []
    for i, cat in enumerate(categorias):
        fila = [cat]
        fila += [f"{matriz[i][j]:.2f}" for j in range(len(metodos))]   # celdas
        fila.append(f"{tot_fila[i]:.2f}")                              # total fila
        filas.append(fila)

    # ultima fila: totales por columna
    fila_total = ["TOTAL"] + [f"{tc:.2f}" for tc in tot_col]
    fila_total.append(f"{sum(tot_col):.2f}")
    filas.append(fila_total)

    imprimir_tabla(headers, filas)
    print("\n  (Cada celda es un monto en S/. La estructura interna es una")
    print("   matriz = lista de listas [[...],[...]] -> array 2D.)")


# =====================================================
#  ANALISIS DE DATOS  (pandas + numpy)
# =====================================================
def menu_analitica(tienda):
    # El DataFrame se construye una vez a partir de las listas en memoria.
    df = analitica.ventas_a_dataframe(tienda)
    while True:
        encabezado("Analisis de Datos  (pandas + numpy)")
        if df.empty:
            print("  [!] Aun no hay ventas registradas para analizar.")
            return
        print("  1. Ver datos (DataFrame de pandas)")
        print("  2. Resumen estadistico (numpy)")
        print("  3. Ventas por categoria")
        print("  4. Ventas por vendedor")
        print("  5. Ventas por metodo de pago")
        print("  6. Tabla dinamica: categoria x metodo (pivot)")
        print("  7. Top productos")
        print("  8. Exportar a CSV")
        print("  9. Demo programacion funcional")
        print("  0. Volver")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            encabezado("DataFrame de ventas (formato tidy)")
            print(df.to_string(index=False))
            print(f"\n  Filas: {len(df)}  |  Columnas: {len(df.columns)}")
        elif op == "2":
            r = analitica.resumen_numpy(df)
            encabezado("Resumen estadistico del ticket (numpy)")
            print(f"  N de ventas       : {r['n_ventas']}")
            print(f"  Ingreso total     : S/ {r['ingreso_total']:.2f}")
            print(f"  Ticket promedio   : S/ {r['ticket_promedio']:.2f}")
            print(f"  Ticket mediana    : S/ {r['ticket_mediana']:.2f}")
            print(f"  Desviacion estand.: S/ {r['desviacion']:.2f}")
            print(f"  Ticket minimo     : S/ {r['ticket_min']:.2f}")
            print(f"  Ticket maximo     : S/ {r['ticket_max']:.2f}")
            print(f"  Percentil 25 / 75 : S/ {r['p25']:.2f}  /  S/ {r['p75']:.2f}")
        elif op == "3":
            encabezado("Ventas por categoria (pandas groupby)")
            print(analitica.ventas_por_categoria(df).to_string(index=False))
        elif op == "4":
            encabezado("Ventas por vendedor (pandas groupby)")
            print(analitica.ventas_por_vendedor(df).to_string(index=False))
        elif op == "5":
            encabezado("Ventas por metodo de pago (pandas groupby)")
            print(analitica.ventas_por_metodo(df).to_string(index=False))
        elif op == "6":
            encabezado("Tabla dinamica: categoria x metodo (pivot_table)")
            print(analitica.tabla_dinamica_categoria_metodo(df).to_string())
        elif op == "7":
            encabezado("Top productos (pandas)")
            print(analitica.top_productos(df).to_string(index=False))
        elif op == "8":
            ruta = analitica.exportar_csv(df, "reporte_ventas.csv")
            print(f"  [OK] Exportado a: {ruta}")
        elif op == "9":
            _demo_funcional(tienda)
        elif op == "0":
            break
        else:
            print("  [!] Opcion invalida.")
        pausa()


def _demo_funcional(tienda):
    """Muestra el paradigma funcional en accion (map, filter, reduce, lambda)."""
    encabezado("Programacion Funcional en accion")
    total = analitica.ingreso_total_funcional(tienda.ventas)
    print(f"  reduce+map+filter -> ingreso total: S/ {total:.2f}")

    nombres = analitica.nombres_clientes_mayuscula(tienda.clientes)
    print(f"  map+lambda -> clientes en MAYUSCULA: {nombres}")

    caros = analitica.productos_caros(tienda.productos, 300)
    print(f"  filter+lambda -> productos >= S/300: "
          f"{[p.nombre for p in caros]}")

    por_metodo = analitica.ingresos_por_metodo_funcional(tienda.ventas)
    print("  comprehension+reduce -> ingresos por metodo:")
    for metodo, monto in por_metodo.items():
        print(f"      {metodo:<15} S/ {monto:.2f}")


if __name__ == "__main__":
    main()
