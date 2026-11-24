from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import json
base=os.environ.get('BASE_URL','http://localhost:3000').rstrip('/'); results=[]; errors=[]; bad=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True); context=b.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write']); page=context.new_page();page.set_default_timeout(4500);page.set_default_navigation_timeout(6000);page.on('pageerror',lambda e: errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
 def test(name,fn):
  try:fn();results.append([name,'PASS']);print(name,'PASS',flush=True)
  except Exception as e:results.append([name,'FAIL',str(e)[:400]]);print(name,'FAIL',str(e)[:300],flush=True)
 def home():
  page.goto(base);page.wait_for_load_state('networkidle');assert page.locator('h1').inner_text()=='El arte de dejar huella.';assert page.locator('.product-card').count()==4;page.screenshot(path='kafatemor-inicio.png',full_page=False)
 def catalog():
  page.goto(base+'/catalogo');page.wait_for_selector('#filter-brand');assert '232' in page.locator('#result-count').inner_text();page.locator('#more').click();assert page.locator('.product-card').count()==48;page.locator('#catalog-search').fill('khamrah');assert page.locator('.product-card').count()>=1;page.locator('#filter-brand').select_option('Lattafa');assert page.locator('.product-card').count()>=1;page.locator('#catalog-search').fill('zzzzz');assert 'No encontramos' in page.locator('#catalog-grid').inner_text();page.locator('#reset-filters').click();assert '232' in page.locator('#result-count').inner_text();page.screenshot(path='kafatemor-catalogo.png',full_page=False)
 def search():
  page.get_by_role('button',name='Buscar perfumes').click();page.locator('#global-search').fill('khamrah');page.wait_for_selector('.search-result');assert 'Khamrah' in page.locator('.search-result').first.inner_text();page.get_by_role('button',name='Cerrar').click()
 def detail():
  page.goto(base+'/perfume/lattafa-khamrah');page.wait_for_load_state('networkidle');assert 'Khamrah' in page.locator('h1').inner_text();page.locator('[data-zoom]').click();assert page.locator('.zoomed').is_visible();page.get_by_role('button',name='Cerrar').click();page.locator('[data-favorite]').first.click();page.locator('[data-compare]').first.click();page.screenshot(path='kafatemor-producto.png',full_page=False)
 def cart():
  page.locator('#detail-add').click();page.wait_for_selector('#order-text');assert 'Khamrah' in page.locator('#order-text').input_value();page.get_by_role('button',name='Aumentar cantidad').click();page.wait_for_function("document.querySelector('#order-text')?.value.includes('2 ×')");page.get_by_role('button',name='1. Copiar pedido').click();assert 'Khamrah' in page.evaluate('navigator.clipboard.readText()');page.get_by_role('button',name='Cerrar').click();page.goto(base+'/carrito');page.wait_for_selector('#order-text');assert '2 ×' in page.locator('#order-text').input_value();assert page.locator('a[href="https://ig.me/m/kafatemorperfumes.uy"]').count()==1;page.get_by_role('button',name='Quitar producto').click();page.wait_for_selector('.empty');assert 'vacía' in page.locator('.empty').inner_text()
 def favcompare():
  page.goto(base+'/favoritos');page.wait_for_selector('.product-card');assert 'Khamrah' in page.locator('.product-card').first.inner_text();page.goto(base+'/comparar');page.wait_for_selector('.compare-table');assert 'Khamrah' in page.locator('.compare-table').inner_text();page.goto(base+'/perfume/afnan-9pm');page.wait_for_selector('#recent-grid .product-card');assert 'Khamrah' in page.locator('#recent-grid').inner_text()
 def quiz():
  page.goto(base+'/descubrir');page.wait_for_selector('#quiz');page.locator('[name=budget]').fill('2500');page.get_by_role('button',name='Descubrir perfumes').click();page.wait_for_selector('#quiz-results .product-card');assert page.locator('#quiz-results .product-card').count()>0
 def mobile():
  page.set_viewport_size({'width':390,'height':844});page.goto(base);page.wait_for_load_state('networkidle');assert page.evaluate('document.documentElement.scrollWidth <= innerWidth');page.screenshot(path='kafatemor-movil.png',full_page=False);page.goto(base+'/catalogo');page.wait_for_selector('#filter-brand',state='attached');page.locator('#filter-toggle').click();assert page.locator('#filters').is_visible();page.locator('#filter-brand').select_option('Afnan');assert page.locator('.product-card').count()>0;assert page.evaluate('document.documentElement.scrollWidth <= innerWidth');page.goto(base+'/perfume/lattafa-khamrah');page.wait_for_load_state('networkidle');assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 def admin():
  page.goto(base+'/admin');assert 'modo lectura' in page.locator('main').inner_text();assert page.request.get(base+'/api/store/admin/data').status==503
 for n,f in [('Inicio y destacados',home),('Búsqueda, filtros y carga progresiva',catalog),('Sugerencias instantáneas',search),('Ficha y zoom',detail),('Carrito, cantidades, copia y persistencia',cart),('Favoritos, comparador y recientes',favcompare),('Asistente de presupuesto',quiz),('Responsive 390px',mobile),('Panel sin credenciales: acceso cerrado',admin)]:test(n,f)
 print(json.dumps({'results':results,'console_errors':errors,'http_errors':bad},ensure_ascii=False,indent=2));b.close();raise SystemExit(1 if any(r[1]=='FAIL' for r in results) or errors else 0)
