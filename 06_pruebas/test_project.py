"""Pruebas ejecutables sin Power BI. python 06_pruebas/test_project.py"""
import sys,csv,json,sqlite3,unittest,hashlib
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
from datetime import date,timedelta
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'03_python_etl'))
from pipeline import normalize,check_rows,etl

def load(n,folder='star'):
    with (ROOT/'01_datos'/folder/(n+'.csv')).open(encoding='utf-8') as f:return list(csv.DictReader(f))
def cents(v):return int(Decimal(v).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
def calc(rows):
    net=sum(int(r['VentaNetaCent']) for r in rows);cost=sum(int(r['CostoTotalCent']) for r in rows);orders=len({r['PedidoID'] for r in rows});clients=len({r['ClienteID'] for r in rows});gross=sum(int(r['VentaBrutaCent']) for r in rows);disc=sum(int(r['DescuentoCent']) for r in rows)
    return {'Ventas totales':net/100,'Costo total':cost/100,'Utilidad bruta':(net-cost)/100,'Margen bruto porcentual':(net-cost)/net if net else None,'Numero de pedidos':orders,'Ticket promedio':net/100/orders if orders else None,'Unidades vendidas':sum(int(r['Cantidad']) for r in rows),'Clientes unicos':clients,'Frecuencia de compra':orders/clients if clients else None,'Ventas por categoria':net/100,'Venta bruta':gross/100,'Descuento total':disc/100,'Descuento ponderado':disc/gross if gross else None}
F=load('FactVentas');D=load('DimCliente');P=load('DimProducto');T=load('DimTienda')
DB=sqlite3.connect(ROOT/'01_datos/andes_comercial.sqlite')
class DataTests(unittest.TestCase):
    def test_volume(self):self.assertEqual((len(F),len(load('Pedidos','raw')),len(load('DimFecha'))),(30000,12000,1096))
    def test_primary_keys_and_missing(self):
        for folder in ['raw','star']:
            for p in (ROOT/'01_datos'/folder).glob('*.csv'):
                rs=list(csv.DictReader(p.open(encoding='utf-8')));check_rows(rs,next(iter(rs[0])))
    def test_foreign_keys(self):self.assertEqual(DB.execute('PRAGMA foreign_key_check').fetchall(),[])
    def test_calendar_continuous(self):self.assertEqual([r['Fecha'] for r in load('DimFecha')],[(date(2023,1,1)+timedelta(days=i)).isoformat() for i in range(1096)])
    def test_line_arithmetic(self):
        for r in F:
            q=int(r['Cantidad']);price=int(r['PrecioUnitarioCent']);bps=int(r['DescuentoBps']);gross=q*price;disc=cents(Decimal(gross)*bps/10000);net=gross-disc
            self.assertGreater(q,0);self.assertTrue(0<=bps<=2000);self.assertEqual(int(r['VentaNetaCent']),net);self.assertEqual(int(r['DescuentoCent']),disc);self.assertEqual(int(r['CostoTotalCent']),q*int(r['CostoUnitarioCent']));self.assertEqual(int(r['IGVCent']),cents(Decimal(net)*18/100));self.assertEqual(int(r['UtilidadCent']),net-int(r['CostoTotalCent']))
    def test_order_consistency(self):
        seen={};prods=set();sellers={r['VendedorID']:r['TiendaID'] for r in load('Vendedores','raw')}
        for r in F:
            key=r['PedidoID'];t=tuple(r[k] for k in ['Fecha','ClienteID','TiendaID','VendedorID','Canal'])
            if key in seen:self.assertEqual(seen[key],t)
            seen[key]=t;pair=(key,r['ProductoID']);self.assertNotIn(pair,prods);prods.add(pair);self.assertEqual(sellers[r['VendedorID']],r['TiendaID'])
    def test_raw_to_star_reconciliation(self):
        raw=load('DetalleVentas','raw');self.assertEqual(len(raw),len(F))
        for a,b in zip(raw,F):
            for k,v in a.items():self.assertEqual(v,b[k])
    def test_sql_python_all_periods(self):
        for y in ['', '2023','2024','2025']:
            rows=[r for r in F if r['Fecha'].startswith(y)];m=calc(rows)
            sql=DB.execute('SELECT SUM("VentaNetaCent"),SUM("CostoTotalCent"),COUNT(DISTINCT "PedidoID"),COUNT(DISTINCT "ClienteID"),SUM("Cantidad") FROM "FactVentas" WHERE "Fecha" LIKE ?', (y+'%',)).fetchone()
            self.assertEqual(sql,(round(m['Ventas totales']*100),round(m['Costo total']*100),m['Numero de pedidos'],m['Clientes unicos'],m['Unidades vendidas']))
    def test_rfm(self):
        for c in D:
            rs=[r for r in F if r['ClienteID']==c['ClienteID']];n=len({r['PedidoID'] for r in rs});self.assertEqual(int(c['FrecuenciaRFM']),n);self.assertEqual(int(c['MonetarioCent']),sum(int(r['VentaNetaCent']) for r in rs))
            rec=(date(2025,12,31)-date.fromisoformat(max(r['Fecha'] for r in rs))).days if rs else -1;self.assertEqual(int(c['RecenciaDias']),rec)
    def test_clients_registered_before_purchase(self):
        clients={r['ClienteID']:r['FechaAlta'] for r in D}
        self.assertTrue(all(r['Fecha']>=clients[r['ClienteID']] for r in F))
    def test_normalization(self):self.assertEqual(normalize({'a':'  Lima   Norte  ','b':1}),{'a':'Lima Norte','b':1})
    def test_reject_duplicate(self):
        with self.assertRaises(ValueError):check_rows([{'id':1},{'id':1}],'id')
    def test_reject_missing(self):
        with self.assertRaises(ValueError):check_rows([{'id':1,'value':''}],'id')
    def test_all_months_have_sales(self):self.assertEqual(len({r['Fecha'][:7] for r in F}),36)
    def test_no_stock_or_credit_assumptions(self):
        # The project covers completed sales only. No inventory/payment assertions inferred.
        self.assertTrue(all(int(r['CostoUnitarioCent'])>0 and int(r['PrecioUnitarioCent'])>0 for r in F))
    def test_invalid_type_rejected(self):
        raw={p.stem:list(csv.DictReader(p.open(encoding='utf-8'))) for p in (ROOT/'01_datos/raw').glob('*.csv')};raw['DetalleVentas'][0]['Cantidad']='1.5'
        with self.assertRaises(ValueError):etl(raw)
    def test_negative_quantity_rejected(self):
        raw={p.stem:list(csv.DictReader(p.open(encoding='utf-8'))) for p in (ROOT/'01_datos/raw').glob('*.csv')};raw['DetalleVentas'][0]['Cantidad']='-2'
        with self.assertRaises(ValueError):etl(raw)
    def test_corrupted_money_rejected(self):
        raw={p.stem:list(csv.DictReader(p.open(encoding='utf-8'))) for p in (ROOT/'01_datos/raw').glob('*.csv')};raw['DetalleVentas'][0]['VentaNetaCent']='1'
        with self.assertRaises(ValueError):etl(raw)
    def test_rfm_scores_and_labels(self):
        for c in D:
            rec=int(c['RecenciaDias']);freq=int(c['FrecuenciaRFM']);money=int(c['MonetarioCent'])
            rs=0 if rec<0 else 1+sum(rec<=x for x in [240,120,60,30]);fs=sum(freq>=x for x in [1,2,5,8,12]);ms=sum(money>=x for x in [1,100000,500000,1000000,2000000])
            self.assertEqual([int(c[k]) for k in ['RScore','FScore','MScore']],[rs,fs,ms])
            seg='Sin compras' if not freq else 'Campeones' if min(rs,fs,ms)>=4 else 'Leales' if min(rs,fs)>=3 else 'En riesgo' if rs<=2 and fs>=3 else 'Recientes' if rs>=4 else 'Ocasionales'
            self.assertEqual(c['SegmentoRFM'],seg)
    def test_zero_division_reference(self):
        m=calc([]);self.assertIsNone(m['Margen bruto porcentual']);self.assertIsNone(m['Ticket promedio']);self.assertIsNone(m['Frecuencia de compra'])
    def test_hashes(self):
        hashes=json.loads((ROOT/'06_pruebas/data_hashes.json').read_text())
        self.assertTrue(all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items()))
    def test_monthly_sql_python(self):
        for ym in sorted({r['Fecha'][:7] for r in F}):
            net=sum(int(r['VentaNetaCent']) for r in F if r['Fecha'].startswith(ym));self.assertEqual(DB.execute('SELECT SUM("VentaNetaCent") FROM "FactVentas" WHERE substr("Fecha",1,7)=?',(ym,)).fetchone()[0],net)
    def test_product_selection_denominator(self):
        selected={r['ProductoID'] for r in P if r['Categoria']=='Hogar'};vals=[sum(int(f['VentaNetaCent']) for f in F if f['ProductoID']==p) for p in selected];den=sum(vals);self.assertAlmostEqual(sum(v/den for v in vals),1)

