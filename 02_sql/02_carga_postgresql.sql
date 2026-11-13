\set ON_ERROR_STOP on
BEGIN;
\copy "Categorias" ("CategoriaID", "Categoria") FROM '01_datos/raw/Categorias.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "Productos" ("ProductoID", "Producto", "CategoriaID", "PrecioBaseCent", "CostoBaseCent") FROM '01_datos/raw/Productos.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "Tiendas" ("TiendaID", "Tienda", "Region", "Ciudad", "Zona", "Latitud", "Longitud", "Pais") FROM '01_datos/raw/Tiendas.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "Vendedores" ("VendedorID", "TiendaID", "Vendedor") FROM '01_datos/raw/Vendedores.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "Clientes" ("ClienteID", "Cliente", "Region", "FechaAlta", "TipoCliente", "RecenciaDias", "FrecuenciaRFM", "MonetarioCent", "RScore", "FScore", "MScore", "SegmentoRFM") FROM '01_datos/raw/Clientes.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "Calendario" ("Fecha", "Anio", "MesNumero", "Mes", "AnioMes", "AnioMesOrden", "Trimestre", "DiaSemana") FROM '01_datos/raw/Calendario.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "Pedidos" ("PedidoID", "Fecha", "ClienteID", "TiendaID", "VendedorID", "Canal") FROM '01_datos/raw/Pedidos.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "DetalleVentas" ("DetalleID", "PedidoID", "ProductoID", "Cantidad", "PrecioUnitarioCent", "CostoUnitarioCent", "DescuentoBps", "VentaBrutaCent", "DescuentoCent", "VentaNetaCent", "CostoTotalCent", "IGVCent") FROM '01_datos/raw/DetalleVentas.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "DimProducto" ("ProductoID", "Producto", "CategoriaID", "PrecioBaseCent", "CostoBaseCent", "Categoria") FROM '01_datos/star/DimProducto.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "DimTienda" ("TiendaID", "Tienda", "Region", "Ciudad", "Zona", "Latitud", "Longitud", "Pais") FROM '01_datos/star/DimTienda.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "DimVendedor" ("VendedorID", "TiendaID", "Vendedor") FROM '01_datos/star/DimVendedor.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "DimCliente" ("ClienteID", "Cliente", "Region", "FechaAlta", "TipoCliente", "RecenciaDias", "FrecuenciaRFM", "MonetarioCent", "RScore", "FScore", "MScore", "SegmentoRFM") FROM '01_datos/star/DimCliente.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "DimFecha" ("Fecha", "Anio", "MesNumero", "Mes", "AnioMes", "AnioMesOrden", "Trimestre", "DiaSemana") FROM '01_datos/star/DimFecha.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
\copy "FactVentas" ("DetalleID", "PedidoID", "ProductoID", "Cantidad", "PrecioUnitarioCent", "CostoUnitarioCent", "DescuentoBps", "VentaBrutaCent", "DescuentoCent", "VentaNetaCent", "CostoTotalCent", "IGVCent", "Fecha", "ClienteID", "TiendaID", "VendedorID", "Canal", "UtilidadCent") FROM '01_datos/star/FactVentas.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
COMMIT;