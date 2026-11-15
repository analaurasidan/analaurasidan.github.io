"""Build Spanish page counterparts and shared language UI without duplicating assets."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def normalize(text):
    return ' '.join(html.unescape(text).split())

def build_languages(public):
    translations = json.loads((ROOT / 'source/translations-es.json').read_text())
    # A shared dictionary also translates text inserted by the original UX runtime.
    (public / 'translations-es.js').write_text('window.portfolioSpanish=' + json.dumps(translations, ensure_ascii=False) + ';')
    pages = list((ROOT / 'source/pages').rglob('*.html'))
    for source in pages:
        rel = source.relative_to(ROOT / 'source/pages')
        page = public / rel
        english = page.read_text()
        route = '/' + str(rel.parent).replace('.', '').strip('/')
        route = route.rstrip('/') + '/'
        spanish_route = '/es' + route
        alternates = ('<link rel="alternate" hreflang="en" href="https://analaurasidan.com.ar' + route + '">'
            '<link rel="alternate" hreflang="es-AR" href="https://analaurasidan.com.ar' + spanish_route + '">'
            '<link rel="alternate" hreflang="x-default" href="https://analaurasidan.com.ar' + route + '">')
        shared = '<link rel="stylesheet" href="/language.css?v=2"><script src="/translations-es.js"></script><script src="/language.js?v=1" defer></script>'
        english = english.replace('</head>', alternates + shared + '</head>')
        page.write_text(english)
        spanish = english.replace('<html lang="en"', '<html lang="es-AR"')
        titles = {'/': 'Analuna — Diseño UX/UI, producto y branding', '/about/': 'Sobre mí — Analuna', '/contact/': 'Contacto — Analuna', '/ux-ui/': 'Diseño UX/UI y de producto — Analuna', '/projects/': 'Proyectos UX/UI — Analuna'}
        if route in titles:
            spanish = re.sub(r'<title>.*?</title>', '<title>' + titles[route] + '</title>', spanish, flags=re.S)
        def metadata(match):
            opening, content = match[1], html.unescape(match[2])
            translated = translations.get(normalize(content), content)
            if 'og:url' in opening and content.startswith('https://analaurasidan.com.ar/'):
                translated = 'https://analaurasidan.com.ar' + spanish_route
            if ('description' in opening or 'og:title' in opening or 'twitter:title' in opening) and translated == content:
                translated = titles.get(route, 'Portfolio de diseño de Analuna')
            return opening + html.escape(translated, quote=True) + '"'
        spanish = re.sub(r'(<meta\b[^>]*content=")([^"]*)"', metadata, spanish)

        spanish = re.sub(r'(<link rel="canonical" href=")[^"]+', r'\g<1>https://analaurasidan.com.ar' + spanish_route, spanish)
        # Translate complete headings/paragraphs before individual text nodes so
        # animated, letter-by-letter headings have a readable Spanish SSR version.
        def block(match):
            key = normalize(re.sub('<[^>]+>', '', match[2]))
            return match[1] + html.escape(translations[key]) + match[3] if key in translations else match[0]
        spanish = re.sub(r'(<(?:h[1-6]|p)\b[^>]*>)(.*?)(</(?:h[1-6]|p)>)', block, spanish, flags=re.S)
        def text_node(match):
            text = match[0]
            key = normalize(text)
            if key not in translations:
                return text
            return re.sub(r'\S.*\S|\S', lambda _: html.escape(translations[key]), text, count=1, flags=re.S)
        # Exclude JS and CSS from textual replacement.
        segments = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', spanish, flags=re.S)
        for i in range(0, len(segments), 2):
            segments[i] = re.sub(r'(?<=>)[^<]+(?=<)', text_node, segments[i])
        spanish = ''.join(segments)
        def accessible(match):
            return match[1] + html.escape(translations.get(normalize(match[2]), html.unescape(match[2])), quote=True) + '"'
        spanish = re.sub(r'((?:alt|aria-label)=")([^"]*)"', accessible, spanish)

        def link(match):
            href = html.unescape(match[1])
            if href.startswith('/') and not href.startswith('//') and not href.startswith(('/assets/', '/landing/', '/es/')):
                href = '/es' + href
            return 'href="' + html.escape(href, quote=True) + '"'
        spanish = re.sub(r'href="([^"]*)"', link, spanish)
        # Shared styles/scripts live at the root rather than under /es/.
        spanish = spanish.replace('href="/es/migration.css', 'href="/migration.css').replace('href="/es/language.css', 'href="/language.css')
        target = public / 'es' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(spanish)
    sitemap = public / 'sitemap.xml'
    xml = sitemap.read_text()
    additions = ''.join('<url><loc>https://analaurasidan.com.ar/es' + ('/' + str(source.relative_to(ROOT / 'source/pages').parent).replace('.', '').strip('/')).rstrip('/') + '/</loc></url>' for source in pages if source.relative_to(ROOT / 'source/pages').parts[0] != '404')
    sitemap.write_text(xml.replace('</urlset>', additions + '</urlset>'))
    for asset in ['language.js', 'language.css']:
        (public / asset).write_text((ROOT / 'source/landing/assets' / asset).read_text())
