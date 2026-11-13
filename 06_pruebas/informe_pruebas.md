# Informe de pruebas · entrega del 1 de noviembre de 2026

## Resultado y frontera de evidencia

| Componente | Trabajo realmente ejecutado | Resultado |
| --- | --- | --- |
| Generador | Python 3.12, semilla 20261101 | 30 000 líneas, 12 000 pedidos |
| ETL CSV | Relectura y transformación con `--from-csv` | Completada |
| SQLite | Carga con FK activas y restricciones | Sin violaciones |
| Datos y cálculos | 23 pruebas unittest | 23 aprobadas, cero fallos y errores |
| Reproducibilidad | Segunda generación, SHA-256 de 14 CSV | 14 idénticos |
| PBIR/PBIP JSON | 43 documentos contra esquemas oficiales | Cero errores de esquema |
| HTML lógica | 8 casos en Node con DOM simulado | Aprobados; incluye nulos, años, reset y vistas |
| Filtro cruzado HTML | Año 2025 + Lima + Tecnología contra SQLite | S/ 3 161 435,83, coincidente |
| Presentación PPTX | Integridad OOXML, geometría, gráfico nativo con libro y reimportación | Aprobada; inspección de PNG de seis diapositivas |
| TMDL | Generado e inspeccionado como texto | No se ejecutó parser TOM/TMDL |
| Power Query M | Código de seis consultas y calendario alternativo | No ejecutado en motor M |
| DAX | 28 definiciones y valores esperados calculados por otros motores | No ejecutado en motor DAX |
| Power BI Desktop | Ninguna sesión disponible | Apertura, actualización y render pendientes |
| PostgreSQL | DDL, carga y consultas proporcionados | No ejecutado en servidor PostgreSQL |

El intento de abrir Chromium falló porque el entorno no permitió crear el socket del proceso. No hubo inspección visual ni clicks reales en navegador para el HTML. Se documenta en validacion_html_navegador.json. Las ocho pruebas de lógica usan DOM simulado; no deben confundirse con render en navegador ni con pruebas de Desktop. No se abrió la presentación en PowerPoint; la comprobación fue programática y visual mediante render de artefactos.

## Cobertura de datos

PK únicas, no nulos, FKs, calendario sin huecos, cantidades y descuentos válidos, costo positivo, cabecera consistente por pedido y vendedor vinculado a la tienda correcta. Aritmética por cada línea: bruto, descuento, neto, costo, utilidad e IGV. Reconciliación campo a campo entre raw y estrella; sumas anuales y mensuales Python/SQLite. RFM contra hechos y verificación independiente de scores y etiquetas.

Fixtures negativos: clave repetida, faltante, tipo fraccionario en Cantidad, cantidad negativa, importe corrupto. Se espera excepción: esos casos aprobados no significan que hubiera errores en los datos de entrega. Se prueba normalización textual. Los casos de división vacía validan el oráculo Python, no la semántica DAX.

## Resultados de control

| Métrica global | Esperado |
| --- | --- |
| Ventas netas | S/ 39 564 593,23 |
| Costo | S/ 31 887 479,70 |
| Utilidad bruta | S/ 7 677 113,53 |
| Margen | 19,4039996453 % |
| Pedidos | 12 000 |
| Clientes compradores | 1 959 |
| Unidades | 64 646 |

Ver kpis_esperados.json, mensuales_esperados.csv, productos_esperados.csv y rfm_esperado.csv. El catálogo DAX indica un contexto y valor de referencia para cada medida. Son resultados esperados, no salidas de DAX.

## Aceptación pendiente

1. Abrir candidato o construir ruta B; registrar versión de Desktop.
2. Actualizar M y revisar tipos/relaciones/tabla de fechas.
3. Ejecutar siete consultas de aceptación. Comparar importes con tolerancia S/ 0,01, razones con 1e-8 y conteos exactos.
4. Probar selecciones de año, categoría, producto y región, limpiar y regresar a totales.
5. Comprobar participación/ranking en tabla plana y por categoría. Sin división por cero; YoY 2023 BLANK; MoM multianual BLANK.
6. Revisar visibilidad, formato, ordenamientos y navegación. Verificar que RFM sea fijo y los KPI transaccionales sí respondan a tiempo/tienda.
7. Ejecutar PostgreSQL en base vacía si se desea declarar ese motor como probado.
8. Registrar evidencia en bitacora_revision.md antes de publicar “dashboard validado”.

## Reejecución

```bash
python 03_python_etl/run_all.py
python -m pip install -r 06_pruebas/requirements_validacion.txt
python 06_pruebas/validate_pbir.py
node 06_pruebas/test_html_logic.mjs
```

No se incluye Node como requisito de datos: solo se necesita para pruebas opcionales del HTML. No hay pruebas de carga, RLS, refresh en Service o gateway porque esas funcionalidades no se implementaron.
