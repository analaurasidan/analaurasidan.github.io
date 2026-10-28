"""Check actual migration risks: module graph, route links, local resources."""
from html.parser import HTMLParser
import html
import json
from pathlib import Path
import re
import urllib.parse as up

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
errors = []
resources = set()
links = set()

class Refs(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and a.get('href'):
            links.add(a['href'])
        if tag != 'a':
            for key in ['src', 'href', 'poster']:
                if a.get(key):
                    resources.add(a[key])
        if a.get('srcset'):
            resources.update(v.strip().split()[0] for v in a['srcset'].split(',') if v.strip())

pages = sorted(PUBLIC.rglob('*.html'))
for page in pages:
    text = page.read_text()
    Refs().feed(text)
    resources.update(re.findall(r'url\(["\x27]?([^\s)"\x27]+)', text))
    if 'https://events.framer.com/script' in text:
        errors.append('Analytics script still present: ' + str(page))

for url in resources:
    url = html.unescape(url)
    if url.startswith('/assets/') and not (PUBLIC / up.urlsplit(url).path.lstrip('/')).is_file():
        errors.append('Missing asset: ' + url)

for link in links:
    if link.startswith('/') and not link.startswith('//'):
        path = PUBLIC / up.urlsplit(link).path.lstrip('/')
        if not path.is_file() and not (path / 'index.html').is_file():
            errors.append('Missing route: ' + link)

modules = list(PUBLIC.rglob('*.mjs'))
for module in modules:
    text = module.read_text()
    for spec in re.findall(r'(?:from\s*|import\s*\(\s*|import\s*)["\x27`]([^"\x27`\s]+\.m?js)["\x27`]', text):
        if spec.startswith('./') and not (module.parent / spec).is_file():
            errors.append('Missing module: ' + str(module) + ' -> ' + spec)
    if 'script_main.' in module.name and 'import(`https://framer.com/edit/init.mjs`)' in text:
        errors.append('Editor service still present')

report = {'html_documents':len(pages), 'modules':len(modules), 'local_resource_references_checked':len(resources), 'route_links_checked':len(links), 'errors':sorted(set(errors))}
(ROOT / 'docs/static-checks.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))
