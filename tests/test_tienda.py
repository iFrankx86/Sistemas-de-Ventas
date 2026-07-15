# tests/test_tienda.py
# Pruebas de las operaciones clave de la Tienda (todo en memoria, sin BD).
# Ejecutar desde la raiz del proyecto:   python -m unittest discover tests

import os
import sys
import unittest

# permite importar 'modulos' al correr los tests desde cualquier sitio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modulos.tienda     import Tienda
from modulos.constantes import METODOS_PAGO, ESTADOS_VENTA, RANGO_IDS


class TestTienda(unittest.TestCase):

    def setUp(self):
        """Una Tienda limpia antes de cada test."""
        self.t = Tienda()
        self.prod = self.t.agregar_producto("Mouse", "Accesorios", 50.0, stock=10, stock_minimo=3)
        self.cli  = self.t.agregar_cliente("Ana", "70111222")
        self.vend = self.t.agregar_vendedor("Pedro", "VEN-01")

    # ---- productos ----
    def test_agregar_producto_genera_id(self):
        p2 = self.t.agregar_producto("Teclado", "Accesorios", 90.0, 5)
        self.assertEqual(self.prod.id_prod, 1)
        self.assertEqual(p2.id_prod, 2)

    def test_buscar_por_id_exacto(self):
        # buscar "1" debe traer solo el producto con id 1, no por LIKE
        res = self.t.buscar_productos("1")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id_prod, 1)

    def test_eliminar_es_baja_logica(self):
        self.t.eliminar_producto(self.prod.id_prod)
        self.assertNotIn(self.prod, self.t.listar_productos())   # no aparece
        self.assertFalse(self.prod.activo)                       # pero sigue existiendo

    # ---- ventas / stock ----
    def test_venta_descuenta_stock(self):
        items = [{"producto": self.prod, "cantidad": 4}]
        venta = self.t.registrar_venta(self.cli, self.vend, items, "efectivo")
        self.assertIsNotNone(venta)
        self.assertEqual(self.prod.stock, 6)          # 10 - 4
        self.assertEqual(venta.total(), 200.0)        # 4 * 50

    def test_no_permite_sobreventa(self):
        items = [{"producto": self.prod, "cantidad": 999}]   # mas que el stock
        venta = self.t.registrar_venta(self.cli, self.vend, items, "efectivo")
        self.assertIsNone(venta)                      # rechazada
        self.assertEqual(self.prod.stock, 10)         # stock intacto

    def test_venta_actualiza_cliente_y_vendedor(self):
        items = [{"producto": self.prod, "cantidad": 2}]
        self.t.registrar_venta(self.cli, self.vend, items, "efectivo")
        self.assertEqual(self.vend.ventas_realizadas, 1)
        self.assertEqual(self.vend.monto_acumulado, 100.0)
        self.assertEqual(self.cli.total_compras(), 100.0)

    def test_anular_repone_stock(self):
        items = [{"producto": self.prod, "cantidad": 3}]
        venta = self.t.registrar_venta(self.cli, self.vend, items, "efectivo")
        self.assertEqual(self.prod.stock, 7)
        r = self.t.anular_venta(venta.id_venta)
        self.assertEqual(r, "ok")
        self.assertEqual(self.prod.stock, 10)         # stock restituido
        self.assertTrue(venta.esta_anulada())
        self.assertEqual(self.vend.ventas_realizadas, 0)   # acumulado revertido

    # ---- inventario ----
    def test_alerta_stock_bajo(self):
        self.t.ajustar_stock(self.prod.id_prod, -8)   # 10 - 8 = 2  (< minimo 3)
        bajos = self.t.productos_stock_bajo()
        self.assertIn(self.prod, bajos)

    def test_ajuste_no_deja_stock_negativo(self):
        ok = self.t.ajustar_stock(self.prod.id_prod, -999)
        self.assertFalse(ok)
        self.assertEqual(self.prod.stock, 10)

    # ---- clientes ----
    def test_dni_duplicado_rechazado(self):
        repetido = self.t.agregar_cliente("Otro", "70111222")   # mismo DNI
        self.assertIsNone(repetido)

    # ---- reportes ----
    def test_reporte_incluye_venta_de_hoy(self):
        items = [{"producto": self.prod, "cantidad": 1}]
        self.t.registrar_venta(self.cli, self.vend, items, "efectivo")
        from datetime import datetime
        hoy = datetime.now().strftime("%Y-%m-%d")
        r = self.t.reporte_periodo(hoy, hoy)          # bug viejo: excluia hoy
        self.assertEqual(r["total_ventas"], 1)
        self.assertEqual(r["ingresos"], 50.0)


    # ---- constantes (tuplas) ----
    def test_constantes_son_tuplas_inmutables(self):
        # deben ser TUPLAS (no listas)
        self.assertIsInstance(METODOS_PAGO, tuple)
        self.assertIsInstance(ESTADOS_VENTA, tuple)
        self.assertIsInstance(RANGO_IDS, tuple)
        # y ser inmutables: intentar modificarlas debe fallar
        with self.assertRaises(TypeError):
            METODOS_PAGO[0] = "otro"

    def test_rango_ids_se_desempaqueta(self):
        id_min, id_max = RANGO_IDS          # desempaquetado de tupla
        self.assertEqual(id_min, 1)
        self.assertLess(id_min, id_max)


if __name__ == "__main__":
    unittest.main(verbosity=2)
