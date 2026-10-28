"""Localize the owner's published site; keep the public design and routes intact.

Run once with --download to retrieve missing literal dynamic module imports.
Subsequent builds use source/ and require no network or package installation.
"""
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import urllib.parse as up
import urllib.request as ur

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
PUBLIC = ROOT / 'public'
BACKUP = ROOT.parent / 'Respaldo-Portfolio-2026-10-28'
REMOTE = 'https://analaurasidan.com.ar'
SITE_CDN = 'https://framerusercontent.com/sites/2vHWIhUI2nrrwWs6Ll1aJu/'
parser = argparse.ArgumentParser()
parser.add_argument('--download', action='store_true')
parser.add_argument('--verify-local', action='store_true', help='Temporarily block external resources except the Spotify iframe')
args = parser.parse_args()
manifest_file = SOURCE / 'manifest.json'
if not manifest_file.exists():
    shutil.copytree(BACKUP / 'site', SOURCE / 'pages', dirs_exist_ok=True)
    shutil.copytree(BACKUP / 'assets', SOURCE / 'assets', dirs_exist_ok=True)
    shutil.copyfile(BACKUP / 'metadata/manifest.json', manifest_file)
    shutil.copyfile(BACKUP / 'metadata/sitemap.xml', SOURCE / 'sitemap.xml')
    shutil.copyfile(BACKUP / 'metadata/robots.txt', SOURCE / 'robots.txt')
records = {r['url']: r for r in json.loads(manifest_file.read_text()) if 'file' in r}

def source_path(record):
    path = record['file']
    if path.startswith('site/'):
        return SOURCE / 'pages' / path[5:]
    return SOURCE / path

def module_imports(text, base):
    # Match literal ESM imports, including Framer's backtick dynamic imports.
    return {up.urljoin(base, m) for m in re.findall(r'(?:from\s*|import\s*\(\s*|import\s*)["\x27`]([^"\x27`\s]+\.m?js)["\x27`]', text) if up.urljoin(base, m).startswith(SITE_CDN)}

def retrieve(url):
    with ur.urlopen(url, timeout=40) as r:
        data = r.read()
        filename = 'assets/' + hashlib.sha256(url.encode()).hexdigest()[:16] + '-' + up.urlsplit(url).path.rsplit('/', 1)[-1]
        (SOURCE / filename).write_bytes(data)
        return {'url': url, 'file': filename, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'content_type': r.headers.get('Content-Type', '')}

while True:
    imports = set()
    for url, record in records.items():
        if url.startswith(SITE_CDN) and up.urlsplit(url).path.endswith(('.mjs', '.js')):
            imports |= module_imports(source_path(record).read_text(), url)
    missing = sorted(imports - records.keys())
    if not missing:
        break
    if not args.download:
        raise SystemExit('Missing modules; run with --download: ' + repr(missing))
    with ThreadPoolExecutor(max_workers=6) as pool:
        for record in pool.map(retrieve, missing):
            records[record['url']] = record
            print('Downloaded module:', record['url'], flush=True)
    manifest_file.write_text(json.dumps(list(records.values()), indent=2, ensure_ascii=False))

# Published Framer CMS uses two binary files with byte offsets. Preserve the
# binary bytes and adapt the client range reader for ordinary static hosting.
cms_urls = set()
for url, record in list(records.items()):
    if url.startswith(SITE_CDN) and record['file'].endswith('.mjs'):
        text = source_path(record).read_text()
        for relative, base in re.findall(r'new URL\(`([^`]+\.framercms)`,`(https://[^`]+)`\)', text):
            cms_urls.add(up.urljoin(base, relative).replace('/modules/', '/cms/'))
missing_cms = sorted(cms_urls - records.keys())
if missing_cms and not args.download:
    raise SystemExit('Missing CMS binaries; run with --download: ' + repr(missing_cms))
with ThreadPoolExecutor(max_workers=4) as pool:
    for record in pool.map(retrieve, missing_cms):
        records[record['url']] = record
        print('Downloaded published CMS:', record['url'], flush=True)
manifest_file.write_text(json.dumps(list(records.values()), indent=2, ensure_ascii=False))

def target_url(url):
    p = up.urlsplit(url)
    path = p.path
    if p.query:
        stem, ext = path.rsplit('.', 1)
        path = stem + '--' + hashlib.sha256(p.query.encode()).hexdigest()[:12] + '.' + ext
    return '/assets/' + p.netloc + path

mapping = {u: target_url(u) for u,r in records.items() if r['file'].startswith('assets/') and u != 'https://framer.com/edit/init.mjs'}
replacements = []
for old, new in mapping.items():
    replacements.append((old, new))
    escaped = html.escape(old, quote=True)
    if escaped != old:
        replacements.append((escaped, new))
replacements.sort(key=lambda item: -len(item[0]))
pattern = re.compile('|'.join(re.escape(old) for old, _ in replacements))
lookup = dict(replacements)

def localize(text):
    text = pattern.sub(lambda m: lookup[m.group()], text)
    text = text.replace(SITE_CDN, '/assets/framerusercontent.com/sites/2vHWIhUI2nrrwWs6Ll1aJu/')
    text = text.replace('https://sociable-points-289834.framer.app/', '/')
    text = text.replace('mailto: analaurasidan@gmail.com', 'mailto:analaurasidan@gmail.com')
    text = text.replace('Ana Lauras Sidan/contact', 'Ana Laura Sidan — Contact').replace('Sidan Porfolio', 'Sidan Portfolio')
    # Keep runtime navigation on the independent site; production canonical meta
    # remains the owner's domain. The DNS has not changed during preparation.
    text = text.replace('siteCanonicalURL:`https://analaurasidan.com.ar`', 'siteCanonicalURL:location.origin')
    text = text.replace('href:`https://analaurasidan.com.ar/', 'href:`/')
    text = re.sub(r'new URL\(`([^`]+)`,`(/assets/[^`]+)`\)', r'new URL(`\1`,new URL(`\2`,location.origin).href)', text)
    text = re.sub(r'//# sourceMappingURL=.*', '', text)
    return text

