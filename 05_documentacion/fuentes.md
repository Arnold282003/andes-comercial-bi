# Fuentes técnicas oficiales

Consultadas el 1 de noviembre de 2026. Se usó documentación oficial para la estructura candidata, no como certificación de funcionamiento.

- PBIP: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview
- Carpetas del reporte y PBIR: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
- Definición de reporte en Fabric: https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/report-definition
- TMDL y sintaxis: https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview
- Esquemas JSON descargados desde https://developer.microsoft.com/json-schemas/fabric/ (URL exacta `$schema` en cada archivo y registro en schemas/registry.json).

PBIP referencia una carpeta de reporte. definition.pbir permite `datasetReference.byPath` relativo al modelo local. PBIR separa report, version, pages y visuals. TMDL declara tablas, columnas, medidas, particiones M y relaciones. No se editó un report.json legacy, cuyo tratamiento difiere de PBIR.

La validación JSON usa versiones declaradas explícitamente, sin asumir que cualquier versión de Desktop las soporta. Compatibilidad TMDL 1604. No se obtuvo un certificado o salida del parser TOM/TMDL. Power BI Desktop sigue siendo el punto final de aceptación.
