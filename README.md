# Portfolio de Ana Laura Sidan

Proyecto de migración de `analaurasidan.com.ar` desde Framer a alojamiento estático.

## Ubicación y alcance

Este proyecto está en `/Users/analaura/Documents/Portfolio-Web`.
El respaldo original se conserva separado en `/Users/analaura/Documents/Respaldo-Portfolio-2026-10-28`.

Incluye Inicio (con Spotify), About, Contact, Projects, los casos CashFly, Filmo acá, Busuu e InnFlow y la página 404. Conserva el diseño y las rutas publicadas.

## Vista previa

Desde esta carpeta:

```sh
python3 scripts/build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory public
```

Abrir `http://127.0.0.1:8765/`. No abrir los HTML con doble clic: los módulos requieren HTTP.

El build normal no usa internet ni instala paquetes. `--download` solo se utilizó para completar los módulos y datos públicos de la captura inicial.

## Estructura

- `source/pages/`: HTML original por ruta.
- `source/assets/`: recursos originales y contenido CMS publicado.
- `source/manifest.json`: origen y huellas SHA-256.
- `scripts/build.py`: genera la versión con recursos locales y adapta el acceso al CMS para un servidor estático.
- `public/`: sitio que se debe publicar.
- `navigation.js`: conserva la navegación entre páginas y corrige rutas relativas en servidores que agregan `/` al final.
- `migration.css`: estilos adicionales de foco y movimiento reducido.
- `docs/`: informes de migración y verificación.

## Qué cambió

Se trasladaron imágenes, fuentes, módulos y archivos públicos de CMS al propio sitio. Se retiraron la analítica y la barra de edición de Framer. Se corrigieron el destino del logo, los enlaces internos, el espacio del enlace de correo y las erratas del título/pie de Contact.

La música se sigue reproduciendo desde Spotify. Los enlaces a Behance, redes y WhatsApp siguen siendo externos.

Esta primera versión conserva el código generado por Framer (React y sus módulos empaquetados), servido localmente. No ofrece el editor visual de Framer. Para editar contenido hay que modificar las fuentes correspondientes y regenerar el sitio; los proyectos también tienen datos binarios de CMS, por lo que no alcanza con editar solo el HTML. Una futura reorganización en componentes legibles facilitaría actualizaciones frecuentes.

## Publicación en GitHub Pages

Repositorio sugerido: `analaurasidan.github.io`, bajo la cuenta `analaurasidan`. Ese nombre permite servir desde la raíz sin cambiar todas las rutas.

El flujo de `.github/workflows/pages.yml` publica únicamente `public/`. En GitHub hay que configurar Settings → Pages → Source: GitHub Actions. Crear el repositorio y autorizarlo en el conector sigue pendiente.

El dominio está comprado en Donweb. Todavía no se cambió ningún registro DNS ni se canceló Framer. Primero revisar la URL de prueba y después conectar el dominio y verificar HTTPS. La configuración `CNAME` se agrega al realizar ese cambio, para que la prueba no redirija antes de tiempo al sitio actual.

Antes de cancelar Framer, verificar la versión publicada y todos los proyectos. Las pruebas locales no reemplazan esa comprobación.
