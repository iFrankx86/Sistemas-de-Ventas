# tests/test_analitica.py
# Pruebas del modulo de analisis de datos (pandas + numpy).
# Ejecutar desde la raiz:   python -m unittest discover tests

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from modulos.tienda    import Tienda
from modulos import analitica


class TestAnalitica(unittest.TestCase):

    def setUp(self):
        """Tienda con 2 productos, 1 cliente, 1 vendedor y 2 ventas."""
        self.t = Tienda()
        self.p1 = self.t.agregar_producto("Laptop",  "Computo",    2000.0, 10, 2)
        self.p2 = self.t.agregar_producto("Teclado", "Accesorios",  100.0, 20, 3)
        self.c  = self.t.agregar_cliente("Ana", "70111222")
        self.v  = self.t.agregar_vendedor("Pedro", "VEN-01")
        # venta 1: Laptop x1 (2000) efectivo
        self.t.registrar_venta(self.c, self.v,
                               [{"producto": self.p1, "cantidad": 1}], "efectivo")
        # venta 2: Teclado x2 (200) tarjeta
        self.t.registrar_venta(self.c, self.v,
                               [{"producto": self.p2, "cantidad": 2}], "tarjeta")

    # ---- construccion / limpieza ----
    def test_dataframe_tiene_columnas_y_filas(self):
        df = analitica.ventas_a_dataframe(self.t)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)                       # 2 lineas -> 2 filas
        for col in ("venta_id", "categoria", "subtotal", "metodo_pago"):
            self.assertIn(col, df.columns)

    def test_limpieza_normaliza_texto(self):
        df = analitica.ventas_a_dataframe(self.t)
        # metodo_pago en minusculas, categoria en Title Case
        self.assertTrue((df["metodo_pago"] == df["metodo_pago"].str.lower()).all())
        self.assertIn("Computo", df["categoria"].tolist())

    def test_columnas_derivadas(self):
        df = analitica.ventas_a_dataframe(self.t)
        self.assertIn("dia", df.columns)
        self.assertIn("mes", df.columns)

    # ---- numpy ----
    def test_resumen_numpy(self):
        df = analitica.ventas_a_dataframe(self.t)
        r = analitica.resumen_numpy(df)
        self.assertEqual(r["n_ventas"], 2)
        self.assertAlmostEqual(r["ingreso_total"], 2200.0)   # 2000 + 200
        self.assertAlmostEqual(r["ticket_promedio"], 1100.0) # (2000+200)/2

    # ---- pandas ----
    def test_ventas_por_categoria(self):
        df = analitica.ventas_a_dataframe(self.t)
        g = analitica.ventas_por_categoria(df)
        ingresos = dict(zip(g["categoria"], g["ingresos"]))
        self.assertAlmostEqual(ingresos["Computo"], 2000.0)
        self.assertAlmostEqual(ingresos["Accesorios"], 200.0)

    def test_pivot_tiene_total(self):
        df = analitica.ventas_a_dataframe(self.t)
        piv = analitica.tabla_dinamica_categoria_metodo(df)
        self.assertIn("TOTAL", piv.index)          # margen de fila
        self.assertIn("TOTAL", piv.columns)        # margen de columna

    def test_exportar_csv(self):
        df = analitica.ventas_a_dataframe(self.t)
        ruta = os.path.join(os.path.dirname(__file__), "_tmp_reporte.csv")
        analitica.exportar_csv(df, ruta)
        self.assertTrue(os.path.exists(ruta))
        os.remove(ruta)                            # limpieza

    # ---- programacion funcional ----
    def test_ingreso_total_funcional_coincide(self):
        df = analitica.ventas_a_dataframe(self.t)
        por_pandas = analitica.resumen_numpy(df)["ingreso_total"]
        por_funcional = analitica.ingreso_total_funcional(self.t.ventas)
        self.assertAlmostEqual(por_pandas, por_funcional)

    def test_funcional_filter_productos_caros(self):
        caros = analitica.productos_caros(self.t.productos, 300)
        nombres = [p.nombre for p in caros]
        self.assertIn("Laptop", nombres)
        self.assertNotIn("Teclado", nombres)

    def test_anuladas_no_cuentan(self):
        # anular la venta 1 y verificar que el ingreso baja a 200
        self.t.anular_venta(1)
        df = analitica.ventas_a_dataframe(self.t)
        r = analitica.resumen_numpy(df)
        self.assertAlmostEqual(r["ingreso_total"], 200.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
