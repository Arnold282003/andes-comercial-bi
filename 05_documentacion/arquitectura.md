# Arquitectura y decisiones

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
