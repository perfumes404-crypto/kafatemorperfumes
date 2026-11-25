import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import catalog from '../data/catalog.json' with {type:'json'};
import { validateProduct } from '../src/model.js';

const require = createRequire(import.meta.url);
const specs = [
  {pkg:'heic-to', entry:'heic-to/csp', files:['dist/csp/heic-to.js','dist/csp/heic-to.min.js'], out:'heic-to.js'},
  {pkg:'pako', entry:'pako/dist/pako.min.js', files:['dist/pako.min.js'], out:'pako.js'},
  {pkg:'utif', entry:'utif', files:['UTIF.js'], out:'utif.js'},
];
async function locate({pkg,entry,files}) {
  const candidates = [];
  try { candidates.push(require.resolve(entry)); } catch {}
  for (const file of files) candidates.push(path.resolve('node_modules',pkg,file));
  for (const file of new Set(candidates)) {
    try { if ((await fs.stat(file)).isFile()) return file; } catch {}
  }
  throw new Error(`No se encontró el conversor ${pkg} (${entry}). Revisá package.json, package-lock.json y la instalación de npm.`);
}
async function resolveAll() {return Promise.all(specs.map(locate));}
let sources;
try { sources = await resolveAll(); }
catch (error) {
  console.warn(`${error.message}\nReinstalando dependencias bloqueadas con npm ci...`);
  execFileSync(process.platform === 'win32' ? 'npm.cmd' : 'npm', ['ci','--include=prod','--ignore-scripts','--no-audit','--no-fund'], {stdio:'inherit',shell:process.platform==='win32'});
  sources = await resolveAll();
}
await fs.mkdir('public/assets/vendor',{recursive:true});
for (let i=0;i<specs.length;i++) {
  await fs.copyFile(sources[i],path.join('public/assets/vendor',specs[i].out));
  console.log(`Conversor incluido: ${specs[i].pkg} → ${specs[i].out}`);
}
for(const p of catalog){validateProduct(p);for(const x of p.images){await fs.access('public'+x);await fs.access('public'+x.replace('.webp','-thumb.webp'));}}
for(const x of ['model','view','cms-fields'])await fs.copyFile(`src/${x}.js`,`public/assets/${x}.js`);
for(const dir of ['src','public/assets','api','scripts','tests'])for(const file of await fs.readdir(dir))if(file.endsWith('.js'))execFileSync(process.execPath,['--check',`${dir}/${file}`],{stdio:'inherit'});
execFileSync(process.execPath,['--check','server.js']);
console.log(`Validación de producción: ${catalog.length} productos e imágenes, módulos sintácticamente válidos.`);
