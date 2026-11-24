# Kafatemor Perfumes — tienda 2.0

Aplicación de comercio electrónico en español de Uruguay, con catálogo renderizado en servidor, componentes reutilizables, JavaScript modular, backend HTTP, panel administrativo y almacenamiento opcional en Supabase. La compra se coordina exclusivamente por Instagram: la tienda genera el resumen, el cliente lo copia y lo pega en un mensaje directo. No realiza cobros ni reserva stock automáticamente.

## 1. Inicio rápido

Requisitos: Node.js **22 LTS** (compatible con la versión configurada en `package.json`), npm y un navegador moderno. No se necesitan dependencias externas de npm ni claves para ver la tienda original migrada.

```bash
npm ci
npm run build
npm test
npm run dev
```

Abrí `http://localhost:3000`. Sin variables de Supabase, los 232 productos se leen del catálogo versionado y el panel en `/admin` permanece cerrado. En Windows, si `npm` está bloqueado por la política de PowerShell, usá `npm.cmd` o la terminal CMD. El script `npm start` sirve la misma aplicación de producción sin servidor de desarrollo adicional. No abras los archivos haciendo doble clic: es una aplicación de servidor.

## 2. Publicar en GitHub

1. Descomprimí el ZIP. En GitHub creá un repositorio privado o público, según tu preferencia. Recomendamos privado para no exponer archivos comerciales versionados. No agregues un README si vas a cargar esta carpeta completa.
2. En GitHub Desktop, agregá la carpeta local y publicala, o ejecutá desde la raíz (reemplazá la URL por la de tu repositorio):

```bash
git init
git add .
git commit -m "Kafatemor: nueva tienda premium"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git push -u origin main
```

3. Si querés conservar la URL de tu tienda actual, creá primero una rama de prueba en el repositorio original o un proyecto Vercel nuevo. No sobrescribas la producción hasta revisar una vista previa. El ZIP tiene todos los archivos necesarios: no mezcles el `index.html` viejo con esta aplicación.
4. El workflow de GitHub Actions valida los módulos, catálogo y tests en cada push y pull request. No solicita claves ni despliega automáticamente por sí mismo.

## 3. Publicar en Vercel

1. Ingresá a Vercel y elegí **Add New → Project**. Importá el repositorio de GitHub.
2. Elegí **Other** como Framework Preset (no Next.js). Root Directory: la carpeta que contiene `package.json`. Node.js: **22.x**. Build Command: `npm run build`. Output Directory: `public`. Install Command: `npm ci` o el valor por defecto. Los rewrites están en `vercel.json` y la función en `api/shop.js`.
3. Configurá `SITE_URL` con la URL final, sin barra al final. Si querés ver la tienda antes de configurar el panel, podés desplegar sin las variables Supabase: el catálogo original estará disponible en modo lectura.
4. Presioná **Deploy**. Probá `/`, `/catalogo`, `/perfume/lattafa-khamrah`, `/carrito`, `/favoritos`, `/comparar`, `/descubrir`, `/admin`, `/sitemap.xml`. Verificá que las imágenes `/media/...` y los módulos `/assets/...` se sirvan directamente. En un proyecto existente eliminá configuraciones manuales de la versión anterior que contradigan `vercel.json`.
5. Para edición persistente completá el paso siguiente y redeployá. Los cambios de catálogo se sirven en cada petición y no necesitan otro despliegue.

**Nota comercial:** verificá las condiciones vigentes del plan de Vercel que uses: el plan Hobby está orientado a uso personal no comercial, por lo que una tienda puede requerir Pro u otro alojamiento permitido. La aplicación no introduce paquetes ni APIs pagas obligatorias; Supabase y el hosting están sujetos a sus planes y cuotas. También funciona en un alojamiento Node.js 22 tradicional con `npm start`.

## 4. Habilitar administración real (Supabase)

La base de datos y Auth son necesarios para editar desde `/admin`. No se entrega una contraseña ni una sesión de demostración; el servidor exige autenticación real.

