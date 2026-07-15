# modulos/venta.py
# Clase Venta. Cada venta agrupa una lista de lineas (productos vendidos).
# La venta referencia objetos Cliente y Vendedor (no ids sueltos): POO real.

from datetime import datetime


class LineaVenta:
    """Una linea del comprobante: un producto, su cantidad y su subtotal."""

    def __init__(self, producto, cantidad, precio_unitario):
        self.producto        = producto          # objeto Producto
        self.cantidad        = cantidad
        self.precio_unitario = precio_unitario

    def subtotal(self):
        return self.cantidad * self.precio_unitario


class Venta:
    """
    Representa una venta completa.
    Guarda una LISTA de objetos LineaVenta (el "array" de items del carrito).
    """

    def __init__(self, id_venta, cliente, vendedor, metodo_pago):
        self.id_venta    = id_venta
        self.cliente     = cliente               # objeto Cliente
        self.vendedor    = vendedor              # objeto Vendedor
        self.metodo_pago = metodo_pago
        self.fecha       = datetime.now()
        self.estado      = "completada"
        self.lineas      = []                    # lista de LineaVenta

    def agregar_linea(self, producto, cantidad, precio_unitario):
        self.lineas.append(LineaVenta(producto, cantidad, precio_unitario))

    def total(self):
        return sum(linea.subtotal() for linea in self.lineas)

    def anular(self):
        self.estado = "anulada"

    def esta_anulada(self):
        return self.estado == "anulada"

    def fecha_str(self):
        return self.fecha.strftime("%Y-%m-%d %H:%M")

    def mostrar_comprobante(self):
        lineas = []
        lineas.append("  --- COMPROBANTE ---------------------------")
        lineas.append(f"  Venta N : #{self.id_venta}")
        lineas.append(f"  Cliente : {self.cliente.nombre}")
        lineas.append(f"  Vendedor: {self.vendedor.nombre}")
        lineas.append(f"  Fecha   : {self.fecha_str()}")
        lineas.append("  -------------------------------------------")
        for ln in self.lineas:
            lineas.append(f"  {ln.producto.nombre:<24} "
                          f"x{ln.cantidad:>2}  S/ {ln.subtotal():>8.2f}")
        lineas.append("  -------------------------------------------")
        lineas.append(f"  TOTAL                          S/ {self.total():>8.2f}")
        lineas.append(f"  Metodo de pago : {self.metodo_pago}")
        lineas.append(f"  Estado         : {self.estado}")
        lineas.append("  -------------------------------------------")
        return "\n".join(lineas)
