"""Caso académico, datos sintéticos. Python >=3.10; solo biblioteca estándar.
Ejecutar desde cualquier directorio: python 03_python_etl/pipeline.py
"""
from pathlib import Path
from datetime import date,timedelta
from collections import defaultdict,Counter
from decimal import Decimal,ROUND_HALF_UP
import random,csv,json,sqlite3,hashlib
ROOT=Path(__file__).resolve().parents[1]
SEED=20261101

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def read_csv(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def rounded(n):return int(Decimal(str(n)).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
def normalize(row):
    return {k:(' '.join(v.strip().split()) if isinstance(v,str) else v) for k,v in row.items()}
def check_rows(rows,pk):
    seen=set()
    for r in rows:
        if any(v is None or v=='' for v in r.values()):raise ValueError('Valor faltante')
        if r[pk] in seen:raise ValueError('Clave duplicada: '+str(r[pk]))
        seen.add(r[pk])
def generate():
    rng=random.Random(SEED)
    categories=[dict(CategoriaID=i+1,Categoria=n) for i,n in enumerate(['Tecnología','Electrohogar','Hogar','Oficina','Deportes'])]
    specs=[('Laptop',240000,.79),('Licuadora',18000,.65),('Organizador',4500,.48),('Silla',23000,.59),('Mancuernas',12000,.61)]
    products=[]
    for i in range(1,101):
        c=(i-1)//20;n,p,ratio=specs[c];price=rounded(p*rng.uniform(.55,1.55))
        products.append(dict(ProductoID=i,Producto=f'{n} Modelo {i:03}',CategoriaID=c+1,PrecioBaseCent=price,CostoBaseCent=rounded(price*ratio)))
    locations=[('Lima','Lima','Centro',-12.046,-77.043),('Arequipa','Arequipa','Sur',-16.399,-71.536),('La Libertad','Trujillo','Norte',-8.112,-79.029),('Piura','Piura','Norte',-5.194,-80.633),('Cusco','Cusco','Sur',-13.532,-71.967),('Junín','Huancayo','Centro',-12.065,-75.204),('Lambayeque','Chiclayo','Norte',-6.771,-79.84),('Loreto','Iquitos','Oriente',-3.75,-73.253)]
    stores=[dict(TiendaID=i+1,Tienda=f'Andes {x[1]}',Region=x[0],Ciudad=x[1],Zona=x[2],Latitud=x[3],Longitud=x[4],Pais='Perú') for i,x in enumerate(locations)]
    sellers=[dict(VendedorID=i,TiendaID=(i-1)//4+1,Vendedor=f'Asesor sintético {i:02}') for i in range(1,33)]
    customers=[dict(ClienteID=i,Cliente=f'Cliente sintético {i:04}',Region=locations[rng.choices(range(8),weights=[35,14,12,10,8,8,7,6])[0]][0],FechaAlta=(date(2022,1,1)+timedelta(days=rng.randrange(365))).isoformat(),TipoCliente=rng.choices(['Persona','Negocio'],[82,18])[0]) for i in range(1,2001)]
    days=[date(2023,1,1)+timedelta(days=i) for i in range(1096)]
    monthnames=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    calendar=[dict(Fecha=d.isoformat(),Anio=d.year,MesNumero=d.month,Mes=monthnames[d.month-1],AnioMes=d.strftime('%Y-%m'),AnioMesOrden=d.year*100+d.month,Trimestre=(d.month-1)//3+1,DiaSemana=d.isoweekday()) for d in days]
    weights=[([.85,.8,1.12,.9,1.05,.94,1.3,.95,.98,1.02,1.48,1.65][d.month-1])*(1+.13*(d.year-2023))*(1.18 if d.weekday()>=5 else 1) for d in days]
    orderdates=sorted(rng.choices(days,weights=weights,k=12000))
    counts=[1]*12000
    for idx in rng.sample(range(12000),6000):counts[idx]+=1
    for _ in range(12000):counts[rng.randrange(12000)]+=1
    # Exactly 30,000 lines. Each order has a unique product selection.
    customerweights=[rng.paretovariate(2) for _ in customers]
    orders=[];details=[]
    for oi,d in enumerate(orderdates,1):
        cid=rng.choices(range(1,2001),weights=customerweights)[0]
        home=customers[cid-1]['Region'];ti=next(s['TiendaID'] for s in stores if s['Region']==home) if rng.random()<.82 else rng.randrange(1,9)
        vi=(ti-1)*4+rng.randrange(1,5)
        orders.append(dict(PedidoID=oi,Fecha=d.isoformat(),ClienteID=cid,TiendaID=ti,VendedorID=vi,Canal=rng.choices(['Tienda','Web'],[70,30])[0]))
        # Seasonal product mix and heavy-tail popularity.
        pool=list(range(1,101));chosen=[]
        for _ in range(counts[oi-1]):
            ps=rng.choices(pool,weights=[(1/(1+(p-1)%20*.12))*(1.7 if d.month==3 and 61<=p<=80 else 1)*(1.4 if d.month in [11,12] and p<=40 else 1) for p in pool])[0];pool.remove(ps);chosen.append(ps)
        for pid in chosen:
            p=products[pid-1];qty=rng.choices([1,2,3,4,5],[55,25,12,6,2])[0]
            if customers[cid-1]['TipoCliente']=='Negocio':qty+=rng.randrange(1,4)
            disc=rng.choices([0,500,1000,1500,2000],weights=[20,25,30,18,7] if d.month in [7,11,12] else [55,25,14,5,1])[0]
            price=rounded(p['PrecioBaseCent']*(1+.035*(d.year-2023)))
            cost=rounded(p['CostoBaseCent']*(1+.045*(d.year-2023))*rng.uniform(.98,1.02))
            gross=qty*price;discount=rounded(Decimal(gross)*disc/10000);net=gross-discount;tax=rounded(Decimal(net)*18/100)
            details.append(dict(DetalleID=len(details)+1,PedidoID=oi,ProductoID=pid,Cantidad=qty,PrecioUnitarioCent=price,CostoUnitarioCent=cost,DescuentoBps=disc,VentaBrutaCent=gross,DescuentoCent=discount,VentaNetaCent=net,CostoTotalCent=qty*cost,IGVCent=tax))
    raw=dict(Categorias=categories,Productos=products,Tiendas=stores,Vendedores=sellers,Clientes=customers,Pedidos=orders,DetalleVentas=details,Calendario=calendar)
    for name,rows in raw.items():write_csv(ROOT/'01_datos/raw'/f'{name}.csv',rows)
    return raw

def etl(raw):
    # Fail fast on invalid data: do not silently impute money, identifiers or dates.
    clean={name:[normalize(r) for r in rows] for name,rows in raw.items()}
    # Normalize and parse external CSV input using an explicit column contract.
    integers=set("CategoriaID ProductoID PrecioBaseCent CostoBaseCent TiendaID VendedorID ClienteID PedidoID DetalleID Cantidad PrecioUnitarioCent CostoUnitarioCent DescuentoBps VentaBrutaCent DescuentoCent VentaNetaCent CostoTotalCent IGVCent Anio MesNumero AnioMesOrden Trimestre DiaSemana".split())
    for name,rows in clean.items():
        for r in rows:
            for k,v in r.items():
                if v is None or v=='': raise ValueError(f'{name}.{k}: faltante')
                if k in integers:
                    if str(v).lstrip('-').isdigit():r[k]=int(v)
                    else:raise ValueError(f'{name}.{k}: entero inválido')
                elif k in ['Latitud','Longitud']:r[k]=float(v)
                elif k in ['Fecha','FechaAlta']:r[k]=date.fromisoformat(v).isoformat()
    for r in clean['DetalleVentas']:
        if r['Cantidad']<=0 or not 0<=r['DescuentoBps']<=10000 or min(r['PrecioUnitarioCent'],r['CostoUnitarioCent'])<=0:raise ValueError('Transacción imposible')
        g=r['Cantidad']*r['PrecioUnitarioCent'];disc=rounded(Decimal(g)*r['DescuentoBps']/10000);net=g-disc
        expected={'VentaBrutaCent':g,'DescuentoCent':disc,'VentaNetaCent':net,'CostoTotalCent':r['Cantidad']*r['CostoUnitarioCent'],'IGVCent':rounded(Decimal(net)*18/100)}
        if any(r[k]!=v for k,v in expected.items()):raise ValueError('Importes inconsistentes')
    pks={'Categorias':'CategoriaID','Productos':'ProductoID','Tiendas':'TiendaID','Vendedores':'VendedorID','Clientes':'ClienteID','Pedidos':'PedidoID','DetalleVentas':'DetalleID','Calendario':'Fecha'}
    for n,rows in clean.items():check_rows(rows,pks[n])
    cats={r['CategoriaID']:r['Categoria'] for r in clean['Categorias']};orders={r['PedidoID']:r for r in clean['Pedidos']}
    fact=[]
    for r in clean['DetalleVentas']:
        o=orders[r['PedidoID']]
        f={**r,**{k:o[k] for k in ['Fecha','ClienteID','TiendaID','VendedorID','Canal']}}
        f['UtilidadCent']=f['VentaNetaCent']-f['CostoTotalCent'];fact.append(f)
    star={'FactVentas':fact,'DimProducto':[{**r,'Categoria':cats[r['CategoriaID']]} for r in clean['Productos']],'DimTienda':clean['Tiendas'],'DimVendedor':clean['Vendedores'],'DimCliente':clean['Clientes'],'DimFecha':clean['Calendario']}
    # Frozen RFM: all historical purchases, monetary value excluding VAT.
    bycustomer=defaultdict(list)
    for f in fact:bycustomer[f['ClienteID']].append(f)
    for c in star['DimCliente']:
        fs=bycustomer[c['ClienteID']];freq=len({f['PedidoID'] for f in fs});money=sum(f['VentaNetaCent'] for f in fs)
        rec=(date(2025,12,31)-date.fromisoformat(max(f['Fecha'] for f in fs))).days if fs else -1
        rs=5 if 0<=rec<=30 else 4 if 0<=rec<=60 else 3 if 0<=rec<=120 else 2 if 0<=rec<=240 else 1 if rec>=0 else 0
        scoref=5 if freq>=12 else 4 if freq>=8 else 3 if freq>=5 else 2 if freq>=2 else 1 if freq else 0
        ms=5 if money>=2000000 else 4 if money>=1000000 else 3 if money>=500000 else 2 if money>=100000 else 1 if money else 0
        seg='Sin compras' if not freq else 'Campeones' if rs>=4 and scoref>=4 and ms>=4 else 'Leales' if rs>=3 and scoref>=3 else 'En riesgo' if rs<=2 and scoref>=3 else 'Recientes' if rs>=4 else 'Ocasionales'
        c.update(RecenciaDias=rec,FrecuenciaRFM=freq,MonetarioCent=money,RScore=rs,FScore=scoref,MScore=ms,SegmentoRFM=seg)
    for n,rows in star.items():write_csv(ROOT/'01_datos/star'/f'{n}.csv',rows)
    return clean,star

def schema(tables):
    keys={'Categorias':'CategoriaID','Productos':'ProductoID','Tiendas':'TiendaID','Vendedores':'VendedorID','Clientes':'ClienteID','Pedidos':'PedidoID','DetalleVentas':'DetalleID','Calendario':'Fecha','FactVentas':'DetalleID','DimProducto':'ProductoID','DimTienda':'TiendaID','DimVendedor':'VendedorID','DimCliente':'ClienteID','DimFecha':'Fecha'}
    refs={'Productos':{'CategoriaID':('Categorias','CategoriaID')},'Vendedores':{'TiendaID':('Tiendas','TiendaID')},'Pedidos':{'ClienteID':('Clientes','ClienteID'),'TiendaID':('Tiendas','TiendaID'),'VendedorID':('Vendedores','VendedorID'),'Fecha':('Calendario','Fecha')},'DetalleVentas':{'PedidoID':('Pedidos','PedidoID'),'ProductoID':('Productos','ProductoID')},'FactVentas':{k:(n,k) for k,n in [('ProductoID','DimProducto'),('ClienteID','DimCliente'),('TiendaID','DimTienda'),('VendedorID','DimVendedor'),('Fecha','DimFecha')]}}
    statements=[]
    for name,rows in tables.items():
        cols=[]
        for k,v in rows[0].items():
            typ='INTEGER' if isinstance(v,int) else 'REAL' if isinstance(v,float) else 'DATE' if k in ['Fecha','FechaAlta'] else 'TEXT'
            s=f'"{k}" {typ} NOT NULL'+(' PRIMARY KEY' if keys[name]==k else '')
            if k in refs.get(name,{}):t,c=refs[name][k];s+=f' REFERENCES "{t}"("{c}")'
            cols.append(s)
        if name in ['DetalleVentas','FactVentas']:cols+=['CHECK ("Cantidad">0)','CHECK ("DescuentoBps" BETWEEN 0 AND 10000)','CHECK ("VentaNetaCent">=0)','UNIQUE ("PedidoID", "ProductoID")']
        statements.append(f'CREATE TABLE "{name}" (\n  '+',\n  '.join(cols)+'\n);')
    return '\n\n'.join(statements)

def load_db(clean,star):
    # Dimension-first load works with both engines and enforced FKs.
    tables={n:clean[n] for n in ['Categorias','Productos','Tiendas','Vendedores','Clientes','Calendario','Pedidos','DetalleVentas']}
    tables.update({n:star[n] for n in ['DimProducto','DimTienda','DimVendedor','DimCliente','DimFecha','FactVentas']})
    ddl=schema(tables)
    (ROOT/'02_sql/schema_sqlite.sql').write_text(ddl,encoding='utf-8')
    pg='-- Run in a NEW empty database. Quoted names are case sensitive. Amounts in cents.\n'+ddl.replace(' INTEGER',' BIGINT').replace(' REAL',' DOUBLE PRECISION')
    (ROOT/'02_sql/01_schema_postgresql.sql').write_text(pg,encoding='utf-8')
    copy=['\\set ON_ERROR_STOP on','BEGIN;']
    for n in tables:
        folder='raw' if n in clean else 'star';cols=', '.join('"'+k+'"' for k in tables[n][0]);copy.append(f'''\\copy "{n}" ({cols}) FROM '01_datos/{folder}/{n}.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')''')
    copy+=['COMMIT;'];(ROOT/'02_sql/02_carga_postgresql.sql').write_text('\n'.join(copy),encoding='utf-8')
    path=ROOT/'01_datos/andes_comercial.sqlite'
    if path.exists():path.unlink()
    with sqlite3.connect(path) as conn:
        conn.execute('PRAGMA foreign_keys=ON');conn.executescript(ddl)
        for n,rs in tables.items():conn.executemany('INSERT INTO "'+n+'" VALUES ('+','.join('?' for _ in rs[0])+')',[tuple(r.values()) for r in rs])
        assert conn.execute('PRAGMA foreign_key_check').fetchall()==[]
    return tables

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--from-csv',action='store_true',help='Reprocesar raw existente sin regenerarlo');args=parser.parse_args()
    raw={p.stem:read_csv(p) for p in (ROOT/'01_datos/raw').glob('*.csv')} if args.from_csv else generate()
    clean,star=etl(raw);load_db(clean,star)
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'01_datos').rglob('*.csv'))}
    (ROOT/'06_pruebas/data_hashes.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'seed':SEED,'lineas':len(star['FactVentas']),'pedidos':len(clean['Pedidos']),'fechas':len(star['DimFecha']),'ventas_soles':sum(f['VentaNetaCent'] for f in star['FactVentas'])/100},indent=2))
if __name__=='__main__':main()
