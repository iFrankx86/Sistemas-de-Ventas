# modulos/producto.py
# Clase Producto. Cada producto es un objeto guardado en una lista (self.productos)
# dentro de la clase Tienda. No hay base de datos: todo vive en memoria.


class Producto:
    """Representa un producto del catalogo de la tienda."""

    def __init__(self, id_prod, nombre, categoria, precio, stock, stock_minimo=5):
        self.id_prod      = id_prod
        self.nombre       = nombre
        self.categoria    = categoria
        self.precio       = precio
        self.stock        = stock
        self.stock_minimo = stock_minimo
        self.activo       = True

    # ----- consultas -----
    def tiene_stock_bajo(self):
        return self.stock <= self.stock_minimo

    def hay_stock(self, cantidad):
        return self.stock >= cantidad

    # ----- operaciones sobre el stock -----
    def descontar(self, cantidad):
        """Resta del stock. Devuelve False si no alcanza (evita sobreventa)."""
        if cantidad <= 0 or cantidad > self.stock:
            return False
        self.stock -= cantidad
        return True

    def reponer(self, cantidad):
        """Suma al stock (compras, anulaciones, ajustes)."""
        self.stock += cantidad

    # ----- presentacion -----
    def mostrar(self):
        alerta = "  [!] BAJO" if self.tiene_stock_bajo() else ""
        return (f"[{self.id_prod}] {self.nombre:<22} "
                f"S/{self.precio:>8.2f}  "
                f"Stock:{self.stock:>4}{alerta}  "
                f"Cat: {self.categoria}")
