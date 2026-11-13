CREATE TABLE "Categorias" (
  "CategoriaID" INTEGER NOT NULL PRIMARY KEY,
  "Categoria" TEXT NOT NULL
);

CREATE TABLE "Productos" (
  "ProductoID" INTEGER NOT NULL PRIMARY KEY,
  "Producto" TEXT NOT NULL,
  "CategoriaID" INTEGER NOT NULL REFERENCES "Categorias"("CategoriaID"),
  "PrecioBaseCent" INTEGER NOT NULL,
  "CostoBaseCent" INTEGER NOT NULL
);

CREATE TABLE "Tiendas" (
  "TiendaID" INTEGER NOT NULL PRIMARY KEY,
  "Tienda" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "Ciudad" TEXT NOT NULL,
  "Zona" TEXT NOT NULL,
  "Latitud" REAL NOT NULL,
  "Longitud" REAL NOT NULL,
  "Pais" TEXT NOT NULL
);

CREATE TABLE "Vendedores" (
  "VendedorID" INTEGER NOT NULL PRIMARY KEY,
  "TiendaID" INTEGER NOT NULL REFERENCES "Tiendas"("TiendaID"),
  "Vendedor" TEXT NOT NULL
);

CREATE TABLE "Clientes" (
  "ClienteID" INTEGER NOT NULL PRIMARY KEY,
  "Cliente" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "FechaAlta" DATE NOT NULL,
  "TipoCliente" TEXT NOT NULL,
  "RecenciaDias" INTEGER NOT NULL,
  "FrecuenciaRFM" INTEGER NOT NULL,
  "MonetarioCent" INTEGER NOT NULL,
  "RScore" INTEGER NOT NULL,
  "FScore" INTEGER NOT NULL,
  "MScore" INTEGER NOT NULL,
  "SegmentoRFM" TEXT NOT NULL
);

CREATE TABLE "Calendario" (
  "Fecha" DATE NOT NULL PRIMARY KEY,
  "Anio" INTEGER NOT NULL,
  "MesNumero" INTEGER NOT NULL,
  "Mes" TEXT NOT NULL,
  "AnioMes" TEXT NOT NULL,
  "AnioMesOrden" INTEGER NOT NULL,
  "Trimestre" INTEGER NOT NULL,
  "DiaSemana" INTEGER NOT NULL
);

CREATE TABLE "Pedidos" (
  "PedidoID" INTEGER NOT NULL PRIMARY KEY,
  "Fecha" DATE NOT NULL REFERENCES "Calendario"("Fecha"),
  "ClienteID" INTEGER NOT NULL REFERENCES "Clientes"("ClienteID"),
  "TiendaID" INTEGER NOT NULL REFERENCES "Tiendas"("TiendaID"),
  "VendedorID" INTEGER NOT NULL REFERENCES "Vendedores"("VendedorID"),
  "Canal" TEXT NOT NULL
);

CREATE TABLE "DetalleVentas" (
  "DetalleID" INTEGER NOT NULL PRIMARY KEY,
  "PedidoID" INTEGER NOT NULL REFERENCES "Pedidos"("PedidoID"),
  "ProductoID" INTEGER NOT NULL REFERENCES "Productos"("ProductoID"),
  "Cantidad" INTEGER NOT NULL,
  "PrecioUnitarioCent" INTEGER NOT NULL,
  "CostoUnitarioCent" INTEGER NOT NULL,
  "DescuentoBps" INTEGER NOT NULL,
  "VentaBrutaCent" INTEGER NOT NULL,
  "DescuentoCent" INTEGER NOT NULL,
  "VentaNetaCent" INTEGER NOT NULL,
  "CostoTotalCent" INTEGER NOT NULL,
  "IGVCent" INTEGER NOT NULL,
  CHECK ("Cantidad">0),
  CHECK ("DescuentoBps" BETWEEN 0 AND 10000),
  CHECK ("VentaNetaCent">=0),
  UNIQUE ("PedidoID", "ProductoID")
);

CREATE TABLE "DimProducto" (
  "ProductoID" INTEGER NOT NULL PRIMARY KEY,
  "Producto" TEXT NOT NULL,
  "CategoriaID" INTEGER NOT NULL,
  "PrecioBaseCent" INTEGER NOT NULL,
  "CostoBaseCent" INTEGER NOT NULL,
  "Categoria" TEXT NOT NULL
);

CREATE TABLE "DimTienda" (
  "TiendaID" INTEGER NOT NULL PRIMARY KEY,
  "Tienda" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "Ciudad" TEXT NOT NULL,
  "Zona" TEXT NOT NULL,
  "Latitud" REAL NOT NULL,
  "Longitud" REAL NOT NULL,
  "Pais" TEXT NOT NULL
);

CREATE TABLE "DimVendedor" (
  "VendedorID" INTEGER NOT NULL PRIMARY KEY,
  "TiendaID" INTEGER NOT NULL,
  "Vendedor" TEXT NOT NULL
);

CREATE TABLE "DimCliente" (
  "ClienteID" INTEGER NOT NULL PRIMARY KEY,
  "Cliente" TEXT NOT NULL,
  "Region" TEXT NOT NULL,
  "FechaAlta" DATE NOT NULL,
  "TipoCliente" TEXT NOT NULL,
  "RecenciaDias" INTEGER NOT NULL,
  "FrecuenciaRFM" INTEGER NOT NULL,
  "MonetarioCent" INTEGER NOT NULL,
  "RScore" INTEGER NOT NULL,
  "FScore" INTEGER NOT NULL,
  "MScore" INTEGER NOT NULL,
  "SegmentoRFM" TEXT NOT NULL
);

CREATE TABLE "DimFecha" (
  "Fecha" DATE NOT NULL PRIMARY KEY,
  "Anio" INTEGER NOT NULL,
  "MesNumero" INTEGER NOT NULL,
  "Mes" TEXT NOT NULL,
  "AnioMes" TEXT NOT NULL,
  "AnioMesOrden" INTEGER NOT NULL,
  "Trimestre" INTEGER NOT NULL,
  "DiaSemana" INTEGER NOT NULL
);

CREATE TABLE "FactVentas" (
  "DetalleID" INTEGER NOT NULL PRIMARY KEY,
  "PedidoID" INTEGER NOT NULL,
  "ProductoID" INTEGER NOT NULL REFERENCES "DimProducto"("ProductoID"),
  "Cantidad" INTEGER NOT NULL,
  "PrecioUnitarioCent" INTEGER NOT NULL,
  "CostoUnitarioCent" INTEGER NOT NULL,
  "DescuentoBps" INTEGER NOT NULL,
  "VentaBrutaCent" INTEGER NOT NULL,
  "DescuentoCent" INTEGER NOT NULL,
  "VentaNetaCent" INTEGER NOT NULL,
  "CostoTotalCent" INTEGER NOT NULL,
  "IGVCent" INTEGER NOT NULL,
  "Fecha" DATE NOT NULL REFERENCES "DimFecha"("Fecha"),
  "ClienteID" INTEGER NOT NULL REFERENCES "DimCliente"("ClienteID"),
  "TiendaID" INTEGER NOT NULL REFERENCES "DimTienda"("TiendaID"),
  "VendedorID" INTEGER NOT NULL REFERENCES "DimVendedor"("VendedorID"),
  "Canal" TEXT NOT NULL,
  "UtilidadCent" INTEGER NOT NULL,
  CHECK ("Cantidad">0),
  CHECK ("DescuentoBps" BETWEEN 0 AND 10000),
  CHECK ("VentaNetaCent">=0),
  UNIQUE ("PedidoID", "ProductoID")
);