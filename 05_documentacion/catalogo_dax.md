# Catálogo DAX y contrato de pruebas

Todas las medidas residen en FactVentas. Código propuesto para Desktop, no ejecutado en motor DAX. Los valores siguientes fueron calculados en Python/SQLite y son oráculos de aceptación, no resultados de ejecución DAX. Formatos porcentuales usan fracción (0,19 = 19 %).

## Ventas totales

```dax
Ventas totales = DIVIDE(SUM(FactVentas[VentaNetaCent]),100)
```

Ventas netas de descuentos, sin IGV, en soles.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **39564593.23**. Estado DAX: pendiente de ejecutar.

## Costo total

```dax
Costo total = DIVIDE(SUM(FactVentas[CostoTotalCent]),100)
```

Costo histórico de las unidades vendidas.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **31887479.7**. Estado DAX: pendiente de ejecutar.

## Utilidad bruta

```dax
Utilidad bruta = [Ventas totales]-[Costo total]
```

No incluye gastos operativos ni impuestos sobre renta.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **7677113.53**. Estado DAX: pendiente de ejecutar.

## Margen bruto porcentual

```dax
Margen bruto porcentual = DIVIDE([Utilidad bruta],[Ventas totales])
```

Margen ponderado por ventas. Nunca promediar porcentajes de filas.

Formato: `0.00%`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **0.19403999645265657**. Estado DAX: pendiente de ejecutar.

## Numero de pedidos

```dax
Numero de pedidos = DISTINCTCOUNT(FactVentas[PedidoID])
```

Pedidos con al menos una línea en el contexto. No es aditivo entre productos.

Formato: `#,0`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **12000**. Estado DAX: pendiente de ejecutar.

## Ticket promedio

```dax
Ticket promedio = DIVIDE([Ventas totales],[Numero de pedidos])
```

Venta de líneas visibles por pedido visible; filtrado por categoría es ticket parcial.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **3297.049435833333**. Estado DAX: pendiente de ejecutar.

## Unidades vendidas

```dax
Unidades vendidas = SUM(FactVentas[Cantidad])
```

Cantidad total de artículos.

Formato: `#,0`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **64646**. Estado DAX: pendiente de ejecutar.

## Ventas anio anterior

```dax
Ventas anio anterior = CALCULATE([Ventas totales],SAMEPERIODLASTYEAR(DimFecha[Fecha]))
```

Mismo periodo calendario del año anterior. 2023 no tiene comparativo en este conjunto.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **2025 (mes único si aplica)**. Valor esperado sin formato: **13346027.24**. Estado DAX: pendiente de ejecutar.

## Crecimiento interanual

```dax
Crecimiento interanual = VAR Prev = [Ventas anio anterior] RETURN IF(NOT ISBLANK(Prev),DIVIDE([Ventas totales]-Prev,Prev))
```

BLANK cuando no hay base comparable o su valor es cero.

Formato: `0.00%`. Contexto de prueba: **2025 (mes único si aplica)**. Valor esperado sin formato: **0.13792732900191507**. Estado DAX: pendiente de ejecutar.

## Ventas YTD

```dax
Ventas YTD = TOTALYTD([Ventas totales],DimFecha[Fecha])
```

Acumulado hasta última fecha del contexto, reinicia en enero. Usar un año o eje AnioMes.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **2025 (mes único si aplica)**. Valor esperado sin formato: **15186809.13**. Estado DAX: pendiente de ejecutar.

## Ventas mes anterior

```dax
Ventas mes anterior = IF(HASONEVALUE(DimFecha[AnioMes]),CALCULATE([Ventas totales],DATEADD(DimFecha[Fecha],-1,MONTH)))
```

Disponible con un único mes en contexto; sin total multimensual.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **2025-12**. Valor esperado sin formato: **1784126.14**. Estado DAX: pendiente de ejecutar.

## Crecimiento mensual

```dax
Crecimiento mensual = VAR Prev = [Ventas mes anterior] RETURN IF(NOT ISBLANK(Prev),DIVIDE([Ventas totales]-Prev,Prev))
```

Un único mes completo; comparar con mes completo previo. No usar slicer de días parciales.

Formato: `0.00%`. Contexto de prueba: **2025-12**. Valor esperado sin formato: **0.24336506274158395**. Estado DAX: pendiente de ejecutar.

## Clientes unicos

```dax
Clientes unicos = DISTINCTCOUNT(FactVentas[ClienteID])
```

Clientes compradores en el contexto, no total del maestro.

Formato: `#,0`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **1959**. Estado DAX: pendiente de ejecutar.

## Frecuencia de compra

```dax
Frecuencia de compra = DIVIDE([Numero de pedidos],[Clientes unicos])
```

Pedidos por cliente comprador del periodo visible.