1. Creá un proyecto en [Supabase](https://supabase.com). En SQL Editor, abrí y ejecutá el contenido de `supabase/schema.sql`. Creará las tablas `products`, `shop_settings` y el bucket público de imágenes `product-images`. Las tablas tienen RLS habilitado y no admiten acceso directo de `anon` ni `authenticated`.
2. En Authentication → Users, creá o invitá al usuario administrador y confirmá su correo. Configurá una contraseña larga y única. Deshabilitá el registro público de nuevos usuarios en Authentication → Sign In / Providers; esta tienda no necesita cuentas de clientes. Revisá la protección de autenticación y los límites de peticiones en el proyecto.
3. En Settings → API Keys, obtené la URL del proyecto, la clave legacy `anon` y la clave legacy `service_role` (JWT). Este adaptador REST usa ambas claves legacy. Si tu proyecto ya no ofrece esas claves, será necesario adaptar el cliente a su modelo de claves antes de activar el panel. **Nunca** compartas la clave `service_role`, ni la pegues en GitHub o en código público.
4. Copiá `.env.example` a `.env` en tu máquina y completá las variables:

| Variable | Uso |
|---|---|
| `SUPABASE_URL` | URL HTTPS del proyecto |
| `SUPABASE_ANON_KEY` | Clave anon legacy |
| `SUPABASE_SERVICE_ROLE_KEY` | Clave service_role legacy, exclusivamente servidor |
| `ADMIN_EMAILS` | Correos confirmados autorizados, separados por comas |
| `SITE_URL` | URL de la tienda en producción |
| `PORT` | Puerto local; no hace falta configurarlo en Vercel |

5. Ejecutá `npm run seed` **antes de conectar la tienda publicada a la base de datos**. Importa los 232 productos y los ajustes originales. El importador es idempotente: no sobrescribe los IDs ya existentes. No lo ejecutes después de eliminar intencionalmente productos, porque restauraría los faltantes del catálogo inicial. Si la base está configurada pero vacía, la tienda no muestra datos de respaldo: hay que importar primero.
6. En Vercel → Settings → Environment Variables, creá las mismas variables (menos `PORT`), seleccioná Production y Preview según corresponda, y redeployá. Es preferible usar una base de prueba separada para Preview para no modificar accidentalmente los datos de producción.
7. Entrá a `/admin`, iniciá sesión con el usuario creado y probá editar un producto no publicado. Revisá el resultado en otra pestaña. Si la sesión vence, volvé a ingresar. La cookie se emite con HttpOnly, SameSite=Strict y Secure en HTTPS; cada acceso de administración consulta Auth y verifica el correo confirmado contra la lista autorizada. No hay refresh automático; la sesión dura hasta una hora. El cierre elimina la cookie local; para revocar sesiones comprometidas, hacelo desde Supabase.

### Administración cotidiana

- **Productos:** crear, editar, duplicar como oculto, eliminar, buscar y paginar. El precio vacío significa consultar; stock vacío significa disponibilidad por confirmar; stock cero impide añadir. Precio anterior mayor que el actual activa la oferta. Las variantes pueden tener precio, imagen y stock propios o heredar el valor base. No hay reserva automática porque la venta se acuerda por mensaje directo.
- **Imágenes:** JPG, PNG, WebP y AVIF; hasta 12 por producto, 2,5 MB por imagen. Se suben al bucket y podés elegir la portada. Quitar una foto del producto no borra automáticamente el archivo del bucket; revisá y limpiá archivos huérfanos manualmente en Supabase Storage. Los originales migrados están en `public/media` con versiones de miniatura.
- **Categorías y marcas:** se derivan de los productos, con sugerencias de nombres existentes. Se pueden asignar varias categorías con el separador `|`; la pestaña Marcas y categorías permite renombrar en bloque o quitar una categoría. No hay una tabla separada de marcas vacías. Las familias olfativas, el género, la ocasión y las demás características se habilitan en filtros/asistente cuando existan datos cargados.
- **Acciones masivas:** seleccioná registros, elegí ocultar/mostrar, destacar, cambiar stock o precio, o añadir categoría. Confirmá la operación. Para más de 100 registros se aplican por lotes; ante un fallo parcial, revisá el catálogo y repetí solo los faltantes.
- **CSV:** exportá una copia de seguridad antes de importar. Usa coma como delimitador, encabezados en inglés y JSON para `images`, `categories` y `variants`. Los IDs existentes se actualizan; los nuevos se crean. Máximo 500 por importación (y 4 MB). Precios y stock vacíos quedan sin informar. Ejemplo mínimo: `name,brand,price` seguido de los datos reales. Los textos que comienzan con caracteres de fórmula se protegen al exportar para abrir en planillas; revisalos al reimportar.
- **Portada y textos:** editar el anuncio superior, título, descripción, imagen de portada, preguntas frecuentes y orden/visibilidad de secciones. Las ofertas reales se muestran antes que las colecciones por defecto. No aparecen descuentos ni novedades cuando no hay datos correspondientes.
- **Estadísticas:** conteos reales del catálogo (visibles, sin precio, stock pendiente). No se simulan ventas ni visitas. No hay integración de analytics o pedidos cerrados por Instagram.

## 5. Decisiones y alcance del rediseño

La versión original contenía 232 registros, 220 precios y 67 denominaciones de marca. Se conservaron los IDs, nombres, marcas y valores exactos, incluso variantes ortográficas del catálogo original; las fotografías asociadas fueron migradas a WebP. Los 12 precios ausentes no se estimaron. Una diferencia entre apóstrofo recto y tipográfico del nombre de archivo de Libre L'Eau Nue fue resuelta en la importación. Las cuatro referencias de la antigua sección de más vendidos se conservaron como **destacados**, ya que no se proporcionaron estadísticas reales de ventas. No había precios anteriores, stock, familias olfativas, categorías, género ni notas documentadas: esos campos se incorporaron para cargar información posteriormente. Se extrajeron tamaños y concentraciones exclusivamente cuando estaban escritos en el nombre original. Los nombres y precios del ZIP tienen fecha de origen abril de 2026 y deben revisarse antes de publicar.

El diseño combina azul noche, marfil y champán, tipografías de sistema, imágenes originales, tarjetas editoriales, categorías cuando existan, acceso directo a marcas, navegación móvil fija, búsqueda instantánea, favoritos, comparador, vista rápida, historial local y asistente de descubrimiento. No se añadieron valoraciones, testimonios, supuestas promociones o clasificaciones sin base. Inspiración funcional: Luckyscent (exploración de fragancias y marcas), Nose Paris (diagnóstico de preferencias). El Instagram oficial no pudo abrirse por limitación de acceso; la identidad se tomó de la marca y el ZIP original.

La arquitectura es Node.js 22, ES modules y renderizado HTML en servidor, no una sola página HTML ni un sitio estático. No se eligió Next.js/React/TypeScript porque el entorno no pudo resolver el registro npm; en vez de producir una compilación sin verificar, se implementó una aplicación sin dependencias externas con backend funcional, validaciones y pruebas. La interfaz usa CSS responsive y SVG inline propios; no usa Tailwind, Framer Motion ni Lucide como dependencia. No se incluye PWA/offline para evitar mostrar precios o disponibilidad obsoletos, ni pagos directos, ni integración automática de mensajes. No hay acceso a métricas reales de venta ni Instagram Insights. El cuestionario ofrece coincidencias según atributos registrados, no predicciones olfativas inventadas.

### Estructura

```
api/shop.js                Adaptador de Vercel Functions
src/server.js              Rutas y control de acceso
src/db.js                  Supabase REST, Auth y Storage
src/model.js               Validación, precios, stock, cotización
src/view.js                Componentes SSR y metadatos
public/assets/             CSS, módulos de interacción, logo original
public/media/              Imágenes WebP y miniaturas
 data/catalog.json         Catálogo inicial completo
 data/settings.json        Configuración editorial inicial
 data/import-report.json   Trazabilidad de fotos y productos
supabase/schema.sql        Migración y permisos
scripts/                   Validación de build e importación
 tests/                    Pruebas de modelo, HTTP y contrato de Auth/DB
.github/workflows/ci.yml    CI sin credenciales
server.js                  Servidor local / alojamiento Node
vercel.json                Configuración de rutas y assets
```

## 6. Control de calidad

`npm ci --offline`, `npm run build` y `npm test` se ejecutaron en Node.js 22.16.0. Ver `RESULTADOS-PRUEBAS.md`. Las pruebas automatizadas de Auth y escrituras usan un servidor HTTP local que simula las respuestas del contrato Supabase: no es un sustituto de probar la base de datos real. La administración de producción no usa ese simulador. Chromium/Playwright bloqueó localhost por política del entorno y no se pudieron confirmar capturas, interacciones de navegador, compatibilidad visual ni puntuaciones Lighthouse. No se afirma que la aplicación haya sido desplegada en Vercel.

Antes de publicar: revisar precios y existencia; comprobar la vista previa en 390, 768 y 1440 px, filtros y sugerencias, favorito/comparador, carrito con producto sin precio y cantidad, copiar resumen y abrir el DM en el navegador de Instagram, carga de imágenes y CRUD real con sesión, acceso anónimo rechazado, CSV y configuración editorial. Medir Lighthouse desde Chrome DevTools en la URL publicada; verificar navegación por teclado, contraste, lectores de pantalla y ausencia de desbordamiento horizontal. Revisar condiciones comerciales, envíos, cambios y devoluciones con el titular del negocio antes de añadir políticas públicas.

Referencias oficiales: [Node.js en Vercel](https://vercel.com/docs/functions/runtimes/node-js), [rewrites](https://vercel.com/docs/routing/rewrites), [Supabase Auth](https://supabase.com/docs/guides/auth), [RLS](https://supabase.com/docs/guides/database/postgres/row-level-security).

Pruebas de navegador opcionales incluidas en `tests/browser-local.py`: en un entorno sin bloqueo, instalá Python Playwright (`pip install playwright`, `python -m playwright install chromium`), iniciá `npm start` sin Supabase y ejecutá `python tests/browser-local.py`. Genera capturas PNG en la carpeta actual y prueba los flujos públicos del catálogo inicial. La prueba del panel en modo lectura requiere no configurar Supabase. Para la vista previa, configurá `BASE_URL` en el entorno. Esta dependencia es solo de pruebas opcionales, no de la tienda.
