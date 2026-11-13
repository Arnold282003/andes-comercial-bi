# ETL y contrato de calidad

`pipeline.py` genera raw; `--from-csv` lee y reprocesa raw existente. No necesita paquetes externos. `etl()` aplica los siguientes pasos:

| Paso | Tratamiento | Evidencia |
| --- | --- | --- |
| Texto | Strip y compactación de espacios | Prueba de normalización |
| Tipos | Enteros, float para coordenadas y fechas ISO explícitas | Conversión estricta |
| Faltantes | Error, no imputación silenciosa | Prueba negativa |
| Duplicados | Error en PK, UNIQUE pedido/producto en SQLite | Prueba negativa y restricciones |
| Transacciones | Rechazar cantidad no positiva, costos/precios no positivos, descuento fuera de rango | Contrato en ETL |
| Importes | Recalcular y comparar con ROUND_HALF_UP | 30 000 líneas probadas |
| Claves | FKs activas durante carga y PRAGMA foreign_key_check | SQLite |
| Cabecera | Unir pedido a detalle por PedidoID | Reconciliación raw/estrella |
| Dimensiones | Categoría y región desnormalizadas | Relaciones sin ambigüedad |
| Calendario | 1 096 fechas consecutivas incluidos 366 días de 2024 | Prueba de continuidad |
| RFM | Snapshot al 31/12/2025 | Comparación con hechos |

No se introdujeron errores en el dataset de entrega para luego fingir limpieza. Los errores se comprueban en fixtures de prueba. Los fallos detienen la carga; corregir el CSV de origen y volver a ejecutar. No borrar filas monetarias para hacer pasar pruebas.

## Power Query

Crear pRuta como consulta de parámetro textual. Los seis `.m` usan Csv.Document, PromoteHeaders, TransformColumnTypes y Text.Trim. Su entrada son los CSV estrella ya validados. `calendario_alternativo.m` es una alternativa a importar DimFecha, no una séptima tabla que deba cargarse simultáneamente. M se entrega escrito, pero no se ejecutó en Power Query aquí. `Text.Trim` en M no repite la compactación interna porque la fuente estrella ya está normalizada.

## RFM fijo

Ventana: 01/01/2023–31/12/2025, fecha de corte inclusiva 31/12/2025. Recencia: diferencia en días a última compra; -1 representa sin compras. Frecuencia: pedidos distintos. Monetario: ventas netas sin IGV en toda la ventana.

| Score | R: días (menor mejor) | F: pedidos | M: soles |
| --- | --- | --- | --- |
| 5 | 0–30 | ≥12 | ≥20 000 |
| 4 | 31–60 | 8–11 | 10 000–19 999,99 |
| 3 | 61–120 | 5–7 | 5 000–9 999,99 |
| 2 | 121–240 | 2–4 | 1 000–4 999,99 |
| 1 | >240 | 1 | >0–999,99 |
| 0 | Sin compras | 0 | 0 |

Precedencia excluyente: Sin compras; Campeones si R≥4, F≥4 y M≥4; Leales si R≥3 y F≥3; En riesgo si R≤2 y F≥3; Recientes si R≥4; Ocasionales en los demás casos. Umbrales heurísticos de negocio, no quintiles. Deben recalibrarse en datos reales. Mantenerlos fijos permite comparar las mismas etiquetas sin depender de segmentadores.
