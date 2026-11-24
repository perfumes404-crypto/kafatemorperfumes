# Resultados reales de validación

- Node.js 22.16.0 / npm 10.9.2.
- `npm ci --offline --ignore-scripts --no-audit --no-fund`: correcto (sin dependencias externas).
- `npm run build`: correcto; comprueba sintaxis de módulos y existencia de las 232 fotografías de producto y 232 miniaturas. No es una compilación Next.js.
- `npm test`: **19 pruebas aprobadas, 0 fallidas**. Incluye modelo, 232 rutas individuales, metadatos, sitemap, carrito, precios ausentes, stock, variantes, autorización, CRUD y ajustes contra un simulador HTTP del servicio de datos. No se han creado usuarios ni datos de prueba en Supabase real.
- Comparación directa contra el catálogo original: 232/232 IDs, nombres, marcas y precios coinciden; 220 precios definidos y 12 pendientes; 67 denominaciones de marca; cuatro destacados originales conservados; 232/232 imágenes identificadas.
- Servidor local: se ejecutó y respondió por HTTP al catálogo y página inicial.
- Playwright/Chromium: intento de navegación bloqueado por política del entorno (`ERR_BLOCKED_BY_ADMINISTRATOR` al acceder a localhost). No se completaron las pruebas visuales o de interacción ni se produjeron capturas. Los flujos de JavaScript de cliente están implementados pero no certificados mediante navegador.
- Pendientes: autenticación/Storage/RLS contra proyecto Supabase real, despliegue de vista previa en Vercel, comprobación móvil en navegador, validación manual de Instagram y medición Lighthouse. No hay resultados de rendimiento inventados.

## Salida de pruebas (Node test runner)

```text

> kafatemor-perfumes@2.0.0 test
> node --test tests/*.test.js

TAP version 13
# Subtest: autorización: rechaza ausencia de sesión, correo no permitido y origen externo
ok 1 - autorización: rechaza ausencia de sesión, correo no permitido y origen externo
  ---
  duration_ms: 45.05566
  type: 'test'
  ...
# Subtest: sesión HttpOnly y operaciones CRUD, ocultar y ajustes sobre servicio simulado
ok 2 - sesión HttpOnly y operaciones CRUD, ocultar y ajustes sobre servicio simulado
  ---
  duration_ms: 55.655573
  type: 'test'
  ...
# Subtest: rutas públicas SSR, SEO y 404
ok 3 - rutas públicas SSR, SEO y 404
  ---
  duration_ms: 66.450439
  type: 'test'
  ...
# Subtest: cada una de las 232 fichas responde con nombre e imagen
ok 4 - cada una de las 232 fichas responde con nombre e imagen
  ---
  duration_ms: 322.973966
  type: 'test'
  ...
# Subtest: sitemap dinámico incluye todos los productos; robots excluye admin
ok 5 - sitemap dinámico incluye todos los productos; robots excluye admin
  ---
  duration_ms: 2.921233
  type: 'test'
  ...
# Subtest: API catálogo conserva datos originales y cotización ignora precio del cliente
ok 6 - API catálogo conserva datos originales y cotización ignora precio del cliente
  ---
  duration_ms: 7.498718
  type: 'test'
  ...
# Subtest: administración falla cerrada sin credenciales
ok 7 - administración falla cerrada sin credenciales
  ---
  duration_ms: 3.225357
  type: 'test'
  ...
# Subtest: adaptador de ruta para Vercel
ok 8 - adaptador de ruta para Vercel
  ---
  duration_ms: 2.172652
  type: 'test'
  ...
# Subtest: 232 IDs únicos, 220 precios y 12 pendientes, imágenes completas
ok 9 - 232 IDs únicos, 220 precios y 12 pendientes, imágenes completas
  ---
  duration_ms: 43.900356
  type: 'test'
  ...
# Subtest: subtotal real con cantidad
ok 10 - subtotal real con cantidad
  ---
  duration_ms: 0.418963
  type: 'test'
  ...
# Subtest: precio desconocido no se convierte en cero
ok 11 - precio desconocido no se convierte en cero
  ---
  duration_ms: 0.129105
  type: 'test'
  ...
# Subtest: rechaza stock insuficiente, agotados, ocultos y cantidades inválidas
ok 12 - rechaza stock insuficiente, agotados, ocultos y cantidades inválidas
  ---
  duration_ms: 0.318541
  type: 'test'
  ...
# Subtest: valida precio y stock de variante, exige selección
ok 13 - valida precio y stock de variante, exige selección
  ---
  duration_ms: 0.204058
  type: 'test'
  ...
# Subtest: rechaza duplicación de líneas y productos inexistentes
ok 14 - rechaza duplicación de líneas y productos inexistentes
  ---
  duration_ms: 0.262347
  type: 'test'
  ...
# Subtest: descuentos se muestran solo con precio previo válido
ok 15 - descuentos se muestran solo con precio previo válido
  ---
  duration_ms: 0.408186
  type: 'test'
  ...
# Subtest: validación de imágenes, variantes e identificadores
ok 16 - validación de imágenes, variantes e identificadores
  ---
  duration_ms: 0.489359
  type: 'test'
  ...
# Subtest: normaliza acentos y escapa HTML
ok 17 - normaliza acentos y escapa HTML
  ---
  duration_ms: 16.609861
  type: 'test'
  ...
# Subtest: portada oculta ofertas inexistentes y no inventa notas
ok 18 - portada oculta ofertas inexistentes y no inventa notas
  ---
  duration_ms: 3.033873
  type: 'test'
  ...
# Subtest: configuración filtra secciones desconocidas y textos maliciosos se escapan
ok 19 - configuración filtra secciones desconocidas y textos maliciosos se escapan
  ---
  duration_ms: 0.923285
  type: 'test'
  ...
1..19
# tests 19
# suites 0
# pass 19
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 492.09968

```
