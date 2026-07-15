# modulos/datos_iniciales.py
# Crea una Tienda ya precargada con productos, clientes y vendedores.
# Como todo vive en memoria, estos datos se cargan cada vez que arranca el programa.

from modulos.tienda import Tienda


def crear_tienda_demo():
    """Devuelve una Tienda lista para usar con datos de ejemplo."""
    tienda = Tienda()

    # --- PRODUCTOS (alguno con stock bajo para mostrar la alerta) ---
    #               nombre                 categoria      precio  stock  min
    tienda.agregar_producto("Laptop HP 15",        "Computo",      2499.90, 8,  3)
    tienda.agregar_producto("Mouse Inalambrico",   "Accesorios",     59.90, 4,  5)  # bajo
    tienda.agregar_producto("Teclado Mecanico",    "Accesorios",    189.00, 12, 4)
    tienda.agregar_producto("Monitor 24 pulgadas", "Computo",       699.50, 6,  3)
    tienda.agregar_producto("Audifonos Gamer",     "Audio",         129.90, 2,  5)  # bajo
    tienda.agregar_producto("Cargador USB-C",      "Accesorios",     45.00, 30, 8)
    tienda.agregar_producto("Disco SSD 1TB",       "Almacenamiento", 320.00, 10, 4)
    tienda.agregar_producto("Webcam Full HD",      "Accesorios",    149.90, 5,  5)  # bajo

    # --- CLIENTES ---
    #              nombre              dni/ruc      telefono     email
    tienda.agregar_cliente("Ana Torres",      "70111222", "999-111-222", "ana@correo.com")
    tienda.agregar_cliente("Carlos Mendoza",  "70333444", "988-333-444", "carlos@correo.com")
    tienda.agregar_cliente("Comercial SAC",   "20512345678", "01-555-7788", "ventas@comercial.pe")

    # --- VENDEDORES ---
    #               nombre           codigo    telefono
    tienda.agregar_vendedor("Pedro Salas",  "VEN-01", "900-000-001")
    tienda.agregar_vendedor("Lucia Ramos",  "VEN-02", "900-000-002")

    # --- VENTAS DE EJEMPLO ---
    # Se precargan para que los reportes y el analisis (pandas/numpy) muestren
    # resultados desde el primer arranque. Formato: (cliente, vendedor, metodo, items)
    # donde items = [(id_producto, cantidad), ...].
    _registrar_venta(tienda, 1, 1, "efectivo",      [(1, 1), (3, 2)])   # Laptop + Teclado
    _registrar_venta(tienda, 2, 2, "tarjeta",       [(4, 1), (6, 2)])   # Monitor + Cargador
    _registrar_venta(tienda, 3, 1, "transferencia", [(7, 2)])           # SSD
    _registrar_venta(tienda, 1, 2, "efectivo",      [(5, 1), (2, 1)])   # Audifonos + Mouse
    _registrar_venta(tienda, 2, 1, "tarjeta",       [(6, 3), (8, 1)])   # Cargador + Webcam
    _registrar_venta(tienda, 3, 2, "efectivo",      [(1, 1)])           # Laptop

    return tienda


def _registrar_venta(tienda, id_cliente, id_vendedor, metodo, items):
    """Ayudante: arma y registra una venta a partir de ids (para datos demo)."""
    cliente  = tienda.obtener_cliente(id_cliente)
    vendedor = tienda.obtener_vendedor(id_vendedor)
    carrito  = [{"producto": tienda.obtener_producto(pid), "cantidad": cant}
                for pid, cant in items]
    return tienda.registrar_venta(cliente, vendedor, carrito, metodo)
