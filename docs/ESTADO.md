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

## Pendiente de GitHub

Cuenta autenticada por el conector: `analaurasidan`. La instalación permite repositorios seleccionados y actualmente el único repositorio accesible es `job-match`. El conector expone escritura sobre repositorios autorizados, pero no creación de repositorios. No está instalado el CLI `gh`.

Se intentó abrir `https://github.com/new` en el navegador de esta sesión; GitHub pidió iniciar sesión. No se creó ni se publicó un repositorio remoto.

Siguiente paso: crear el repositorio público `analaurasidan.github.io` (para usar Pages gratis y rutas desde la raíz) y seleccionarlo en la instalación existente del conector: https://github.com/settings/installations/176300908. Una vez autorizado se podrá subir el proyecto. Si la interfaz ofrece más permisos que ese repositorio específico, revisar esa ampliación antes de aceptarla.

## Dominio y Framer

Proveedor declarado: Donweb. No se modificó DNS, no se agregó CNAME, no se cambió el sitio de producción y no se canceló el plan de Framer.

El respaldo original sigue separado y sin modificaciones por esta migración.
