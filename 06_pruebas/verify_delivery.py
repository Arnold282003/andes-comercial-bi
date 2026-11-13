"""Verifica la integridad de la entrega original. Después de editar/regenerar es normal que cambie."""
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text())
bad=[p for p,h in manifest.items() if not (root/p).is_file() or hashlib.sha256((root/p).read_bytes()).hexdigest()!=h]
print(f'{len(manifest)-len(bad)}/{len(manifest)} archivos coinciden con la entrega original.')
for p in bad:print('Modificado o ausente:',p)
sys.exit(bool(bad))
