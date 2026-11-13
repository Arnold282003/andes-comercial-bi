from pathlib import Path
import csv,json,sqlite3,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'03_python_etl'))
from build_powerbi import MEASURES
K=json.loads((ROOT/'06_pruebas/kpis_esperados.json').read_text());G=K['GLOBAL'];DB=sqlite3.connect(ROOT/'01_datos/andes_comercial.sqlite')
def put(p,s):(ROOT/p).write_text(s.strip()+'\n',encoding='utf-8')
def money(n):return f'S/ {n:,.2f}'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(str(v) for v in row)+' |' for row in rows)
put('README.md',f'''# Andes Comercial · Business Intelligence

**Sistema de Inteligencia de Negocios para el Análisis de Ventas, Rentabilidad y Clientes de una Empresa Comercial Peruana.**

Caso académico de portafolio para Ingeniería de Sistemas, UNI. Empresa ficticia y datos 100 % sintéticos. No representa experiencia laboral ni resultados comerciales reales.

## Estado de la entrega

- Dataset, ETL Python, SQLite, resultados de referencia y pruebas automatizadas: ejecutados.
- PBIP candidato con TMDL, PBIR, 4 páginas y 34 visuales: generado. Ver validación estructural JSON en `06_pruebas/validacion_pbir.json`.
- **No se abrió Power BI Desktop. No se ejecutaron DAX ni M en un motor Microsoft.** La validación de esquemas no garantiza apertura, render ni semántica.
- Scripts PostgreSQL: entregados, sin ejecución en servidor PostgreSQL.
- Guía manual completa y consultas independientes permiten construir el informe aunque el candidato requiera ajustes.

## Inicio rápido

Descomprimir sin modificar las carpetas. Python 3.10 o posterior, biblioteca estándar para datos y pruebas:

```bash
python 03_python_etl/pipeline.py
python 03_python_etl/build_powerbi.py
python 06_pruebas/test_project.py
python 03_python_etl/build_docs.py
```

Para reprocesar los CSV existentes sin volver a generarlos:

```bash
python 03_python_etl/pipeline.py --from-csv
```

Opcional, validación de definiciones PBIR contra esquemas oficiales incluidos:

```bash
python -m pip install -r 06_pruebas/requirements_validacion.txt
python 06_pruebas/validate_pbir.py
```

La semilla es 20261101. La generación sobrescribe exclusivamente los entregables generados del proyecto. Guardar una copia de cualquier edición propia antes de regenerar. El orden de ejecución anterior importa: las pruebas producen las cifras que usa la documentación.

## Primer uso en Power BI

Abrir `04_powerbi/PBIP_CANDIDATO/Andes.pbip`. Editar el parámetro `pRuta` a la ruta absoluta terminada en `/` de `01_datos/star/`. Actualizar. Si Desktop no abre el candidato, seguir `05_documentacion/instalacion_powerbi.md`, ruta B. Importar `04_powerbi/tema_andes.json` y aplicar los ajustes finales de orden, navegación y filtros documentados.

## Cifras verificadas con Python y SQLite

{table(['Indicador 2023–2025','Valor'],[['Ventas netas sin IGV',money(G['Ventas totales'])],['Costo',money(G['Costo total'])],['Utilidad bruta',money(G['Utilidad bruta'])],['Margen bruto',f"{G['Margen bruto porcentual']:.2%}"],['Pedidos','12 000'],['Líneas','30 000'],['Clientes compradores',G['Clientes unicos']]])}

Los 2 000 clientes del maestro incluyen 41 sin compras. Hay 100 productos, cinco categorías, ocho tiendas, 32 vendedores y 1 096 días. Las ventas se registran en PEN sin IGV; se calcula un IGV sintético de 18 % por línea. No se modelan devoluciones, pagos, inventario ni utilidad neta.

## Recorrido recomendado

1. Leer arquitectura y contrato de métricas.
2. Ejecutar pruebas y estudiar el modelo estrella.
3. Abrir o reconstruir el informe en Desktop, ejecutar las consultas DAX de aceptación.
4. Completar la bitácora personal antes de adaptar CV y LinkedIn.

`INDICE_ARCHIVOS.md` describe cada archivo. `07_portafolio/presentacion_entrevista.pptx` contiene la presentación breve.

## Autoría y uso responsable

Base técnica generada con herramientas automatizadas bajo las instrucciones del estudiante. No se ha verificado qué partes Arnold Espinoza revisó personalmente. La bitácora de revisión se entrega sin completar. Los textos públicos distinguen entrega asistida y validación personal pendiente.

Código original del caso: licencia MIT. Datos sintéticos: CC0 según `01_datos/LICENCIA_DATOS.md`. Esquemas Microsoft en `04_powerbi/schemas`: conservar procedencia y licencias de su proveedor, no quedan relicenciados por MIT.
''')
put('05_documentacion/arquitectura.md','''# Arquitectura y decisiones

## Capas

1. Generador Python con semilla fija: produce ocho CSV normalizados de origen.
2. ETL Python: valida y tipa, normaliza texto, aplica contrato monetario, une cabecera y líneas; calcula snapshot RFM.
3. SQLite: réplica transaccional y modelo dimensional con PK, FK y CHECK. PostgreSQL: DDL y carga psql equivalentes.
4. CSV estrella: contrato portable de ingestión. Power Query importa UTF-8 y tipa explícitamente.
5. Modelo Power BI Import: cinco dimensiones filtran FactVentas. Medidas DAX calculan métricas en contexto.
6. PBIR: páginas y visuales definidos como JSON. Publicación en Power BI Service queda fuera del alcance ejecutado.

## Contratos

Grano: una línea = un producto dentro de un pedido. `(PedidoID, ProductoID)` es único. Cada pedido pertenece a un cliente, fecha, tienda, canal y vendedor. Los pedidos tienen una o más líneas. Un vendedor pertenece a una tienda; la relación se valida en los datos, sin activar otra ruta de filtro entre dimensiones.

Dinero entero en céntimos. Precio y costo históricos se congelan en la línea, no se recalculan con el precio actual del producto. Cantidad positiva entera. Descuento en puntos básicos (500 = 5 %). Se redondea descuento al céntimo con ROUND_HALF_UP; neto = bruto − descuento. Costo = cantidad × costo unitario. IGV sintético = redondeo de neto × 18 %. Los KPI excluyen IGV. La utilidad es bruta, no neta.

Empresa ficticia de venta de tecnología, electrohogar, hogar, oficina y deportes. Ocho tiendas en ciudades reales; no representan domicilios comerciales reales. Clientes y vendedores usan etiquetas sintéticas, sin DNI, emails ni información personal.

## Generación estadística

La distribución diaria tiene factores de mes, fin de semana y crecimiento de demanda anual de 13 % en el peso de muestreo. Las fechas son muestreadas entre 2023-01-01 y 2025-12-31. Los resultados observados no tienen que crecer exactamente 13 %. Noviembre/diciembre tienen mayor demanda; marzo favorece oficina. Los clientes tienen propensiones Pareto con repetición y preferencia por tienda de su región (82 %). Los productos tienen popularidad desigual. Los precios aumentan 3,5 % anual sobre base y los costos 4,5 % anual, con perturbación acotada. Promociones en julio, noviembre y diciembre aumentan probabilidad de descuento. No se simula causalidad ni se calibró con una empresa real.

## Operación

Cargas completas, no incrementales. CSV UTF-8, separador coma, punto decimal, fechas ISO. Python y SQL pueden ejecutarse offline. La primera instalación opcional de jsonschema requiere acceso a PyPI. Power BI usa rutas locales; no se entrega gateway. Para Service se necesitaría una fuente accesible y configuración de actualización. No hay RLS porque el caso se publica como datos sintéticos; antes de usar datos reales se debe diseñar seguridad, minimización y gobernanza.

## Límites

Tres años sin 2022: comparativos de 2023 quedan BLANK. No usar la frecuencia global como si fuera anual. No sumar clientes únicos o pedidos entre categorías. RFM fijo no cambia con los slicers de fechas. Se ofrece una tabla de regiones en lugar de depender de servicios de mapas o geocodificación.
''')
relations=[['DimFecha','Fecha','Fecha'],['DimCliente','ClienteID','ClienteID'],['DimProducto','ProductoID','ProductoID'],['DimTienda','TiendaID','TiendaID'],['DimVendedor','VendedorID','VendedorID']]
put('05_documentacion/modelo_estrella.md','''# Modelo estrella

```mermaid
flowchart TB
  F["FactVentas · 30 000 líneas"]
  D["DimFecha · 1 096 días"] -->|"1 a muchos"| F
  C["DimCliente · 2 000 clientes + RFM"] -->|"1 a muchos"| F
  P["DimProducto · 100 productos + categoría"] -->|"1 a muchos"| F
  T["DimTienda · 8 tiendas + ubicación"] -->|"1 a muchos"| F
  V["DimVendedor · 32 vendedores"] -->|"1 a muchos"| F
```

'''+table(['Lado 1','Clave dimensión','Clave FactVentas'],relations)+'''

Todas las relaciones son activas, 1:* y unidireccionales desde dimensión hacia hechos. No crear relaciones entre DimTienda y DimVendedor ni entre región del cliente y región de tienda. Esto evita rutas ambiguas. DimFecha debe marcarse como tabla de fechas usando Fecha, única, sin huecos ni nulos.

Categoría se desnormaliza en DimProducto y ubicación en DimTienda. Categorias, Pedidos y DetalleVentas permanecen en origen/SQLite, pero no se cargan como tablas adicionales al modelo Power BI. PedidoID es dimensión degenerada en FactVentas. Canal también queda en la tabla de hechos.

Filtrar categoría selecciona productos y sus líneas. DISTINCTCOUNT(PedidoID) cuenta cada pedido visible una sola vez. Un pedido con productos de dos categorías aparece en ambas, por ello sumar el número de pedidos de categorías sobrecuenta el total. Un filtro de región usa ubicación de la tienda, no domicilio del cliente.

DimCliente contiene tanto todos los clientes como los atributos de segmentación. `Clientes unicos` cuenta compradores desde FactVentas. `Clientes segmento` cuenta el maestro y por diseño ignora filtros de tiempo y tienda. Esas dos medidas responden preguntas distintas.
''')
put('05_documentacion/etl.md','''# ETL y contrato de calidad

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
''')
put('05_documentacion/instalacion_powerbi.md','''# Instalación y construcción en Power BI Desktop

## Requisitos

Windows con Power BI Desktop estándar que admita PBIP, PBIR y TMDL (no edición optimizada para Report Server). Consultar los enlaces oficiales en fuentes.md para configuración de formatos en la versión instalada. Python >=3.10 para regeneración, espacio aproximado 30 MB para descomprimir. PostgreSQL y psql opcionales. No requiere licencia de Service para analizar localmente.

## Ruta A · proyecto candidato

1. Extraer todo el ZIP. Evitar mover únicamente el `.pbip`.
2. Abrir `04_powerbi/PBIP_CANDIDATO/Andes.pbip` en Desktop. Si hay error de definición, conservar el mensaje y seguir ruta B. Los JSON fueron validados por esquema; el parser TMDL y Desktop quedan por comprobar.
3. En Transformar datos, administrar parámetros, cambiar `pRuta` por la ruta absoluta a `01_datos/star/`, por ejemplo `C:/BI_Peru/peru_bi/01_datos/star/`. Debe terminar en `/`. Alternativamente editar expressions.tmdl antes de abrir.
4. Establecer nivel de privacidad local apropiado y cerrar/aplicar. Actualizar. Revisar seis tablas y 30 000 filas en FactVentas.
5. Marcar DimFecha como tabla de fechas por Fecha. Confirmar relaciones activas 1:* y filtro simple. Ordenar Mes por MesNumero y AnioMes por AnioMesOrden. Desactivar fecha/hora automática para este archivo.
6. Vista > Temas > Examinar temas: importar `04_powerbi/tema_andes.json`. No se presupone que Desktop haya registrado este recurso en el candidato.
7. Completar ajustes visuales descritos abajo. Guardar como PBIP validado propio. Solo crear un PBIX desde Desktop si se necesita.

## Ruta B · construcción independiente

1. Crear un informe vacío. Transformar datos > Nueva consulta > Consulta en blanco. En editor avanzado pegar `04_powerbi/powerquery/pRuta.m`; nombrar `pRuta` y ajustar ruta.
2. Repetir consulta en blanco para `DimFecha`, `DimCliente`, `DimProducto`, `DimTienda`, `DimVendedor` y `FactVentas`, pegando el `.m` homónimo. Conservar nombres exactos. Habilitar carga en estas seis. No cargar raw ni calendario_alternativo además de DimFecha.
3. Cerrar y aplicar. En Modelo crear las cinco relaciones de modelo_estrella.md. Dimensiones lado 1, hechos lado *, activas y filtro único. No crear otras relaciones automáticas.
4. Marcar DimFecha y sus ordenamientos como en ruta A. Ocultar importes Cent de FactVentas y claves técnicas a los usuarios; no eliminarlos. Tipos: IDs/importes enteros, Fecha/FechaAlta fecha, coordenadas decimal, demás según diccionario.
5. En FactVentas > Nueva medida: crear individualmente cada definición de medidas.dax. No pegar todo el archivo en una sola medida. Aplicar el formato indicado en catálogo. Se usa separador DAX coma estándar; si la configuración local requiere punto y coma, desactivar separadores localizados o ajustar delimitadores de argumentos.
6. Crear cuatro páginas, lienzo personalizado 1440×900. Insertar visuales según `especificacion_visuales.json` o la tabla de manual_dashboard.md. Usar campos dimensionales para ejes/segmentadores y medidas para valores, sin sumar IDs ni porcentajes.
7. Importar tema, aplicar ajustes siguientes y ejecutar aceptación DAX.

## Ajustes finales, ambas rutas

- Fondo de página #F4F7FA, tarjetas blancas, texto #16324F, acento #087F8C. Segoe UI. KPI 28–32 pt, títulos 14 pt, etiquetas ≥11 pt. Sin gráficos 3D. Usar tooltips para cifras exactas.
- Segmentadores de año, región de tienda y categoría, desplegables. Sin selección significa todo. Sincronizar esos tres entre páginas (Ver > Sincronizar segmentaciones). El candidato tiene segmentadores locales; sincronización se configura aquí.
- Línea mensual: ordenar AnioMes ascendente. Comparación anual: ordenar Anio ascendente. Estacionalidad: Mes por MesNumero y leyenda Anio.
- Ranking productos: ordenar Ranking productos ascendente. Si se desea Top 10, usar filtro visual Top N 10 por Ventas totales. Esta es una acción manual, no un filtro ya guardado.
- Productos menos rentables: ordenar Margen bruto porcentual ascendente, conservar ventas y utilidad en tooltip. Top/Bottom 10 opcional mediante filtro N inferior por margen. La tabla candidata incluye todos los productos hasta aplicar el filtro.
- Clientes de mayor valor: ordenar Ventas totales descendente. Mantener RFM en columnas con título que indique corte fijo. Gráfico RFM usa Clientes segmento. Desactivar interacción de filtros de fecha/tienda hacia ese gráfico para comunicar el snapshot fijo; filtrar por segmento sí debe filtrar las otras métricas de clientes.
- Productos por categoría: ventas como barra, margen/descuento como tabla de porcentajes. No usar doble eje sin etiquetas claras.
- Insertar > Botones > Navegador > Navegador de páginas. Ubicarlo en el borde inferior (1440×40) y aumentar alto del lienzo a 950 si se desea conservar el contenido. Alternativa disponible inmediatamente: pestañas de páginas de Desktop. El navegador no está generado en PBIR.
- Geografía: barras por región de tienda, tabla de zonas. Evita dependencia de mapas. Si se añade mapa, usar Latitud/Longitud de DimTienda y marcar categorías geográficas, con acceso al proveedor de mapas.
- Accesibilidad: revisar contraste, texto alternativo, orden de tabulación, formatos S/ y %, y navegación con teclado.

## Aceptación real en Desktop

Ejecutar cada bloque EVALUATE de `06_pruebas/consultas_aceptacion.dax` en Vista de consultas DAX (o DAX Studio conectado). Comparar con kpis_esperados.json y CSV esperados. Tolerancia: S/ 0,01 en importes, 1e-8 en razones antes del formato. BLANK en 2023 YoY y en MoM multimensual. No reemplazar BLANK por cero para esconder ausencia de historia.

Probar año 2025; una categoría; dos productos; una región; seleccionar cliente; limpiar filtros; confirmar que las cifras vuelven a total. Guardar captura y registrar versión de Desktop, fecha, resultado y discrepancias en bitacora_revision.md. La apertura exitosa sola no valida medidas o interacciones.

## PostgreSQL opcional

Crear una base vacía de trabajo. Desde la raíz `peru_bi`, ejecutar:

```bash
psql -d andes_bi -v ON_ERROR_STOP=1 -f 02_sql/01_schema_postgresql.sql
psql -d andes_bi -v ON_ERROR_STOP=1 -f 02_sql/02_carga_postgresql.sql
psql -d andes_bi -v ON_ERROR_STOP=1 -f 02_sql/03_consultas_control.sql
```

Usar las opciones de conexión de psql para host/usuario. No guardar contraseñas en scripts. DDL no borra tablas; volver a ejecutar sobre base con tablas falla de forma intencional. La carga CSV usa rutas relativas a la raíz y va en una transacción.
''')
# DAX catalogue, each measure with concrete expected reference.
refs={n:('GLOBAL',G.get(n)) for n,d,f,e in MEASURES if n in G}
for n in ['Ventas anio anterior','Crecimiento interanual','Ventas YTD','Ventas mes anterior','Crecimiento mensual']:refs[n]=('2025 (mes único si aplica)',K['2025'].get(n))
monthly=list(csv.DictReader((ROOT/'06_pruebas/mensuales_esperados.csv').open()))
for n in ['Ventas mes anterior','Crecimiento mensual']:refs[n]=('2025-12',monthly[-1][n])
pr=list(csv.DictReader((ROOT/'06_pruebas/productos_esperados.csv').open()));rr=list(csv.DictReader((ROOT/'06_pruebas/rfm_esperado.csv').open()))
for n in ['Ranking productos','Participacion producto']:refs[n]=('Producto '+pr[0]['Producto']+' sin filtros',pr[0][n])
for n in ['Recencia RFM','Frecuencia RFM','Monetario RFM','R score','F score','M score','Segmento RFM']:refs[n]=('ClienteID = 1',rr[0][n])
refs['Clientes segmento']=('Maestro completo',2000)
cat=['# Catálogo DAX y contrato de pruebas','Todas las medidas residen en FactVentas. Código propuesto para Desktop, no ejecutado en motor DAX. Los valores siguientes fueron calculados en Python/SQLite y son oráculos de aceptación, no resultados de ejecución DAX. Formatos porcentuales usan fracción (0,19 = 19 %).']
for n,d,f,e in MEASURES:
    context,value=refs[n];cat.extend([f'## {n}',f'```dax\n{n} = {d}\n```',e,f'Formato: `{f or "texto"}`. Contexto de prueba: **{context}**. Valor esperado sin formato: **{value}**. Estado DAX: pendiente de ejecutar.'])
