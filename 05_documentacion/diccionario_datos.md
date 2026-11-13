# Diccionario de datos

## Origen normalizado

| Tabla | Campo | Tipo SQLite | Nulos | Descripción | Ejemplo |
| --- | --- | --- | --- | --- | --- |
| Calendario | Fecha | DATE | No | Fecha ISO | 2023-01-01 |
| Calendario | Anio | INTEGER | No | Atributo Anio | 2023 |
| Calendario | MesNumero | INTEGER | No | Atributo MesNumero | 1 |
| Calendario | Mes | TEXT | No | Atributo Mes | Ene |
| Calendario | AnioMes | TEXT | No | Atributo AnioMes | 2023-01 |
| Calendario | AnioMesOrden | INTEGER | No | Atributo AnioMesOrden | 202301 |
| Calendario | Trimestre | INTEGER | No | Atributo Trimestre | 1 |
| Calendario | DiaSemana | INTEGER | No | Atributo DiaSemana | 7 |
| Categorias | CategoriaID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Categorias | Categoria | TEXT | No | Atributo Categoria | Tecnología |
| Clientes | ClienteID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Clientes | Cliente | TEXT | No | Atributo Cliente | Cliente sintético 0001 |
| Clientes | Region | TEXT | No | Atributo Region | Lima |
| Clientes | FechaAlta | DATE | No | Fecha ISO | 2022-01-02 |
| Clientes | TipoCliente | TEXT | No | Atributo TipoCliente | Negocio |
| DetalleVentas | DetalleID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| DetalleVentas | PedidoID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| DetalleVentas | ProductoID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| DetalleVentas | Cantidad | INTEGER | No | Atributo Cantidad | 2 |
| DetalleVentas | PrecioUnitarioCent | INTEGER | No | Céntimos PEN | 308721 |
| DetalleVentas | CostoUnitarioCent | INTEGER | No | Céntimos PEN | 245741 |
| DetalleVentas | DescuentoBps | INTEGER | No | Puntos básicos (100 = 1 %) | 500 |
| DetalleVentas | VentaBrutaCent | INTEGER | No | Céntimos PEN | 617442 |
| DetalleVentas | DescuentoCent | INTEGER | No | Céntimos PEN | 30872 |
| DetalleVentas | VentaNetaCent | INTEGER | No | Céntimos PEN | 586570 |
| DetalleVentas | CostoTotalCent | INTEGER | No | Céntimos PEN | 491482 |
| DetalleVentas | IGVCent | INTEGER | No | Céntimos PEN | 105583 |
| Pedidos | PedidoID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Pedidos | Fecha | DATE | No | Fecha ISO | 2023-01-01 |
| Pedidos | ClienteID | INTEGER | No | Clave sintética; ver FK en DDL | 1563 |
| Pedidos | TiendaID | INTEGER | No | Clave sintética; ver FK en DDL | 2 |
| Pedidos | VendedorID | INTEGER | No | Clave sintética; ver FK en DDL | 7 |
| Pedidos | Canal | TEXT | No | Atributo Canal | Tienda |
| Productos | ProductoID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Productos | Producto | TEXT | No | Atributo Producto | Laptop Modelo 001 |
| Productos | CategoriaID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Productos | PrecioBaseCent | INTEGER | No | Céntimos PEN | 308721 |
| Productos | CostoBaseCent | INTEGER | No | Céntimos PEN | 243890 |
| Tiendas | TiendaID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Tiendas | Tienda | TEXT | No | Atributo Tienda | Andes Lima |
| Tiendas | Region | TEXT | No | Atributo Region | Lima |
| Tiendas | Ciudad | TEXT | No | Atributo Ciudad | Lima |
| Tiendas | Zona | TEXT | No | Atributo Zona | Centro |
| Tiendas | Latitud | REAL | No | Atributo Latitud | -12.046 |
| Tiendas | Longitud | REAL | No | Atributo Longitud | -77.043 |
| Tiendas | Pais | TEXT | No | Atributo Pais | Perú |
| Vendedores | VendedorID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Vendedores | TiendaID | INTEGER | No | Clave sintética; ver FK en DDL | 1 |
| Vendedores | Vendedor | TEXT | No | Atributo Vendedor | Asesor sintético 01 |

## Modelo estrella

Ver diccionario_estrella.csv para todos los campos con tipo Power BI, tipo M, nulabilidad y ejemplo. PK/FK exactas se definen en 02_sql/schema_sqlite.sql y 01_schema_postgresql.sql. Coordenadas en grados decimales. AnioMesOrden es AAAAMM, DiaSemana usa lunes=1. RecenciaDias=-1 significa sin compras, no un plazo negativo real.
