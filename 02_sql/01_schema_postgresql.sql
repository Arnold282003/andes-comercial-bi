-- Run in a NEW empty database. Quoted names are case sensitive. Amounts in cents.
CREATE TABLE "Categorias" (
  "CategoriaID" BIGINT NOT NULL PRIMARY KEY,
  "Categoria" TEXT NOT NULL
);

CREATE TABLE "Productos" (
  "ProductoID" BIGINT NOT NULL PRIMARY KEY,
  "Producto" TEXT NOT NULL,
  "CategoriaID" BIGINT NOT NULL REFERENCES "Categorias"("CategoriaID"),
  "PrecioBaseCent" BIGINT NOT NULL,
  "CostoBaseCent" BIGINT NOT NULL
);

CREATE TABLE "Tiendas" (
  "TiendaID" BIGINT NOT NULL PRIMARY KEY,
  "Tienda" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "Ciudad" TEXT NOT NULL,
  "Zona" TEXT NOT NULL,
  "Latitud" DOUBLE PRECISION NOT NULL,
  "Longitud" DOUBLE PRECISION NOT NULL,
  "Pais" TEXT NOT NULL
);

CREATE TABLE "Vendedores" (
  "VendedorID" BIGINT NOT NULL PRIMARY KEY,
  "TiendaID" BIGINT NOT NULL REFERENCES "Tiendas"("TiendaID"),
  "Vendedor" TEXT NOT NULL
);

CREATE TABLE "Clientes" (
  "ClienteID" BIGINT NOT NULL PRIMARY KEY,
  "Cliente" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "FechaAlta" DATE NOT NULL,
  "TipoCliente" TEXT NOT NULL,
  "RecenciaDias" BIGINT NOT NULL,
  "FrecuenciaRFM" BIGINT NOT NULL,
  "MonetarioCent" BIGINT NOT NULL,
  "RScore" BIGINT NOT NULL,
  "FScore" BIGINT NOT NULL,
  "MScore" BIGINT NOT NULL,
  "SegmentoRFM" TEXT NOT NULL
);

CREATE TABLE "Calendario" (
  "Fecha" DATE NOT NULL PRIMARY KEY,
  "Anio" BIGINT NOT NULL,
  "MesNumero" BIGINT NOT NULL,
  "Mes" TEXT NOT NULL,
  "AnioMes" TEXT NOT NULL,
  "AnioMesOrden" BIGINT NOT NULL,
  "Trimestre" BIGINT NOT NULL,
  "DiaSemana" BIGINT NOT NULL
);

CREATE TABLE "Pedidos" (
  "PedidoID" BIGINT NOT NULL PRIMARY KEY,
  "Fecha" DATE NOT NULL REFERENCES "Calendario"("Fecha"),
  "ClienteID" BIGINT NOT NULL REFERENCES "Clientes"("ClienteID"),
  "TiendaID" BIGINT NOT NULL REFERENCES "Tiendas"("TiendaID"),
  "VendedorID" BIGINT NOT NULL REFERENCES "Vendedores"("VendedorID"),
  "Canal" TEXT NOT NULL
);

CREATE TABLE "DetalleVentas" (
  "DetalleID" BIGINT NOT NULL PRIMARY KEY,
  "PedidoID" BIGINT NOT NULL REFERENCES "Pedidos"("PedidoID"),
  "ProductoID" BIGINT NOT NULL REFERENCES "Productos"("ProductoID"),
  "Cantidad" BIGINT NOT NULL,
  "PrecioUnitarioCent" BIGINT NOT NULL,
  "CostoUnitarioCent" BIGINT NOT NULL,
  "DescuentoBps" BIGINT NOT NULL,
  "VentaBrutaCent" BIGINT NOT NULL,
  "DescuentoCent" BIGINT NOT NULL,
  "VentaNetaCent" BIGINT NOT NULL,
  "CostoTotalCent" BIGINT NOT NULL,
  "IGVCent" BIGINT NOT NULL,
  CHECK ("Cantidad">0),
  CHECK ("DescuentoBps" BETWEEN 0 AND 10000),
  CHECK ("VentaNetaCent">=0),
  UNIQUE ("PedidoID", "ProductoID")
);