cat.append('## Contextos críticos\n\nALLSELECTED(DimProducto) define participación sobre la selección externa total, incluidas categorías seleccionadas. En una matriz categoría/producto, cada fila de categoría representa su parte del total seleccionado. Ranking mantiene categoría y solo retira el producto de la fila; se reinicia por categoría si esta está en filas. Quitar todos los filtros debe dar participación de todos los productos sumando 1. Los CSV de ranking corresponden a tabla plana sin categoría en filas.\n\nRFM usa columnas del maestro. Sus medidas individuales son BLANK si no hay exactamente un valor (por diseño SELECTEDVALUE), no sumas. Para una fila por cliente usar ClienteID o Cliente, que es único en este caso. Clientes segmento es conteo maestro y no cuenta compradores filtrados.\n\nLas métricas de tiempo requieren DimFecha marcada. Usar periodos contiguos para DATEADD clásico. El dashboard ofrece año/mes y no selecciones dispersas de días. YTD en total multianual se refiere al último año del contexto; mostrarlo por año/mes.')
put('05_documentacion/catalogo_dax.md','\n\n'.join(cat))
spec=json.loads((ROOT/'04_powerbi/especificacion_visuales.json').read_text())
put('05_documentacion/manual_dashboard.md','''# Manual del dashboard

## Lectura de las páginas

1. **Resumen ejecutivo:** importe neto sin IGV, utilidad bruta, margen ponderado, pedidos y ticket. Línea de meses y comparativo anual. Investigar si crecimiento de ventas viene acompañado por utilidad.
2. **Productos y rentabilidad:** ranking, categoría, margen y descuento efectivo. Una venta elevada no implica mayor margen. Los rankings dependen de la selección.
3. **Clientes:** compradores del periodo, pedidos por comprador y ticket. La segmentación RFM permanece fija al 31/12/2025; los KPI transaccionales responden a filtros. Una persona sin compras aparece en el maestro pero no en compradores.
4. **Geografía y tiempo:** región de la tienda y zonas, tendencia y estacionalidad. Las ocho regiones no equivalen a cobertura nacional completa.

## Interacciones

Seleccionar año, región o categoría reduce el contexto. Ctrl permite selección múltiple si el segmentador lo permite. Limpiar con borrador. Seleccionar barras aplica interacciones predeterminadas de Power BI: comprobarlas en Editar interacciones. En construcción manual configurar gráficos a filtrado, no resaltado, cuando se quiera que KPI y tablas coincidan. Las pestañas permiten cambiar de página. Sincronización y navegador requieren los pasos de instalación.

## Plano exacto de visuales

Coordenadas en píxeles del lienzo 1440×900. Cada fila corresponde a un JSON del candidato. Para construcción manual, X/Y y ancho/alto se establecen en Formato > General > Propiedades.

'''+table(['Página','Título / tipo','X,Y / Ancho×Alto','Campos por rol'],[[s['Pagina'],s['Titulo']+' / '+s['Tipo'],f"{s['X']},{s['Y']} / {s['Ancho']}×{s['Alto']}",'; '.join(k+': '+', '.join(v) for k,v in s['Campos'].items())] for s in spec])+'''

## Formatos y filtros

Importes: S/ con dos decimales, unidades visuales auto o millones, tooltip exacto. Ratios: porcentaje con dos decimales. Pedidos/clientes: entero con separador. Frecuencia: dos decimales. No multiplicar porcentajes por 100 en DAX y además aplicar formato %. RFM: entero para días/frecuencia, PEN para monetario. Véase instalación para ordenamientos, filtros Top N opcionales y navegación.

No se entregan capturas pretendiendo provenir de Desktop. Los archivos PBIR son una definición candidata y requieren revisión de renderizado.
''')
catrows=DB.execute('SELECT p."Categoria", SUM(f."VentaNetaCent")/100.0, SUM(f."UtilidadCent")*1.0/SUM(f."VentaNetaCent") FROM "FactVentas" f JOIN "DimProducto" p USING ("ProductoID") GROUP BY 1 ORDER BY 2 DESC').fetchall()
regionrows=DB.execute('SELECT t."Region",SUM(f."VentaNetaCent")/100.0 FROM "FactVentas" f JOIN "DimTienda" t USING ("TiendaID") GROUP BY 1 ORDER BY 2 DESC').fetchall()
put('05_documentacion/hallazgos_comerciales.md',f'''# Hallazgos del caso sintético

Cálculos sobre 2023–2025 completos, sin filtros. Interpretaciones hipotéticas, no conclusiones sobre el mercado peruano.

{table(['Año','Ventas','Utilidad bruta','Margen','YoY'],[[y,money(K[y]['Ventas totales']),money(K[y]['Utilidad bruta']),f"{K[y]['Margen bruto porcentual']:.2%}",f"{K[y]['Crecimiento interanual']:.2%}" if K[y]['Crecimiento interanual'] is not None else 'Sin base 2022'] for y in ['2023','2024','2025']])}

Las ventas de 2025 aumentaron {K['2025']['Crecimiento interanual']:.2%} respecto de 2024. El margen cayó de {K['2023']['Margen bruto porcentual']:.2%} en 2023 a {K['2025']['Margen bruto porcentual']:.2%} en 2025: {(K['2025']['Margen bruto porcentual']-K['2023']['Margen bruto porcentual'])*100:.2f} puntos porcentuales. La utilidad bruta aumentó pese a la compresión del margen. Esto es compatible con los supuestos del generador (costos crecen más que precios), pero no prueba causalidad por sí solo.

## Mezcla comercial

{table(['Categoría','Ventas','Margen'],[[c,money(v),f'{m:.2%}'] for c,v,m in catrows])}

La concentración en tecnología refleja precios unitarios superiores y supuestos de mezcla. Una decisión posible es revisar promociones de categorías de bajo margen, evaluando volumen e ingreso incremental; este dataset no contiene experimento causal, por lo que no permite afirmar que bajar descuentos aumentaría utilidad total.

## Distribución geográfica

{table(['Región de tienda','Ventas'],[[r,money(v)] for r,v in regionrows])}

La región líder es {regionrows[0][0]} con {regionrows[0][1]/G['Ventas totales']:.2%} de ventas. La generación asigna mayor peso a Lima. No extrapolar participación de mercado ni evaluar productividad sin costos de tienda, área o tráfico.

## Clientes y retención

{table(['Segmento fijo','Clientes'],list(K['Segmentos'].items()))}

Existen {G['Clientes unicos']} compradores sobre 2 000 clientes del maestro. Los 301 clientes En riesgo merecen una hipótesis de campaña de reactivación; medir tasa incremental contra grupo de control en un caso real. RFM no predice churn automáticamente y los umbrales se definieron de forma heurística.

## Acciones exploratorias

- Revisar categorías con margen bajo y productos con descuento elevado; medir utilidad, no solo ventas.
- Preparar demanda estacional y comparar cada mes con su equivalente anual antes de interpretar cambios.
- Priorizar pruebas de retención sobre segmentos de valor histórico, documentando exclusiones y consentimiento si se usan datos reales.
- Incorporar devoluciones, gastos logísticos, inventario y pagos en una siguiente versión para ampliar la interpretación.

Los CSV de referencia y consultas SQL permiten auditar los importes. No se atribuyen mejoras de negocio a un dashboard que aún no se usó en una operación real.
''')
put('05_documentacion/fuentes.md','''# Fuentes técnicas oficiales

Consultadas el 1 de noviembre de 2026. Se usó documentación oficial para la estructura candidata, no como certificación de funcionamiento.

- PBIP: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
- Carpetas del reporte y PBIR: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
- Definición de reporte en Fabric: https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/report-definition
- TMDL y sintaxis: https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview
- Esquemas JSON descargados desde https://developer.microsoft.com/json-schemas/fabric/ (URL exacta `$schema` en cada archivo y registro en schemas/registry.json).

PBIP referencia una carpeta de reporte. definition.pbir permite `datasetReference.byPath` relativo al modelo local. PBIR separa report, version, pages y visuals. TMDL declara tablas, columnas, medidas, particiones M y relaciones. No se editó un report.json legacy, cuyo tratamiento difiere de PBIR.

La validación JSON usa versiones declaradas explícitamente, sin asumir que cualquier versión de Desktop las soporta. Compatibilidad TMDL 1604. No se obtuvo un certificado o salida del parser TOM/TMDL. Power BI Desktop sigue siendo el punto final de aceptación.
''')
put('02_sql/03_consultas_control.sql','''-- Compatible con SQLite y PostgreSQL. Importes en soles.
SELECT SUM("VentaNetaCent")/100.0 AS ventas, SUM("CostoTotalCent")/100.0 AS costo,
       SUM("UtilidadCent")/100.0 AS utilidad,
       SUM("UtilidadCent")*1.0/NULLIF(SUM("VentaNetaCent"),0) AS margen,
       COUNT(DISTINCT "PedidoID") AS pedidos, COUNT(DISTINCT "ClienteID") AS clientes
FROM "FactVentas";

SELECT d."Anio", SUM(f."VentaNetaCent")/100.0 AS ventas,
       COUNT(DISTINCT f."PedidoID") AS pedidos
FROM "FactVentas" f JOIN "DimFecha" d ON f."Fecha"=d."Fecha"
GROUP BY d."Anio" ORDER BY d."Anio";

SELECT p."Categoria", SUM(f."VentaNetaCent")/100.0 AS ventas,
       SUM(f."UtilidadCent")*1.0/NULLIF(SUM(f."VentaNetaCent"),0) AS margen
FROM "FactVentas" f JOIN "DimProducto" p ON f."ProductoID"=p."ProductoID"
GROUP BY p."Categoria" ORDER BY ventas DESC;

-- Deben devolver cero filas.
SELECT "PedidoID","ProductoID",COUNT(*) FROM "FactVentas"
GROUP BY "PedidoID","ProductoID" HAVING COUNT(*)>1;
SELECT f."DetalleID" FROM "FactVentas" f LEFT JOIN "DimCliente" c
ON f."ClienteID"=c."ClienteID" WHERE c."ClienteID" IS NULL;
''')
put('06_pruebas/requirements_validacion.txt','jsonschema==4.25.1\nreferencing==0.37.0')
put('06_pruebas/consultas_aceptacion.dax','''// Ejecutar cada bloque EVALUATE por separado en Vista de consultas DAX.
// 1. Global: comparar kpis_esperados.json GLOBAL.
EVALUATE
ROW("Ventas totales",[Ventas totales],"Costo total",[Costo total],"Utilidad bruta",[Utilidad bruta],
"Margen bruto porcentual",[Margen bruto porcentual],"Numero de pedidos",[Numero de pedidos],
"Ticket promedio",[Ticket promedio],"Unidades vendidas",[Unidades vendidas],
"Clientes unicos",[Clientes unicos],"Frecuencia de compra",[Frecuencia de compra],
"Venta bruta",[Venta bruta],"Descuento total",[Descuento total],"Descuento ponderado",[Descuento ponderado])

// 2. Cada año: kpis_esperados.json 2023,2024,2025.
EVALUATE
SUMMARIZECOLUMNS(DimFecha[Anio],"Ventas totales",[Ventas totales],"Ventas anio anterior",[Ventas anio anterior],
"Crecimiento interanual",[Crecimiento interanual],"Ventas YTD",[Ventas YTD])
ORDER BY DimFecha[Anio]

// 3. Cada mes: mensuales_esperados.csv.
EVALUATE
SUMMARIZECOLUMNS(DimFecha[AnioMes],"Ventas totales",[Ventas totales],"Ventas mes anterior",[Ventas mes anterior],
"Crecimiento mensual",[Crecimiento mensual],"Ventas anio anterior",[Ventas anio anterior],
"Crecimiento interanual",[Crecimiento interanual],"Ventas YTD",[Ventas YTD])
ORDER BY DimFecha[AnioMes]

// 4. Productos planos: productos_esperados.csv. Sin Categoria en agrupación para ranking global.
EVALUATE
SUMMARIZECOLUMNS(DimProducto[ProductoID],DimProducto[Producto],"Ventas totales",[Ventas totales],
"Ranking productos",[Ranking productos],"Participacion producto",[Participacion producto])
ORDER BY DimProducto[ProductoID]

// 5. Clientes: rfm_esperado.csv. Frecuencia 0 conserva clientes sin compras.
EVALUATE
SUMMARIZECOLUMNS(DimCliente[ClienteID],"Recencia RFM",[Recencia RFM],"Frecuencia RFM",[Frecuencia RFM],
"Monetario RFM",[Monetario RFM],"R score",[R score],"F score",[F score],"M score",[M score],"Segmento RFM",[Segmento RFM])
ORDER BY DimCliente[ClienteID]

// 6. Segmentos: kpis_esperados.json Segmentos.
EVALUATE
SUMMARIZECOLUMNS(DimCliente[SegmentoRFM],"Clientes segmento",[Clientes segmento])

// 7. Categorías: hallazgos_comerciales.md.
EVALUATE
SUMMARIZECOLUMNS(DimProducto[Categoria],"Ventas por categoria",[Ventas por categoria],"Margen",[Margen bruto porcentual])
''')
# Data dictionary for every raw field, separate from star.
rawdict=[]
for p in sorted((ROOT/'01_datos/raw').glob('*.csv')):
    rows=list(csv.DictReader(p.open(encoding='utf-8')))
    for c,v in rows[0].items():
        desc='Céntimos PEN' if c.endswith('Cent') else 'Puntos básicos (100 = 1 %)' if c=='DescuentoBps' else 'Fecha ISO' if c in ['Fecha','FechaAlta'] else 'Clave sintética; ver FK en DDL' if c.endswith('ID') else 'Atributo '+c
        typ='DATE' if c in ['Fecha','FechaAlta'] else 'REAL' if c in ['Latitud','Longitud'] else 'INTEGER' if v.lstrip('-').isdigit() else 'TEXT'
        rawdict.append([p.stem,c,typ,'No',desc,v])
