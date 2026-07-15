# modulos/personas.py
# Jerarquia de personas: herencia simple, herencia multiple y polimorfismo.
# Todos los objetos viven en memoria (listas dentro de la clase Tienda).


# =====================================================
#  CLASE BASE
# =====================================================
class Persona:
    """Clase base. Define la interfaz comun para todos los roles."""

    def __init__(self, nombre, telefono):
        self.nombre   = nombre
        self.telefono = telefono

    def mostrar_info(self):          # metodo que se sobreescribe (POLIMORFISMO)
        return f"Nombre: {self.nombre} | Tel: {self.telefono}"

    def tipo(self):
        return "Persona"


# =====================================================
#  HERENCIA SIMPLE  ->  Cliente
# =====================================================
class Cliente(Persona):
    """Hereda de Persona. Agrega DNI/RUC y un historial de compras (lista)."""

    def __init__(self, id_cliente, nombre, dni_o_ruc,
                 telefono="", email="", direccion=""):
        super().__init__(nombre, telefono)   # llama al __init__ de Persona
        self.id_cliente        = id_cliente
        self.dni_o_ruc         = dni_o_ruc
        self.email             = email
        self.direccion         = direccion
        self.historial_compras = []          # array dinamico de montos

    def mostrar_info(self):                  # POLIMORFISMO: sobreescribe Persona
        return (f"[CLIENTE] {self.nombre} | "
                f"DNI/RUC: {self.dni_o_ruc} | Tel: {self.telefono}")

    def tipo(self):
        return "Cliente"

    def agregar_compra(self, monto):
        self.historial_compras.append(monto)

    def total_compras(self):
        return sum(self.historial_compras)


# =====================================================
#  HERENCIA SIMPLE  ->  Vendedor
# =====================================================
class Vendedor(Persona):
    """Hereda de Persona. Empleado que realiza ventas y acumula montos."""

    def __init__(self, id_vendedor, nombre, codigo, telefono=""):
        super().__init__(nombre, telefono)
        self.id_vendedor       = id_vendedor
        self.codigo            = codigo
        self.ventas_realizadas = 0
        self.monto_acumulado   = 0.0

    def mostrar_info(self):                  # POLIMORFISMO
        return (f"[VENDEDOR] {self.nombre} | "
                f"Codigo: {self.codigo} | "
                f"Ventas: {self.ventas_realizadas} | "
                f"Acumulado: S/ {self.monto_acumulado:.2f}")

    def tipo(self):
        return "Vendedor"

    def registrar_venta(self, monto):
        self.ventas_realizadas += 1
        self.monto_acumulado   += monto

    def revertir_venta(self, monto):
        """Se usa al anular una venta de este vendedor."""
        if self.ventas_realizadas > 0:
            self.ventas_realizadas -= 1
            self.monto_acumulado   -= monto


# =====================================================
#  HERENCIA SIMPLE  ->  Auditor
# =====================================================
class Auditor(Persona):
    """Hereda de Persona. Tiene acceso de solo lectura al sistema."""

    def __init__(self, nombre, nivel_acceso, telefono=""):
        super().__init__(nombre, telefono)
        self.nivel_acceso = nivel_acceso

    def mostrar_info(self):                  # POLIMORFISMO
        return (f"[AUDITOR] {self.nombre} | "
                f"Nivel de acceso: {self.nivel_acceso}")

    def tipo(self):
        return "Auditor"


# =====================================================
#  HERENCIA MULTIPLE  ->  EmpleadoAuditor
# =====================================================
class EmpleadoAuditor(Vendedor, Auditor):
    """
    Herencia MULTIPLE: hereda de Vendedor Y de Auditor.
    Orden MRO (Method Resolution Order):
        EmpleadoAuditor -> Vendedor -> Auditor -> Persona
    Aqui llamamos a AMBOS __init__ para inicializar bien los dos lados.
    """

    def __init__(self, id_vendedor, nombre, codigo, nivel_acceso, telefono=""):
        Vendedor.__init__(self, id_vendedor, nombre, codigo, telefono)  # lado Vendedor
        Auditor.__init__(self, nombre, nivel_acceso, telefono)          # lado Auditor

    def mostrar_info(self):                  # POLIMORFISMO
        return (f"[AUDITOR-VENDEDOR] {self.nombre} | "
                f"Codigo: {self.codigo} | "
                f"Acceso: {self.nivel_acceso} | "
                f"Ventas: {self.ventas_realizadas}")

    def tipo(self):
        return "EmpleadoAuditor"


# =====================================================
#  DEMO DE POLIMORFISMO
# =====================================================
def demo_polimorfismo():
    """
    Llama al MISMO metodo mostrar_info() sobre objetos de distintas clases.
    El resultado cambia segun el tipo real del objeto -> POLIMORFISMO.
    Tambien demuestra el MRO de la herencia multiple.
    """
    personas = [
        Cliente(1, "Ana Torres",   "70000001", "999-111"),
        Vendedor(1, "Pedro Salas", "VEN-01",   "900-001"),
        Auditor("Sara Cano", "ALTO",           "900-002"),
        EmpleadoAuditor(2, "Luis Diaz", "EMP-01", "MEDIO", "900-003"),
    ]
    print("\n  [Demo Polimorfismo]")
    for p in personas:
        print(f"  tipo={p.tipo():<18} -> {p.mostrar_info()}")

    print("\n  [MRO de EmpleadoAuditor]")
    for clase in EmpleadoAuditor.__mro__:
        print(f"    -> {clase.__name__}")
