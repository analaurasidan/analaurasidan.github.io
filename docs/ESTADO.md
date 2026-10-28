# Estado de migración — 28 de octubre de 2026

## Preparado localmente

- Proyecto y repositorio Git local: `/Users/analaura/Documents/Portfolio-Web`.
- Sitio generado: `public/`.
- Nueve rutas del original, más `404.html` para alojamiento estático.
- 425 recursos localizados, incluidos módulos cargados bajo demanda y dos archivos binarios de contenido CMS publicado.
- Inicio conserva el reproductor de Spotify.
- Adaptaciones: rutas relativas con slash final, logo hacia Inicio, correo normalizado, retiro de barra de edición y analítica de Framer, lectura de rangos CMS desde archivos estáticos.
- Build reproducible sin red ni instalación de dependencias.
- Flujo de GitHub Pages preparado con las versiones de acciones indicadas en la documentación oficial consultada: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Verificación realizada

- `python3 scripts/build.py`: OK.
- `python3 scripts/verify.py`: 10 documentos HTML, 38 módulos, 390 referencias a recursos y 17 enlaces distintos revisados; cero errores. Ver `static-checks.json`.
- En navegador, Inicio muestra imágenes locales y la playlist Workland de Spotify.
- Navegación real Inicio → Projects → CashFly → About: OK; enlaces de navegación desde un proyecto apuntan a las rutas correctas.
- Vista móvil de 390 px: menú abre y permite llegar a Contact; correo normalizado; sin desbordamiento horizontal observado.
- Filmo acá, Busuu, InnFlow y 404 abren a 390 px sin imágenes terminadas con error ni imágenes apuntando a servidores externos en las comprobaciones DOM realizadas.
- Se corrigió un error inicial de URL base del lector CMS. No se observaron errores nuevos de ejecución en el registro después de esa corrección durante las pruebas posteriores.
- Se hizo un build temporal con CSP que permite recursos propios y el iframe de Spotify, bloqueando los servidores de Framer. Inicio, Projects, los cuatro proyectos, About, Contact y 404 cargaron con contenido; el registro de esa sesión no mostró errores ni advertencias. Las cuatro imágenes del catálogo cargaron desde el servidor local. El video de About llegó a `readyState=4` con una URL local.
- Después de esa prueba se regeneró el build normal, sin la CSP temporal. Se puede repetir con `python3 scripts/build.py --verify-local` y volver al normal con `python3 scripts/build.py`.

Esto es una comprobación local, no una auditoría completa de accesibilidad ni garantía de identidad visual píxel a píxel. Falta verificar la versión publicada y la reproducción de ambos videos en todos los contextos pertinentes; se verificó la carga del video visible en About. Spotify seguirá necesitando internet y su servicio externo.

## GitHub y publicación

Cuenta autenticada por el conector: `analaurasidan`. Ana Laura creó el repositorio público `analaurasidan.github.io` y lo autorizó en la instalación del conector. Se transfirieron los 477 contenidos únicos correspondientes a los 889 archivos iniciales, verificando sus SHA de Git; no hubo errores de transferencia.

Repositorio: https://github.com/analaurasidan/analaurasidan.github.io

Web publicada y verificada: https://analaurasidan.github.io/

Commit de la primera subida completa: `7cc1274e6bd02a8b10a27690e32c807eaade0d07`.
Commit de compatibilidad con publicación desde la raíz: `28fad5e39e884a8c64ee32e8858cdbd2fe1bfbce`.

GitHub Pages ya estaba habilitado con publicación desde `main` / raíz. Eso hizo que la primera publicación mostrara el README aunque el flujo de Actions publicaba correctamente `public/`. Se corrigió generando también las páginas y recursos en la raíz del repositorio. Ambas salidas se comparan byte a byte con `scripts/verify.py`.

Se conservó la configuración de Pages y se resolvió mediante el conector, sin controlar Chrome. La carpeta local quedó conectada a `origin` y su historial se integró con el remoto conservando ambos historiales.

Verificación online realizada:

- Inicio muestra el portfolio; sus tres imágenes visibles cargaron desde `analaurasidan.github.io`.
- Spotify muestra el reproductor Workland y sus controles. No se inició reproducción de audio durante la prueba.
- Projects, CashFly, Filmo acá, Busuu, InnFlow, About, Contact y 404 abren con contenido. No se observaron imágenes completadas con error ni imágenes apuntando a `framerusercontent.com` en las comprobaciones realizadas.
- La sesión online no registró errores ni advertencias durante esas pruebas.
- A 390 px el menú abre y permite navegar a Contact; no se observó desbordamiento horizontal y el correo apunta a `mailto:analaurasidan@gmail.com`.
- Los procesos de publicación de la primera subida terminaron correctamente. La Home real se verificó después del despliegue de la corrección de raíz.

Siguiente etapa: revisión de la web publicada y conexión del dominio comprado en Donweb. Todavía no se canceló Framer.

## Dominio y Framer

Proveedor declarado: Donweb. No se modificó DNS, no se agregó CNAME, no se cambió el sitio de producción y no se canceló el plan de Framer.

El respaldo original sigue separado y sin modificaciones por esta migración.
