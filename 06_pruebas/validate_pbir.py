"""Requiere jsonschema y referencing. Valida estructura JSON, no render ni DAX."""
import json,sys
from pathlib import Path
from jsonschema import Draft7Validator
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT7
ROOT=Path(__file__).resolve().parents[1];path=ROOT/'04_powerbi/schemas/registry.json';docs=json.loads(path.read_text())
registry=Registry().with_resources((u,Resource.from_contents(d,default_specification=DRAFT7)) for u,d in docs.items())
results=[]
for p in sorted((ROOT/'04_powerbi/PBIP_CANDIDATO').rglob('*')):
 if p.suffix not in ['.json','.pbip','.pbir']:continue
 d=json.loads(p.read_text());u=d.get('$schema')
 if not u:continue
 try:
  errors=[e.message for e in Draft7Validator(docs[u],registry=registry).iter_errors(d)]
 except Exception as e:errors=[str(e)]
 results.append({'archivo':str(p.relative_to(ROOT)),'errores':errors})
(ROOT/'06_pruebas/validacion_pbir.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('Validados',len(results),'archivos; con errores',sum(bool(r['errores']) for r in results))
for r in results:
 if r['errores']:print(r)
sys.exit(any(r['errores'] for r in results))
