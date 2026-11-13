"""Regenera datos, candidato PBIP, pruebas, documentación y HTML. Solo Python estándar."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
for script in ['03_python_etl/pipeline.py','03_python_etl/build_powerbi.py','06_pruebas/test_project.py','03_python_etl/build_docs.py','03_python_etl/build_preview.py']:
    print('Ejecutando',script,flush=True)
    subprocess.run([sys.executable,str(root/script)],cwd=root,check=True)
print('Completado. JSON Schema, DAX, Desktop y PostgreSQL tienen validaciones separadas.')
