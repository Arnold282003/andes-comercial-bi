-- Compatible con SQLite y PostgreSQL. Importes en soles.
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