def expected():
    out={};total=calc(F)
    for year in [2023,2024,2025]:
        rs=[r for r in F if r['Fecha'].startswith(str(year))];m=calc(rs);prev=calc([r for r in F if r['Fecha'].startswith(str(year-1))])['Ventas totales'] or None
        m.update({'Ventas anio anterior':prev,'Crecimiento interanual':(m['Ventas totales']-prev)/prev if prev else None,'Ventas YTD':m['Ventas totales'],'Ventas mes anterior':None,'Crecimiento mensual':None});out[str(year)]=m
    out['GLOBAL']=total
    monthly=[]
    for ym in sorted({r['Fecha'][:7] for r in F}):
        rs=[r for r in F if r['Fecha'].startswith(ym)];m=calc(rs);y,mo=map(int,ym.split('-'));previous=(date(y,mo,1)-timedelta(days=1)).strftime('%Y-%m');prior=f'{y-1}-{mo:02}'
        p=calc([r for r in F if r['Fecha'].startswith(previous)])['Ventas totales'] or None;py=calc([r for r in F if r['Fecha'].startswith(prior)])['Ventas totales'] or None
        m.update({'AnioMes':ym,'Ventas mes anterior':p,'Crecimiento mensual':(m['Ventas totales']-p)/p if p else None,'Ventas anio anterior':py,'Crecimiento interanual':(m['Ventas totales']-py)/py if py else None,'Ventas YTD':sum(int(r['VentaNetaCent']) for r in F if r['Fecha'][:4]==str(y) and r['Fecha'][:7]<=ym)/100});monthly.append(m)
    prods=[]
    for p in P:
        m=calc([r for r in F if r['ProductoID']==p['ProductoID']]);prods.append({'ProductoID':p['ProductoID'],'Producto':p['Producto'],'Categoria':p['Categoria'],**m})
    values=sorted({p['Ventas totales'] for p in prods},reverse=True)
    for p in prods:p.update({'Ranking productos':values.index(p['Ventas totales'])+1,'Participacion producto':p['Ventas totales']/total['Ventas totales']})
    rfm=[{'ClienteID':c['ClienteID'],'Recencia RFM':None if int(c['RecenciaDias'])<0 else int(c['RecenciaDias']),'Frecuencia RFM':int(c['FrecuenciaRFM']),'Monetario RFM':int(c['MonetarioCent'])/100,'R score':int(c['RScore']),'F score':int(c['FScore']),'M score':int(c['MScore']),'Segmento RFM':c['SegmentoRFM']} for c in D]
    out['Segmentos']=dict(Counter(c['SegmentoRFM'] for c in D))
    folder=ROOT/'06_pruebas';(folder/'kpis_esperados.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    for name,rows in [('mensuales_esperados',monthly),('productos_esperados',prods),('rfm_esperado',rfm)]:
        with (folder/(name+'.csv')).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    return out

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(DataTests)
    with (ROOT/'06_pruebas/test_log.txt').open('w',encoding='utf-8') as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    expected();report={'ejecutadas':result.testsRun,'fallos':len(result.failures),'errores':len(result.errors),'motor':'Python unittest + SQLite','dax_ejecutado':False,'powerbi_desktop_abierto':False,'postgresql_ejecutado':False}
    (ROOT/'06_pruebas/resultado_pruebas.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));sys.exit(not result.wasSuccessful())