put('05_documentacion/diccionario_datos.md','# Diccionario de datos\n\n## Origen normalizado\n\n'+table(['Tabla','Campo','Tipo SQLite','Nulos','Descripción','Ejemplo'],rawdict)+'\n\n## Modelo estrella\n\nVer diccionario_estrella.csv para todos los campos con tipo Power BI, tipo M, nulabilidad y ejemplo. PK/FK exactas se definen en 02_sql/schema_sqlite.sql y 01_schema_postgresql.sql. Coordenadas en grados decimales. AnioMesOrden es AAAAMM, DiaSemana usa lunes=1. RecenciaDias=-1 significa sin compras, no un plazo negativo real.\n')
put('01_datos/LICENCIA_DATOS.md','# Datos sintéticos\n\nLos datos sintéticos originales de este caso se ofrecen bajo CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/ . No contienen registros reales de clientes o empresas. Nombres geográficos se usan solo como contexto. El IGV se usa como supuesto fijo didáctico, no como asesoría tributaria.\n')
print('Documentación técnica y aceptación generadas')
# Keep immediate-view instructions when documentation is regenerated.
p=ROOT/'README.md';s=p.read_text();s=s.replace('python 03_python_etl/build_docs.py','python 03_python_etl/build_docs.py\npython 03_python_etl/build_preview.py');s=s.replace('## Primer uso en Power BI','## Informe interactivo inmediato\n\nAbrir `04_powerbi/informe_interactivo.html` en un navegador, sin servidor ni conexión. Incluye cuatro vistas y filtros de año, región y categoría. Los cálculos usan JavaScript sobre los mismos datos; no ejecuta DAX. Regenerar con `build_preview.py`.\n\n## Primer uso en Power BI');p.write_text(s)
p=ROOT/'05_documentacion/modelo_estrella.md';s=p.read_text().replace('# Modelo estrella','# Modelo estrella\n\nDiagrama vectorial: [modelo_estrella.svg](modelo_estrella.svg). Fuente alternativa: modelo_estrella.dot (Graphviz opcional).');p.write_text(s)
