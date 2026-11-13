# Manual del dashboard

## Lectura de las páginas

1. **Resumen ejecutivo:** importe neto sin IGV, utilidad bruta, margen ponderado, pedidos y ticket. Línea de meses y comparativo anual. Investigar si crecimiento de ventas viene acompañado por utilidad.
2. **Productos y rentabilidad:** ranking, categoría, margen y descuento efectivo. Una venta elevada no implica mayor margen. Los rankings dependen de la selección.
3. **Clientes:** compradores del periodo, pedidos por comprador y ticket. La segmentación RFM permanece fija al 31/12/2025; los KPI transaccionales responden a filtros. Una persona sin compras aparece en el maestro pero no en compradores.
4. **Geografía y tiempo:** región de la tienda y zonas, tendencia y estacionalidad. Las ocho regiones no equivalen a cobertura nacional completa.

## Interacciones

Seleccionar año, región o categoría reduce el contexto. Ctrl permite selección múltiple si el segmentador lo permite. Limpiar con borrador. Seleccionar barras aplica interacciones predeterminadas de Power BI: comprobarlas en Editar interacciones. En construcción manual configurar gráficos a filtrado, no resaltado, cuando se quiera que KPI y tablas coincidan. Las pestañas permiten cambiar de página. Sincronización y navegador requieren los pasos de instalación.

## Plano exacto de visuales

Coordenadas en píxeles del lienzo 1440×900. Cada fila corresponde a un JSON del candidato. Para construcción manual, X/Y y ancho/alto se establecen en Formato > General > Propiedades.

| Página | Título / tipo | X,Y / Ancho×Alto | Campos por rol |
| --- | --- | --- | --- |
| 01_resumen | Anio / slicer | 24,16 / 440×80 | Values: DimFecha.Anio |
| 01_resumen | Region / slicer | 489,16 / 440×80 | Values: DimTienda.Region |
| 01_resumen | Categoria / slicer | 954,16 / 440×80 | Values: DimProducto.Categoria |
| 02_productos | Anio / slicer | 24,16 / 440×80 | Values: DimFecha.Anio |
| 02_productos | Region / slicer | 489,16 / 440×80 | Values: DimTienda.Region |
| 02_productos | Categoria / slicer | 954,16 / 440×80 | Values: DimProducto.Categoria |
| 03_clientes | Anio / slicer | 24,16 / 440×80 | Values: DimFecha.Anio |
| 03_clientes | Region / slicer | 489,16 / 440×80 | Values: DimTienda.Region |
| 03_clientes | Categoria / slicer | 954,16 / 440×80 | Values: DimProducto.Categoria |
| 04_geografia | Anio / slicer | 24,16 / 440×80 | Values: DimFecha.Anio |
| 04_geografia | Region / slicer | 489,16 / 440×80 | Values: DimTienda.Region |
| 04_geografia | Categoria / slicer | 954,16 / 440×80 | Values: DimProducto.Categoria |
| 01_resumen | Ventas totales / card | 24,112 / 265×125 | Values: FactVentas.Ventas totales |
| 01_resumen | Utilidad bruta / card | 304,112 / 265×125 | Values: FactVentas.Utilidad bruta |
| 01_resumen | Margen bruto porcentual / card | 584,112 / 265×125 | Values: FactVentas.Margen bruto porcentual |
| 01_resumen | Numero de pedidos / card | 864,112 / 265×125 | Values: FactVentas.Numero de pedidos |
| 01_resumen | Ticket promedio / card | 1144,112 / 265×125 | Values: FactVentas.Ticket promedio |
| 01_resumen | Ventas por mes / lineChart | 24,260 / 900×290 | Category: DimFecha.AnioMes; Y: FactVentas.Ventas totales |
| 01_resumen | Comparación anual / clusteredColumnChart | 948,260 / 468×290 | Category: DimFecha.Anio; Y: FactVentas.Ventas totales, FactVentas.Ventas anio anterior |
| 01_resumen | Rentabilidad por año / tableEx | 24,575 / 1392×290 | Values: DimFecha.Anio, FactVentas.Ventas totales, FactVentas.Costo total, FactVentas.Utilidad bruta, FactVentas.Crecimiento interanual |
| 02_productos | Ranking de productos / tableEx | 24,115 / 690×360 | Values: DimProducto.Producto, FactVentas.Ventas totales, FactVentas.Ranking productos, FactVentas.Participacion producto |
| 02_productos | Ventas por categoría / clusteredBarChart | 738,115 / 678×360 | Category: DimProducto.Categoria; Y: FactVentas.Ventas por categoria |
| 02_productos | Productos menos rentables: ordenar por margen / tableEx | 24,500 / 690×365 | Values: DimProducto.Producto, FactVentas.Utilidad bruta, FactVentas.Margen bruto porcentual |
| 02_productos | Descuento y margen por categoría / tableEx | 738,500 / 678×365 | Values: DimProducto.Categoria, FactVentas.Descuento total, FactVentas.Descuento ponderado, FactVentas.Margen bruto porcentual |
| 03_clientes | Clientes unicos / card | 24,112 / 440×125 | Values: FactVentas.Clientes unicos |
| 03_clientes | Frecuencia de compra / card | 489,112 / 440×125 | Values: FactVentas.Frecuencia de compra |
| 03_clientes | Ticket promedio / card | 954,112 / 440×125 | Values: FactVentas.Ticket promedio |
| 03_clientes | Clientes por RFM fijo al 31/12/2025 / clusteredBarChart | 24,260 / 600×260 | Category: DimCliente.SegmentoRFM; Y: FactVentas.Clientes segmento |
| 03_clientes | Clientes de mayor valor / tableEx | 648,260 / 768×605 | Values: DimCliente.Cliente, FactVentas.Ventas totales, FactVentas.Recencia RFM, FactVentas.Frecuencia RFM, FactVentas.Monetario RFM, FactVentas.Segmento RFM |
| 03_clientes | Clientes compradores por mes / lineChart | 24,545 / 600×320 | Category: DimFecha.AnioMes; Y: FactVentas.Clientes unicos |
| 04_geografia | Ventas por región de la tienda / clusteredBarChart | 24,115 / 690×350 | Category: DimTienda.Region; Y: FactVentas.Ventas totales |
| 04_geografia | Ventas y margen por zona / tableEx | 738,115 / 678×350 | Values: DimTienda.Zona, FactVentas.Ventas totales, FactVentas.Margen bruto porcentual |
| 04_geografia | Tendencia y comparación interanual / lineChart | 24,490 / 690×375 | Category: DimFecha.AnioMes; Y: FactVentas.Ventas totales, FactVentas.Ventas anio anterior |
| 04_geografia | Estacionalidad por mes y año / clusteredColumnChart | 738,490 / 678×375 | Category: DimFecha.Mes; Series: DimFecha.Anio; Y: FactVentas.Ventas totales |

## Formatos y filtros

Importes: S/ con dos decimales, unidades visuales auto o millones, tooltip exacto. Ratios: porcentaje con dos decimales. Pedidos/clientes: entero con separador. Frecuencia: dos decimales. No multiplicar porcentajes por 100 en DAX y además aplicar formato %. RFM: entero para días/frecuencia, PEN para monetario. Véase instalación para ordenamientos, filtros Top N opcionales y navegación.

No se entregan capturas pretendiendo provenir de Desktop. Los archivos PBIR son una definición candidata y requieren revisión de renderizado.
