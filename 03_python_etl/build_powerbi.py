"""Genera definiciones PBIP/PBIR/TMDL candidatas. No ejecuta Power BI Desktop."""
from pathlib import Path
import csv,json,uuid
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'04_powerbi';PROJ=OUT/'PBIP_CANDIDATO';MODEL=PROJ/'Andes.SemanticModel';REPORT=PROJ/'Andes.Report'
def put(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def js(p,o):put(p,json.dumps(o,ensure_ascii=False,indent=2))
MONEY='"S/ "#,0.00;("S/ "#,0.00);"S/ "0.00'
MEASURES=[
('Ventas totales','DIVIDE(SUM(FactVentas[VentaNetaCent]),100)',MONEY,'Ventas netas de descuentos, sin IGV, en soles.'),
('Costo total','DIVIDE(SUM(FactVentas[CostoTotalCent]),100)',MONEY,'Costo histórico de las unidades vendidas.'),
('Utilidad bruta','[Ventas totales]-[Costo total]',MONEY,'No incluye gastos operativos ni impuestos sobre renta.'),
('Margen bruto porcentual','DIVIDE([Utilidad bruta],[Ventas totales])','0.00%','Margen ponderado por ventas. Nunca promediar porcentajes de filas.'),
('Numero de pedidos','DISTINCTCOUNT(FactVentas[PedidoID])','#,0','Pedidos con al menos una línea en el contexto. No es aditivo entre productos.'),
('Ticket promedio','DIVIDE([Ventas totales],[Numero de pedidos])',MONEY,'Venta de líneas visibles por pedido visible; filtrado por categoría es ticket parcial.'),
('Unidades vendidas','SUM(FactVentas[Cantidad])','#,0','Cantidad total de artículos.'),
('Ventas anio anterior','CALCULATE([Ventas totales],SAMEPERIODLASTYEAR(DimFecha[Fecha]))',MONEY,'Mismo periodo calendario del año anterior. 2023 no tiene comparativo en este conjunto.'),
('Crecimiento interanual','VAR Prev = [Ventas anio anterior] RETURN IF(NOT ISBLANK(Prev),DIVIDE([Ventas totales]-Prev,Prev))','0.00%','BLANK cuando no hay base comparable o su valor es cero.'),
('Ventas YTD','TOTALYTD([Ventas totales],DimFecha[Fecha])',MONEY,'Acumulado hasta última fecha del contexto, reinicia en enero. Usar un año o eje AnioMes.'),
('Ventas mes anterior','IF(HASONEVALUE(DimFecha[AnioMes]),CALCULATE([Ventas totales],DATEADD(DimFecha[Fecha],-1,MONTH)))',MONEY,'Disponible con un único mes en contexto; sin total multimensual.'),
('Crecimiento mensual','VAR Prev = [Ventas mes anterior] RETURN IF(NOT ISBLANK(Prev),DIVIDE([Ventas totales]-Prev,Prev))','0.00%','Un único mes completo; comparar con mes completo previo. No usar slicer de días parciales.'),
('Clientes unicos','DISTINCTCOUNT(FactVentas[ClienteID])','#,0','Clientes compradores en el contexto, no total del maestro.'),
('Frecuencia de compra','DIVIDE([Numero de pedidos],[Clientes unicos])','0.00','Pedidos por cliente comprador del periodo visible.'),
('Ventas por categoria','[Ventas totales]',MONEY,'Colocar DimProducto[Categoria] en filas/eje. La relación hace la agrupación.'),
('Participacion producto','DIVIDE([Ventas totales],CALCULATE([Ventas totales],ALLSELECTED(DimProducto)))','0.00%','Porcentaje de la selección externa de productos y categorías; mantiene fecha, tienda y cliente.'),
('Ranking productos','IF(ISINSCOPE(DimProducto[Producto]),RANKX(ALLSELECTED(DimProducto[ProductoID],DimProducto[Producto]),[Ventas totales],,DESC,Dense))','0','Ranking denso dentro de la categoría/filtros externos visibles. Sin ranking en totales.'),
('Recencia RFM','VAR R = SELECTEDVALUE(DimCliente[RecenciaDias]) RETURN IF(R>=0,R)','0','Días desde última compra al 31/12/2025, histórico completo. -1 del archivo se muestra vacío.'),
('Frecuencia RFM','SELECTEDVALUE(DimCliente[FrecuenciaRFM])','0','Pedidos de un cliente en 2023–2025, snapshot fijo.'),
('Monetario RFM','DIVIDE(SELECTEDVALUE(DimCliente[MonetarioCent]),100)',MONEY,'Venta histórica de un cliente, snapshot fijo.'),
('R score','SELECTEDVALUE(DimCliente[RScore])','0','1–5 por recencia, cero sin compras.'),
('F score','SELECTEDVALUE(DimCliente[FScore])','0','1–5 por frecuencia, cero sin compras.'),
('M score','SELECTEDVALUE(DimCliente[MScore])','0','1–5 por monetario, cero sin compras.'),
('Segmento RFM','SELECTEDVALUE(DimCliente[SegmentoRFM])','','Etiqueta fija por cliente, sin etiqueta total.'),
('Clientes segmento','COUNTROWS(DimCliente)','#,0','Cuenta clientes del maestro por segmento fijo, no cambia con fecha o tienda.'),
('Venta bruta','DIVIDE(SUM(FactVentas[VentaBrutaCent]),100)',MONEY,'Venta antes de descuentos, sin IGV.'),
('Descuento total','DIVIDE(SUM(FactVentas[DescuentoCent]),100)',MONEY,'Descuento monetario redondeado por línea.'),
('Descuento ponderado','DIVIDE([Descuento total],[Venta bruta])','0.00%','Descuento efectivo ponderado por venta bruta.')]

def main():
    js(OUT/'medidas.json',[dict(nombre=n,dax=d,formato=f,explicacion=e) for n,d,f,e in MEASURES])
    put(OUT/'medidas.dax','\n\n'.join(f'// {e}\n// Formato: {f}\n{n} = {d}' for n,d,f,e in MEASURES))
    put(MODEL/'definition/database.tmdl','database\n\tcompatibilityLevel: 1604\n')
    tables={p.stem:list(csv.DictReader(p.open(encoding='utf-8'))) for p in sorted((ROOT/'01_datos/star').glob('*.csv'))}
    put(MODEL/'definition/model.tmdl','model Model\n\tculture: es-PE\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-US\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\n'+''.join(f'ref table {n}\n' for n in tables))
    js(MODEL/'definition.pbism',{'version':'4.0','settings':{}})
    path='C:/BI_Peru/peru_bi/01_datos/star/'
    expr=f'"{path}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]'
    put(OUT/'powerquery/pRuta.m',expr)
    put(MODEL/'definition/expressions.tmdl','expression pRuta = '+expr+'\n')
    dictrows=[]
    for name,rows in tables.items():
        text=f'table {name}\n'
        if name=='DimFecha':text+='\tdataCategory: Time\n'
        pairs=[]
        for col,s in rows[0].items():
            datecol=col in ['Fecha','FechaAlta'];number=col in ['Latitud','Longitud'];integer=not datecol and not number and s.lstrip('-').isdigit()
            datatype='dateTime' if datecol else 'double' if number else 'int64' if integer else 'string'
            mtype='type date' if datecol else 'type number' if number else 'Int64.Type' if integer else 'type text'
            pairs.append('{"'+col+'", '+mtype+'}')
            text+=f'\n\tcolumn {col}\n\t\tdataType: {datatype}\n\t\tsourceColumn: {col}\n\t\tsummarizeBy: none\n'
            if name=='DimFecha' and col=='Fecha':text+='\t\tisKey\n'
            if datecol:text+='\t\tformatString: yyyy-mm-dd\n'
            if name=='DimFecha' and col=='Mes':text+='\t\tsortByColumn: MesNumero\n'
            if name=='DimFecha' and col=='AnioMes':text+='\t\tsortByColumn: AnioMesOrden\n'
            if col.endswith('Cent') and name=='FactVentas':text+='\t\tisHidden\n'
            desc='Importe entero en céntimos de PEN' if col.endswith('Cent') else 'Clave de identificación sintética' if col.endswith('ID') else 'Fecha ISO calendario' if datecol else 'Descuento en puntos básicos (100 = 1%)' if col=='DescuentoBps' else 'Atributo de análisis: '+col
            dictrows.append(dict(Tabla=name,Campo=col,TipoPowerBI=datatype,TipoM=mtype,Nulos='No',Descripcion=desc,Ejemplo=s))
        m=f'''let
    Source = Csv.Document(File.Contents(pRuta & "{name}.csv"),[Delimiter=",", Columns={len(rows[0])}, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers,{{{', '.join(pairs)}}},"en-US"),
    TextCols = Table.ColumnsOfType(Typed,{{type text}}),
    Clean = Table.TransformColumns(Typed,List.Transform(TextCols,each {{_, Text.Trim, type text}}))
in
    Clean'''
        put(OUT/'powerquery'/f'{name}.m',m)
        text+=f'\n\tpartition {name} = m\n\t\tmode: import\n\t\tsource =\n'+''.join('\t\t\t\t'+line+'\n' for line in m.splitlines())
        if name=='FactVentas':
            for n,d,f,e in MEASURES:
                text+=f"\n\t/// {e}\n\tmeasure '{n}' = {d}\n"
                if f:text+='\t\tformatString: '+f+'\n'
                text+='\t\tdisplayFolder: '+('RFM fijo' if n in ['Recencia RFM','Frecuencia RFM','Monetario RFM','R score','F score','M score','Segmento RFM','Clientes segmento'] else 'Indicadores')+'\n'
        put(MODEL/'definition/tables'/f'{name}.tmdl',text)
    relationships=[]
    for dim,col in [('DimFecha','Fecha'),('DimCliente','ClienteID'),('DimProducto','ProductoID'),('DimTienda','TiendaID'),('DimVendedor','VendedorID')]:
        relationships.append(f'relationship {uuid.uuid5(uuid.NAMESPACE_DNS,dim)}\n\tfromColumn: FactVentas.{col}\n\ttoColumn: {dim}.{col}\n\tcrossFilteringBehavior: oneDirection\n')
    put(MODEL/'definition/relationships.tmdl','\n'.join(relationships))
    with (ROOT/'05_documentacion/diccionario_estrella.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=dictrows[0]);w.writeheader();w.writerows(dictrows)
    js(PROJ/'Andes.pbip',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':'Andes.Report'}}],'settings':{'enableAutoRecovery':True}})
    js(REPORT/'definition.pbir',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../Andes.SemanticModel'}}})
    def sch(kind,v):return f'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/{kind}/{v}/schema.json'
    js(REPORT/'definition/version.json',{'$schema':sch('versionMetadata','1.0.0'),'version':'4.0.0'})
    # Theme import is manual to avoid claiming a Desktop-registered resource.
    js(REPORT/'definition/report.json',{'$schema':sch('report','2.0.0'),'themeCollection':{}})
    js(OUT/'tema_andes.json',{'name':'Andes Comercial','dataColors':['#087F8C','#16324F','#F2B134','#7B6D8D','#DB5461','#68B0AB'],'background':'#F4F7FA','foreground':'#16324F','tableAccent':'#087F8C','textClasses':{'title':{'fontFace':'Segoe UI','fontSize':14},'label':{'fontFace':'Segoe UI','fontSize':11},'callout':{'fontFace':'Segoe UI','fontSize':28}}})
    def col(t,p):return {'Column':{'Expression':{'SourceRef':{'Entity':t}},'Property':p}}
    def measure(p):return {'Measure':{'Expression':{'SourceRef':{'Entity':'FactVentas'}},'Property':p}}
    def projection(f):
        x=next(iter(f.values()));return {'field':f,'queryRef':x['Expression']['SourceRef']['Entity']+'.'+x['Property'],'nativeQueryRef':x['Property']}
    pages=[('01_resumen','Resumen ejecutivo'),('02_productos','Productos y rentabilidad'),('03_clientes','Análisis de clientes'),('04_geografia','Geografía y tiempo')]
    js(REPORT/'definition/pages/pages.json',{'$schema':sch('pagesMetadata','1.0.0'),'pageOrder':[p[0] for p in pages],'activePageName':pages[0][0]})
    spec=[]
    def visual(page,name,title,kind,x,y,w,h,fields):
        roles={role:{'projections':[projection(f) for f in fs]} for role,fs in fields.items()}
        literal=lambda v: {'expr':{'Literal':{'Value':v}}}
        title_obj={'title':[{'properties':{'show':literal('true'),'text':literal("'"+title+"'")}}]}
        obj={'$schema':sch('visualContainer','2.1.0'),'name':name,'position':{'x':x,'y':y,'z':len(spec),'width':w,'height':h,'tabOrder':len(spec)},'visual':{'visualType':kind,'query':{'queryState':roles},'visualContainerObjects':title_obj,'drillFilterOtherVisuals':True}}

        js(REPORT/f'definition/pages/{page}/visuals/{name}/visual.json',obj)
        spec.append(dict(Pagina=page,Visual=name,Titulo=title,Tipo=kind,X=x,Y=y,Ancho=w,Alto=h,Campos={k:[projection(f)['queryRef'] for f in v] for k,v in fields.items()}))
    for pid,title in pages:
        js(REPORT/f'definition/pages/{pid}/page.json',{'$schema':sch('page','2.0.0'),'name':pid,'displayName':title,'displayOption':'FitToPage','width':1440,'height':900})
        for i,(t,c) in enumerate([('DimFecha','Anio'),('DimTienda','Region'),('DimProducto','Categoria')]):visual(pid,'slicer'+str(i),c,'slicer',24+465*i,16,440,80,{'Values':[col(t,c)]})
    pid=pages[0][0]
    for i,n in enumerate(['Ventas totales','Utilidad bruta','Margen bruto porcentual','Numero de pedidos','Ticket promedio']):visual(pid,'kpi'+str(i),n,'card',24+i*280,112,265,125,{'Values':[measure(n)]})
    visual(pid,'mensual','Ventas por mes','lineChart',24,260,900,290,{'Category':[col('DimFecha','AnioMes')],'Y':[measure('Ventas totales')]})
    visual(pid,'anual','Comparación anual','clusteredColumnChart',948,260,468,290,{'Category':[col('DimFecha','Anio')],'Y':[measure('Ventas totales'),measure('Ventas anio anterior')]})
    visual(pid,'rentabilidad','Rentabilidad por año','tableEx',24,575,1392,290,{'Values':[col('DimFecha','Anio'),measure('Ventas totales'),measure('Costo total'),measure('Utilidad bruta'),measure('Crecimiento interanual')]})
    pid=pages[1][0]
    visual(pid,'ranking','Ranking de productos','tableEx',24,115,690,360,{'Values':[col('DimProducto','Producto'),measure('Ventas totales'),measure('Ranking productos'),measure('Participacion producto')]})
    visual(pid,'categoria','Ventas por categoría','clusteredBarChart',738,115,678,360,{'Category':[col('DimProducto','Categoria')],'Y':[measure('Ventas por categoria')]})
    visual(pid,'bajo_margen','Productos menos rentables: ordenar por margen','tableEx',24,500,690,365,{'Values':[col('DimProducto','Producto'),measure('Utilidad bruta'),measure('Margen bruto porcentual')]})
    visual(pid,'descuentos','Descuento y margen por categoría','tableEx',738,500,678,365,{'Values':[col('DimProducto','Categoria'),measure('Descuento total'),measure('Descuento ponderado'),measure('Margen bruto porcentual')]})
    pid=pages[2][0]
    for i,n in enumerate(['Clientes unicos','Frecuencia de compra','Ticket promedio']):visual(pid,'kpi'+str(i),n,'card',24+465*i,112,440,125,{'Values':[measure(n)]})
    visual(pid,'rfm','Clientes por RFM fijo al 31/12/2025','clusteredBarChart',24,260,600,260,{'Category':[col('DimCliente','SegmentoRFM')],'Y':[measure('Clientes segmento')]})
    visual(pid,'clientes','Clientes de mayor valor','tableEx',648,260,768,605,{'Values':[col('DimCliente','Cliente'),measure('Ventas totales'),measure('Recencia RFM'),measure('Frecuencia RFM'),measure('Monetario RFM'),measure('Segmento RFM')]})
    visual(pid,'evolucion','Clientes compradores por mes','lineChart',24,545,600,320,{'Category':[col('DimFecha','AnioMes')],'Y':[measure('Clientes unicos')]})
    pid=pages[3][0]
    visual(pid,'region','Ventas por región de la tienda','clusteredBarChart',24,115,690,350,{'Category':[col('DimTienda','Region')],'Y':[measure('Ventas totales')]})
    visual(pid,'zonas','Ventas y margen por zona','tableEx',738,115,678,350,{'Values':[col('DimTienda','Zona'),measure('Ventas totales'),measure('Margen bruto porcentual')]})
    visual(pid,'temporal','Tendencia y comparación interanual','lineChart',24,490,690,375,{'Category':[col('DimFecha','AnioMes')],'Y':[measure('Ventas totales'),measure('Ventas anio anterior')]})
    visual(pid,'estacional','Estacionalidad por mes y año','clusteredColumnChart',738,490,678,375,{'Category':[col('DimFecha','Mes')],'Series':[col('DimFecha','Anio')],'Y':[measure('Ventas totales')]})
    js(OUT/'especificacion_visuales.json',spec)
    # Calendar alternative, same three complete years.
    put(OUT/'powerquery/calendario_alternativo.m','''let
    Fechas = List.Dates(#date(2023,1,1),1096,#duration(1,0,0,0)),
    Tabla = Table.FromList(Fechas,Splitter.SplitByNothing(),{"Fecha"}),
    Tipo = Table.TransformColumnTypes(Tabla,{{"Fecha", type date}}),
    Anio = Table.AddColumn(Tipo,"Anio",each Date.Year([Fecha]),Int64.Type),
    MesNumero = Table.AddColumn(Anio,"MesNumero",each Date.Month([Fecha]),Int64.Type),
    Mes = Table.AddColumn(MesNumero,"Mes",each {"Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"}{[MesNumero]-1},type text),
    AnioMes = Table.AddColumn(Mes,"AnioMes",each Date.ToText([Fecha],"yyyy-MM"),type text),
    Orden = Table.AddColumn(AnioMes,"AnioMesOrden",each [Anio]*100+[MesNumero],Int64.Type),
    Tri = Table.AddColumn(Orden,"Trimestre",each Date.QuarterOfYear([Fecha]),Int64.Type),
    Dia = Table.AddColumn(Tri,"DiaSemana",each Date.DayOfWeek([Fecha],Day.Monday)+1,Int64.Type)
in Dia''')
    print('PBIP candidato:',len(spec),'visuales;',len(MEASURES),'medidas')
if __name__=='__main__':main()