PUBLIC.mkdir(exist_ok=True)
for url, record in records.items():
    if not record['file'].startswith('assets/') or url not in mapping:
        continue
    dest = PUBLIC / mapping[url].lstrip('/')
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = source_path(record).read_bytes()
    if dest.suffix in ('.js', '.mjs', '.css', '.json', '.svg'):
        text = localize(data.decode('utf-8'))
        if 'script_main.' in dest.name:
            # On-page editing is a Framer-hosted service, unnecessary on the copy.
            text, count = re.subn(r'EditorBar:l===void 0\?void 0:.*?,adaptLayoutToTextDirection:', 'EditorBar:void 0,adaptLayoutToTextDirection:', text)
            assert count == 1, 'Editor service patch no longer matches source'
        if 'qcOEbDaZ_.CW7_7ww_' in dest.name:
            text = text.replace('a.searchParams.set(`range`,o);', 'a.searchParams.delete(`range`);')
            old = 'let c=await s.arrayBuffer(),l=new Uint8Array(c);'
            new = 'let c=await s.arrayBuffer(),full=new Uint8Array(c),l=new Uint8Array(i),cursor=0;for(const part of n){l.set(full.subarray(part.from,part.to),cursor);cursor+=part.to-part.from;}'
            assert old in text, 'CMS range adapter no longer matches source'
            text = text.replace(old, new)
            text = text.replace('return this.decoder.decode(t)', 'return globalThis.__portfolioLocalize(this.decoder.decode(t))')
        data = text.encode('utf-8')
    dest.write_bytes(data)

for src in sorted((SOURCE / 'pages').rglob('*.html')):
    rel = src.relative_to(SOURCE / 'pages')
    dest = PUBLIC / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text()
    text = re.sub(r'<script\b[^>]*src=["\x27]https://events\.framer\.com/[^>]*>.*?</script>', '', text, flags=re.S)
    text = re.sub(r'<link\b[^>]*rel="preconnect"[^>]*>', '', text)
    text = localize(text)
    # Root-relative routes avoid /projects/ -> /projects/projects after static
    # hosting normalizes a directory URL with a trailing slash.
    route = '/' + rel.parent.as_posix().replace('.', '').strip('/')
    def relative_link(match):
        url = up.urlsplit(up.urljoin(REMOTE + route, html.unescape(match.group(1))))
        return 'href="' + html.escape(up.urlunsplit(('', '', url.path, url.query, url.fragment)), quote=True) + '"'
    text = re.sub(r'href="((?:\.{1,2}/)[^"]*)"', relative_link, text)
    text = text.replace('href="https://analaurasidan.com.ar/"', 'href="/"')
    text = text.replace('mailto:%20analaurasidan@gmail.com', 'mailto:analaurasidan@gmail.com')
    if rel.as_posix() == 'contact/index.html':
        text = text.replace('Ana Lauras Sidan/contact', 'Ana Laura Sidan — Contact').replace('Porfolio', 'Portfolio')
    text = text.replace('</head>', '<link rel="stylesheet" href="/migration.css"><script src="/runtime-url-map.js"></script></head>')
    if args.verify_local:
        policy = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; media-src 'self' blob:; connect-src 'self'; frame-src https://open.spotify.com; worker-src 'self' blob:"
        text = text.replace('<head>', '<head><meta http-equiv="Content-Security-Policy" content="' + policy + '">', 1)
    text = text.replace('</body>', '<script src="/navigation.js" defer></script></body>')
    dest.write_text(text)

# GitHub Pages requires a top-level 404 document; keep the original /404 route.
shutil.copyfile(PUBLIC / '404/index.html', PUBLIC / '404.html')
for name in ['sitemap.xml', 'robots.txt']:
    shutil.copyfile(SOURCE / name, PUBLIC / name)
(PUBLIC / '.nojekyll').touch()
urlmap = json.dumps(mapping, ensure_ascii=False)
(PUBLIC / 'runtime-url-map.js').write_text('/* Localize URLs decoded from the published CMS binary without changing its byte offsets. */\n(()=>{const map='+urlmap+';const keys=Object.keys(map).sort((a,b)=>b.length-a.length);globalThis.__portfolioLocalize=text=>{for(const key of keys)text=text.split(key).join(map[key]);return text;};})();\n')
for name in ['navigation.js', 'migration.css']:
    shutil.copyfile(ROOT / name, PUBLIC / name)
(ROOT / 'docs/localization.json').write_text(json.dumps({'source_pages': len(list((SOURCE/'pages').rglob('*.html'))), 'localized_assets': len(mapping), 'literal_module_imports_missing': [], 'assets': mapping}, indent=2))
# Support GitHub Pages' existing "Deploy from branch / main / root" setting
# as well as the Actions artifact. Both paths must publish the same website.
shutil.copytree(PUBLIC, ROOT, dirs_exist_ok=True)
print('Build ready:', PUBLIC, 'assets:', len(mapping), flush=True)
