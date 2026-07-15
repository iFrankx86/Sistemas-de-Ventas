# modulos/tienda.py
# Clase Tienda: el "cerebro" del sistema. Contiene TODAS las listas en memoria
# (productos, clientes, vendedores, ventas) y todas las operaciones sobre ellas.
# NO usa base de datos: cuando el programa se cierra, los datos se pierden.

from functools import reduce

from modulos.producto   import Producto
from modulos.personas   import Cliente, Vendedor
from modulos.venta      import Venta
from modulos.constantes import METODOS_PAGO   # TUPLA con los metodos de pago


class Tienda:
    """Almacena las listas en memoria y opera sobre ellas (alta, baja, ventas, reportes)."""

    def __init__(self):
        # --- Las "tablas" del sistema, ahora como listas/arrays ---
        self.productos  = []   # lista de objetos Producto
        self.clientes   = []   # lista de objetos Cliente
        self.vendedores = []   # lista de objetos Vendedor
        self.ventas     = []   # lista de objetos Venta

        # --- Contadores para generar ids autoincrementales ---
        self._next_id_producto = 1
        self._next_id_cliente  = 1
        self._next_id_vendedor = 1
        self._next_id_venta    = 1

    # =================================================
    #  PRODUCTOS
    # =================================================
    def agregar_producto(self, nombre, categoria, precio, stock, stock_minimo=5):
        prod = Producto(self._next_id_producto, nombre, categoria,
                        precio, stock, stock_minimo)
        self.productos.append(prod)
        self._next_id_producto += 1
        return prod

    def listar_productos(self, solo_activos=True):
        if solo_activos:
            return [p for p in self.productos if p.activo]
        return list(self.productos)

    def obtener_producto(self, id_prod):
        """Busca un producto por id exacto. Devuelve el objeto o None.
        Estilo funcional: filter + next, sin bucle explicito."""
        return next(
            filter(lambda p: p.id_prod == id_prod and p.activo, self.productos),
            None,
        )

    def buscar_productos(self, termino):
        """Busca por id exacto o por coincidencia parcial de nombre.
        Estilo funcional: filter + lambda sobre la lista en memoria."""
        termino = str(termino).strip().lower()
        if termino == "":
            return []
        coincide = lambda p: p.activo and (
            (termino.isdigit() and p.id_prod == int(termino))
            or termino in p.nombre.lower()
        )
        return list(filter(coincide, self.productos))

    def eliminar_producto(self, id_prod):
        """Baja logica: marca el producto como inactivo."""
        p = self.obtener_producto(id_prod)
        if p:
            p.activo = False
            return True
        return False

    # =================================================
    #  CLIENTES
    # =================================================
    def agregar_cliente(self, nombre, dni_o_ruc, telefono="", email="", direccion=""):
        """Crea un cliente. Devuelve None si el DNI/RUC ya existe."""
        if self.obtener_cliente_por_doc(dni_o_ruc):
            return None
        cli = Cliente(self._next_id_cliente, nombre, dni_o_ruc,
                      telefono, email, direccion)
        self.clientes.append(cli)
        self._next_id_cliente += 1
        return cli

    def listar_clientes(self):
        return list(self.clientes)

    def obtener_cliente(self, id_cliente):
        """Estilo funcional: filter + next, sin bucle explicito."""
        return next(filter(lambda c: c.id_cliente == id_cliente, self.clientes), None)

    def obtener_cliente_por_doc(self, dni_o_ruc):
        """Estilo funcional: filter + next, sin bucle explicito."""
        return next(filter(lambda c: c.dni_o_ruc == dni_o_ruc, self.clientes), None)

    def buscar_clientes(self, termino):
        """Busca por nombre parcial o por DNI/RUC exacto (filter + lambda)."""
        termino = str(termino).strip().lower()
        if termino == "":
            return []
        coincide = lambda c: termino in c.nombre.lower() or termino == c.dni_o_ruc.lower()
        return list(filter(coincide, self.clientes))

    # =================================================
    #  VENDEDORES
    # =================================================
    def agregar_vendedor(self, nombre, codigo, telefono=""):
        v = Vendedor(self._next_id_vendedor, nombre, codigo, telefono)
        self.vendedores.append(v)
        self._next_id_vendedor += 1
        return v

    def listar_vendedores(self):
        return list(self.vendedores)

    def obtener_vendedor(self, id_vendedor):
        """Estilo funcional: filter + next, sin bucle explicito."""
        return next(filter(lambda v: v.id_vendedor == id_vendedor, self.vendedores), None)

    # =================================================
    #  VENTAS
    # =================================================
    def registrar_venta(self, cliente, vendedor, items, metodo_pago):
        """
        items = lista de dicts: [{"producto": objProducto, "cantidad": int}]
        Valida stock de TODOS los items ANTES de tocar nada (evita sobreventa),
        luego descuenta stock, crea la Venta y actualiza cliente y vendedor.
        Devuelve la Venta creada, o None si algo falla.
        """
        if not items:
            return None

        # --- 1) Validar stock de todo el carrito ANTES de confirmar ---
        # (se suma por producto por si el mismo aparece dos veces)
        requerido = {}
        for it in items:
            requerido[it["producto"].id_prod] = (
                requerido.get(it["producto"].id_prod, 0) + it["cantidad"]
            )
        for it in items:
            prod = it["producto"]
            if not prod.hay_stock(requerido[prod.id_prod]):
                return None   # no alcanza el stock -> se cancela toda la venta

        # --- 2) Crear la venta y sus lineas ---
        venta = Venta(self._next_id_venta, cliente, vendedor, metodo_pago)
        for it in items:
            prod = it["producto"]
            prod.descontar(it["cantidad"])                      # baja el stock del objeto
            venta.agregar_linea(prod, it["cantidad"], prod.precio)

        # --- 3) Actualizar acumulados de cliente y vendedor (POO) ---
        cliente.agregar_compra(venta.total())
        vendedor.registrar_venta(venta.total())

        self.ventas.append(venta)
        self._next_id_venta += 1
        return venta

    def listar_ventas(self):
        return list(self.ventas)

    def obtener_venta(self, id_venta):
        """Estilo funcional: filter + next, sin bucle explicito."""
        return next(filter(lambda v: v.id_venta == id_venta, self.ventas), None)

    def anular_venta(self, id_venta):
        """Marca anulada, repone stock de cada producto y revierte acumulados."""
        venta = self.obtener_venta(id_venta)
        if not venta:
            return "no_encontrada"
        if venta.esta_anulada():
            return "ya_anulada"
        for ln in venta.lineas:
            ln.producto.reponer(ln.cantidad)
        venta.vendedor.revertir_venta(venta.total())
        venta.anular()
        return "ok"

    # =================================================
    #  INVENTARIO
    # =================================================
    def productos_stock_bajo(self):
        return [p for p in self.productos if p.activo and p.tiene_stock_bajo()]

    def ajustar_stock(self, id_prod, cantidad):
        """Ajuste manual (+ entrada / - salida). Evita dejar stock negativo."""
        prod = self.obtener_producto(id_prod)
        if not prod:
            return False
        if prod.stock + cantidad < 0:
            return False
        prod.reponer(cantidad)   # reponer suma; con cantidad negativa resta
        return True

    # =================================================
    #  REPORTES
    # =================================================
    def reporte_periodo(self, fecha_inicio=None, fecha_fin=None):
        """
        fecha_inicio / fecha_fin: strings 'YYYY-MM-DD' (o None = todas).
        Compara por DIA, asi la venta del propio dia SI entra en el rango.
        Solo cuenta ventas completadas.
        """
        completadas = [v for v in self.ventas if not v.esta_anulada()]
        if fecha_inicio and fecha_fin:
            completadas = [
                v for v in completadas
                if fecha_inicio <= v.fecha.strftime("%Y-%m-%d") <= fecha_fin
            ]
        total_ventas = len(completadas)
        ingresos     = sum(v.total() for v in completadas)
        return {"total_ventas": total_ventas, "ingresos": ingresos}

    def productos_mas_vendidos(self, top_n=5):
        """
        Devuelve [(producto, unidades)] ordenado por unidades vendidas.
        Estilo funcional: se aplana el arbol venta->lineas con una
        comprehension y se acumulan las unidades con reduce (sin bucles
        anidados explicitos). Integrado directamente en el reporte real
        del sistema (menu 7, no una demo aislada).
        """
        lineas = [ln for v in self.ventas if not v.esta_anulada()
                  for ln in v.lineas]

        def acumular(acc, ln):
            pid = ln.producto.id_prod
            _, unidades_prev = acc.get(pid, (ln.producto, 0))
            acc[pid] = (ln.producto, unidades_prev + ln.cantidad)
            return acc

        unidades = reduce(acumular, lineas, {})
        ranking = sorted(unidades.values(), key=lambda x: x[1], reverse=True)
        return ranking[:top_n]

    def cliente_top(self):
        """
        Cliente que mas ha gastado (en ventas no anuladas). Devuelve (cliente, monto).
        Estilo funcional: filter descarta anuladas y reduce acumula el gasto
        por cliente, terminando con max + lambda (sin bucles explicitos).
        """
        completadas = filter(lambda v: not v.esta_anulada(), self.ventas)

        def acumular(acc, v):
            cid = v.cliente.id_cliente
            _, total_prev = acc.get(cid, (v.cliente, 0.0))
            acc[cid] = (v.cliente, total_prev + v.total())
            return acc

        gasto = reduce(acumular, completadas, {})
        if not gasto:
            return None
        return max(gasto.values(), key=lambda x: x[1])

    def ranking_vendedores(self):
        """Vendedores ordenados por monto acumulado. Devuelve lista de Vendedor."""
        return sorted(self.vendedores,
                      key=lambda v: v.monto_acumulado, reverse=True)

    def matriz_ventas_categoria_pago(self):
        """
        Construye una MATRIZ (lista de listas / array 2D) con los montos vendidos.
            filas    = categorias de producto
            columnas = metodos de pago (efectivo, tarjeta, transferencia)
            celda    = total S/ vendido en esa categoria con ese metodo

        Devuelve: (categorias, metodos, matriz, totales_fila, totales_columna)
        """
        # se convierte la TUPLA constante a lista para poder usar .index()
        metodos = list(METODOS_PAGO)

        # 1) categorias unicas que existen en el catalogo (orden estable)
        #    map extrae la categoria de cada producto y dict.fromkeys
        #    elimina duplicados preservando el orden (estilo funcional).
        categorias = list(dict.fromkeys(map(lambda p: p.categoria, self.productos)))

        # 2) matriz de ceros: tantas filas como categorias, 3 columnas
        matriz = [[0.0 for _ in metodos] for _ in categorias]

        # 3) recorrer ventas no anuladas y acumular en la celda correspondiente
        for v in self.ventas:
            if v.esta_anulada():
                continue
            if v.metodo_pago not in metodos:
                continue
            col = metodos.index(v.metodo_pago)
            for ln in v.lineas:
                if ln.producto.categoria in categorias:
                    fila = categorias.index(ln.producto.categoria)
                    matriz[fila][col] += ln.subtotal()

        # 4) totales por fila y por columna (suma de la matriz)
        totales_fila = [sum(fila) for fila in matriz]
        totales_col  = [sum(matriz[f][c] for f in range(len(categorias)))
                        for c in range(len(metodos))]

        return categorias, metodos, matriz, totales_fila, totales_col