Formato: `0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **6.1255742725880555**. Estado DAX: pendiente de ejecutar.

## Ventas por categoria

```dax
Ventas por categoria = [Ventas totales]
```

Colocar DimProducto[Categoria] en filas/eje. La relación hace la agrupación.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **39564593.23**. Estado DAX: pendiente de ejecutar.

## Participacion producto

```dax
Participacion producto = DIVIDE([Ventas totales],CALCULATE([Ventas totales],ALLSELECTED(DimProducto)))
```

Porcentaje de la selección externa de productos y categorías; mantiene fecha, tienda y cliente.

Formato: `0.00%`. Contexto de prueba: **Producto Laptop Modelo 001 sin filtros**. Valor esperado sin formato: **0.09020444565809076**. Estado DAX: pendiente de ejecutar.

## Ranking productos

```dax
Ranking productos = IF(ISINSCOPE(DimProducto[Producto]),RANKX(ALLSELECTED(DimProducto[ProductoID],DimProducto[Producto]),[Ventas totales],,DESC,Dense))
```

Ranking denso dentro de la categoría/filtros externos visibles. Sin ranking en totales.

Formato: `0`. Contexto de prueba: **Producto Laptop Modelo 001 sin filtros**. Valor esperado sin formato: **1**. Estado DAX: pendiente de ejecutar.

## Recencia RFM

```dax
Recencia RFM = VAR R = SELECTEDVALUE(DimCliente[RecenciaDias]) RETURN IF(R>=0,R)
```

Días desde última compra al 31/12/2025, histórico completo. -1 del archivo se muestra vacío.

Formato: `0`. Contexto de prueba: **ClienteID = 1**. Valor esperado sin formato: **557**. Estado DAX: pendiente de ejecutar.

## Frecuencia RFM

```dax
Frecuencia RFM = SELECTEDVALUE(DimCliente[FrecuenciaRFM])
```

Pedidos de un cliente en 2023–2025, snapshot fijo.

Formato: `0`. Contexto de prueba: **ClienteID = 1**. Valor esperado sin formato: **1**. Estado DAX: pendiente de ejecutar.

## Monetario RFM

```dax
Monetario RFM = DIVIDE(SELECTEDVALUE(DimCliente[MonetarioCent]),100)
```

Venta histórica de un cliente, snapshot fijo.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **ClienteID = 1**. Valor esperado sin formato: **657.8**. Estado DAX: pendiente de ejecutar.

## R score

```dax
R score = SELECTEDVALUE(DimCliente[RScore])
```

1–5 por recencia, cero sin compras.

Formato: `0`. Contexto de prueba: **ClienteID = 1**. Valor esperado sin formato: **1**. Estado DAX: pendiente de ejecutar.

## F score

```dax
F score = SELECTEDVALUE(DimCliente[FScore])
```

1–5 por frecuencia, cero sin compras.

Formato: `0`. Contexto de prueba: **ClienteID = 1**. Valor esperado sin formato: **1**. Estado DAX: pendiente de ejecutar.

## M score

```dax
M score = SELECTEDVALUE(DimCliente[MScore])
```

1–5 por monetario, cero sin compras.

Formato: `0`. Contexto de prueba: **ClienteID = 1**. Valor esperado sin formato: **1**. Estado DAX: pendiente de ejecutar.

## Segmento RFM

```dax
Segmento RFM = SELECTEDVALUE(DimCliente[SegmentoRFM])
```

Etiqueta fija por cliente, sin etiqueta total.

Formato: `texto`. Contexto de prueba: **ClienteID = 1**. Valor esperado sin formato: **Ocasionales**. Estado DAX: pendiente de ejecutar.

## Clientes segmento

```dax
Clientes segmento = COUNTROWS(DimCliente)
```

Cuenta clientes del maestro por segmento fijo, no cambia con fecha o tienda.

Formato: `#,0`. Contexto de prueba: **Maestro completo**. Valor esperado sin formato: **2000**. Estado DAX: pendiente de ejecutar.

## Venta bruta

```dax
Venta bruta = DIVIDE(SUM(FactVentas[VentaBrutaCent]),100)
```

Venta antes de descuentos, sin IGV.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **41819307.39**. Estado DAX: pendiente de ejecutar.

## Descuento total

```dax
Descuento total = DIVIDE(SUM(FactVentas[DescuentoCent]),100)
```

Descuento monetario redondeado por línea.

Formato: `"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **2254714.16**. Estado DAX: pendiente de ejecutar.

## Descuento ponderado

```dax
Descuento ponderado = DIVIDE([Descuento total],[Venta bruta])
```

Descuento efectivo ponderado por venta bruta.

Formato: `0.00%`. Contexto de prueba: **GLOBAL**. Valor esperado sin formato: **0.05391562655433065**. Estado DAX: pendiente de ejecutar.

## Contextos críticos

ALLSELECTED(DimProducto) define participación sobre la selección externa total, incluidas categorías seleccionadas. En una matriz categoría/producto, cada fila de categoría representa su parte del total seleccionado. Ranking mantiene categoría y solo retira el producto de la fila; se reinicia por categoría si esta está en filas. Quitar todos los filtros debe dar participación de todos los productos sumando 1. Los CSV de ranking corresponden a tabla plana sin categoría en filas.

RFM usa columnas del maestro. Sus medidas individuales son BLANK si no hay exactamente un valor (por diseño SELECTEDVALUE), no sumas. Para una fila por cliente usar ClienteID o Cliente, que es único en este caso. Clientes segmento es conteo maestro y no cuenta compradores filtrados.

Las métricas de tiempo requieren DimFecha marcada. Usar periodos contiguos para DATEADD clásico. El dashboard ofrece año/mes y no selecciones dispersas de días. YTD en total multianual se refiere al último año del contexto; mostrarlo por año/mes.