CREATE TABLE "DimProducto" (
  "ProductoID" BIGINT NOT NULL PRIMARY KEY,
  "Producto" TEXT NOT NULL,
  "CategoriaID" BIGINT NOT NULL,
  "PrecioBaseCent" BIGINT NOT NULL,
  "CostoBaseCent" BIGINT NOT NULL,
  "Categoria" TEXT NOT NULL
);

CREATE TABLE "DimTienda" (
  "TiendaID" BIGINT NOT NULL PRIMARY KEY,
  "Tienda" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "Ciudad" TEXT NOT NULL,
  "Zona" TEXT NOT NULL,
  "Latitud" DOUBLE PRECISION NOT NULL,
  "Longitud" DOUBLE PRECISION NOT NULL,
  "Pais" TEXT NOT NULL
);

CREATE TABLE "DimVendedor" (
  "VendedorID" BIGINT NOT NULL PRIMARY KEY,
  "TiendaID" BIGINT NOT NULL,
  "Vendedor" TEXT NOT NULL
);

CREATE TABLE "DimCliente" (
  "ClienteID" BIGINT NOT NULL PRIMARY KEY,
  "Cliente" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "FechaAlta" DATE NOT NULL,
  "TipoCliente" TEXT NOT NULL,
  "RecenciaDias" BIGINT NOT NULL,
  "FrecuenciaRFM" BIGINT NOT NULL,
  "MonetarioCent" BIGINT NOT NULL,
  "RScore" BIGINT NOT NULL,
  "FScore" BIGINT NOT NULL,
  "MScore" BIGINT NOT NULL,
  "SegmentoRFM" TEXT NOT NULL
);

CREATE TABLE "DimFecha" (
  "Fecha" DATE NOT NULL PRIMARY KEY,
  "Anio" BIGINT NOT NULL,
  "MesNumero" BIGINT NOT NULL,
  "Mes" TEXT NOT NULL,
  "AnioMes" TEXT NOT NULL,
  "AnioMesOrden" BIGINT NOT NULL,
  "Trimestre" BIGINT NOT NULL,
  "DiaSemana" BIGINT NOT NULL
);

CREATE TABLE "FactVentas" (
  "DetalleID" BIGINT NOT NULL PRIMARY KEY,
  "PedidoID" BIGINT NOT NULL,
  "ProductoID" BIGINT NOT NULL REFERENCES "DimProducto"("ProductoID"),
  "Cantidad" BIGINT NOT NULL,
  "PrecioUnitarioCent" BIGINT NOT NULL,
  "CostoUnitarioCent" BIGINT NOT NULL,
  "DescuentoBps" BIGINT NOT NULL,
  "VentaBrutaCent" BIGINT NOT NULL,
  "DescuentoCent" BIGINT NOT NULL,
  "VentaNetaCent" BIGINT NOT NULL,
  "CostoTotalCent" BIGINT NOT NULL,
  "IGVCent" BIGINT NOT NULL,
  "Fecha" DATE NOT NULL REFERENCES "DimFecha"("Fecha"),
  "ClienteID" BIGINT NOT NULL REFERENCES "DimCliente"("ClienteID"),
  "TiendaID" BIGINT NOT NULL REFERENCES "DimTienda"("TiendaID"),
  "VendedorID" BIGINT NOT NULL REFERENCES "DimVendedor"("VendedorID"),
  "Canal" TEXT NOT NULL,
  "UtilidadCent" BIGINT NOT NULL,
  CHECK ("Cantidad">0),
  CHECK ("DescuentoBps" BETWEEN 0 AND 10000),
  CHECK ("VentaNetaCent">=0),
  UNIQUE ("PedidoID", "ProductoID")
);