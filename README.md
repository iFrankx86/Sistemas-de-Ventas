# Sistemas de Ventas

Sistema de ventas en consola desarrollado con Python para gestionar productos, clientes, vendedores, ventas e inventario sin usar base de datos. Todo el modelo vive en memoria, por lo que los datos se cargan al iniciar la aplicacion y se pierden al cerrarla.

## Concepto

El proyecto simula el flujo basico de una tienda:

- mantenimiento de catalogo de productos;
- registro y busqueda de clientes y vendedores;
- registro de ventas con comprobante;
- anulacion de ventas con restitucion de stock;
- alertas de stock bajo;
- reportes operativos y analitica de datos.

Ademas, el sistema incluye ejemplos de programacion orientada a objetos, polimorfismo, herencia simple y multiple, uso de estructuras de datos en memoria y tratamiento de datos con pandas y numpy.

## Tecnologias y librerias

- Python 3
- Programacion orientada a objetos
- `pandas` para analisis y transformacion de datos
- `numpy` para estadistica descriptiva
- `unittest` para pruebas automatizadas
- Libreria estandar de Python: `datetime`, `functools`, `os`, `sys`

## Arquitectura

La aplicacion esta organizada por capas simples:

- `main.py`: punto de entrada y menu principal de la aplicacion.
- `modulos/tienda.py`: nucleo del sistema; administra las colecciones en memoria y la logica de negocio.
- `modulos/producto.py`: modelo de producto y operaciones de stock.
- `modulos/personas.py`: jerarquia de personas, clientes, vendedores y demo de polimorfismo.
- `modulos/venta.py`: modelo de venta, lineas de venta y comprobante.
- `modulos/datos_iniciales.py`: carga de datos demo al arrancar.
- `modulos/analitica.py`: construccion de DataFrame, reportes con pandas/numpy y funciones funcionales.
- `modulos/constantes.py`: constantes globales como metodos de pago y rangos de IDs.
- `utils/consola.py`: helpers para entrada por consola, tablas y mensajes.
- `tests/`: pruebas unitarias del dominio y de la analitica.

### Flujo general

1. `main.py` crea una tienda de demo con `crear_tienda_demo()`.
2. El usuario interactua por menus de consola.
3. `Tienda` centraliza productos, clientes, vendedores y ventas.
4. `Venta` y `LineaVenta` representan el comprobante y sus items.
5. `analitica.py` convierte las ventas en un DataFrame para explorar reportes.

## Caracteristicas principales

- Alta, listado, busqueda y baja logica de productos.
- Registro de clientes y vendedores.
- Registro de ventas con validacion de stock.
- Anulacion de ventas y ajuste de inventario.
- Reportes por periodo, top productos, cliente top, ranking de vendedores y matriz categoria x metodo de pago.
- Analisis de datos con agrupaciones, tablas dinamicas, estadistica con numpy y exportacion a CSV.
- Demo de programacion funcional con `map`, `filter`, `reduce` y `lambda`.

## Estructura del proyecto

```text
main.py
modulos/
	analitica.py
	constantes.py
	datos_iniciales.py
	personas.py
	producto.py
	tienda.py
	venta.py
tests/
	test_analitica.py
	test_tienda.py
utils/
	consola.py
```

## Instalacion

1. Crear un entorno virtual opcional.
2. Instalar dependencias:

```bash
pip install pandas numpy
```

## Ejecucion

```bash
python main.py
```

## Pruebas

Ejecutar todas las pruebas unitarias:

```bash
python -m unittest discover tests
```

## Notas de diseno

- No usa base de datos ni archivos de persistencia permanentes.
- La capa de negocio esta concentrada en `Tienda` para facilitar mantenimiento y pruebas.
- El proyecto esta pensado para fines academicos y demostrativos, con foco en POO, colecciones y analitica basica.
