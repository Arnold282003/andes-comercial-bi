# Hallazgos del caso sintético

Cálculos sobre 2023–2025 completos, sin filtros. Interpretaciones hipotéticas, no conclusiones sobre el mercado peruano.

| Año | Ventas | Utilidad bruta | Margen | YoY |
| --- | --- | --- | --- | --- |
| 2023 | S/ 11,031,756.86 | S/ 2,257,991.81 | 20.47% | Sin base 2022 |
| 2024 | S/ 13,346,027.24 | S/ 2,564,572.43 | 19.22% | 20.98% |
| 2025 | S/ 15,186,809.13 | S/ 2,854,549.29 | 18.80% | 13.79% |

Las ventas de 2025 aumentaron 13.79% respecto de 2024. El margen cayó de 20.47% en 2023 a 18.80% en 2025: -1.67 puntos porcentuales. La utilidad bruta aumentó pese a la compresión del margen. Esto es compatible con los supuestos del generador (costos crecen más que precios), pero no prueba causalidad por sí solo.

## Mezcla comercial

| Categoría | Ventas | Margen |
| --- | --- | --- |
| Tecnología | S/ 32,023,589.48 | 15.61% |
| Oficina | S/ 3,022,413.30 | 37.19% |
| Electrohogar | S/ 2,334,461.12 | 30.55% |
| Deportes | S/ 1,619,530.65 | 34.94% |
| Hogar | S/ 564,598.68 | 48.96% |

La concentración en tecnología refleja precios unitarios superiores y supuestos de mezcla. Una decisión posible es revisar promociones de categorías de bajo margen, evaluando volumen e ingreso incremental; este dataset no contiene experimento causal, por lo que no permite afirmar que bajar descuentos aumentaría utilidad total.

## Distribución geográfica

| Región de tienda | Ventas |
| --- | --- |
| Lima | S/ 10,567,694.58 |
| Lambayeque | S/ 5,148,850.62 |
| La Libertad | S/ 5,141,489.59 |
| Arequipa | S/ 4,961,350.08 |
| Piura | S/ 4,228,370.07 |
| Junín | S/ 3,665,454.10 |
| Loreto | S/ 2,972,464.14 |
| Cusco | S/ 2,878,920.05 |

La región líder es Lima con 26.71% de ventas. La generación asigna mayor peso a Lima. No extrapolar participación de mercado ni evaluar productividad sin costos de tienda, área o tráfico.

## Clientes y retención

| Segmento fijo | Clientes |
| --- | --- |
| Ocasionales | 759 |
| En riesgo | 301 |
| Recientes | 208 |
| Campeones | 271 |
| Leales | 420 |
| Sin compras | 41 |

Existen 1959 compradores sobre 2 000 clientes del maestro. Los 301 clientes En riesgo merecen una hipótesis de campaña de reactivación; medir tasa incremental contra grupo de control en un caso real. RFM no predice churn automáticamente y los umbrales se definieron de forma heurística.

## Acciones exploratorias

- Revisar categorías con margen bajo y productos con descuento elevado; medir utilidad, no solo ventas.
- Preparar demanda estacional y comparar cada mes con su equivalente anual antes de interpretar cambios.
- Priorizar pruebas de retención sobre segmentos de valor histórico, documentando exclusiones y consentimiento si se usan datos reales.
- Incorporar devoluciones, gastos logísticos, inventario y pagos en una siguiente versión para ampliar la interpretación.

Los CSV de referencia y consultas SQL permiten auditar los importes. No se atribuyen mejoras de negocio a un dashboard que aún no se usó en una operación real.
