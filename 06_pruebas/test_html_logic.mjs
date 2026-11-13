// Node >=18. Executes generated JS against a minimal DOM stub, not a browser renderer.
import fs from 'node:fs';import vm from 'node:vm';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html=fs.readFileSync(path.join(root,'04_powerbi/informe_interactivo.html'),'utf8');
const script=html.match(/<script>([\s\S]*)<\/script>/)[1];
const elements=new Map();function get(id){if(!elements.has(id))elements.set(id,{value:'',innerHTML:'',textContent:'',querySelectorAll:()=>[]});return elements.get(id)}
const ctx=vm.createContext({document:{getElementById:get},window:{},Intl,console});vm.runInContext(script,ctx,{timeout:10000});const cases=[];
function verify(name,expr){let pass=vm.runInContext(expr,ctx);cases.push({name,pass});if(!pass)throw Error(name)}
verify('Global exacto','window.currentSummary.v===3956459323 && window.currentSummary.orders===12000');
get('year').value='2025';get('year').onchange();verify('Año 2025','window.currentSummary.v===1518680913');
get('region').value='Lima';get('category').value='Tecnología';get('category').onchange();let filtered=ctx.window.currentSummary;
get('reset').onclick();verify('Reset','window.currentSummary.v===3956459323');
for(let i=0;i<4;i++){vm.runInContext(`active=${i};render()`,ctx);cases.push({name:'Generación DOM vista '+i,pass:get('app').innerHTML.includes('class="panel"')});}
vm.runInContext('window.empty=summary([])',ctx);verify('División nula','window.empty.margin===null && window.empty.ticket===0');
const report={motor:'Node vm con DOM simulado',casos:cases,seleccion_2025_Lima_Tecnologia:filtered,render_navegador:false,powerbi:false};fs.writeFileSync(path.join(root,'06_pruebas/validacion_html_logica.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
