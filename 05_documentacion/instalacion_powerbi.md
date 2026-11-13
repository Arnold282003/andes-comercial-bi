# Instalación y construcción en Power BI Desktop

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
