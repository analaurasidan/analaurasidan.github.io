/* Framer emits links relative to routes without trailing slashes. Directory
 * hosting adds a slash; resolve using the original route semantics. */
const portfolioContextKey = 'analuna-portfolio-context';
function portfolioContext() {
  const path = location.pathname.replace(/^\/es(?=\/|$)/, '') || '/';
  const context = path.startsWith('/branding') ? 'branding'
    : path.startsWith('/ux-ui') || path.startsWith('/projects') ? 'ux'
    : path === '/' || path === '/index.html' ? 'home' : null;
  try {
    if (context) sessionStorage.setItem(portfolioContextKey, context);
    return context || sessionStorage.getItem(portfolioContextKey) || 'home';
  } catch { return context || 'home'; }
}
const currentPortfolio = portfolioContext();
function normalizeLinks() {
  const base = location.origin + (location.pathname.replace(/\/$/, '') || '/');
  for (const link of document.querySelectorAll('a[href]')) {
    const raw = link.getAttribute('href');
    if (/^(?:(?:Projects|Proyectos)\s*)+$/.test(link.textContent.trim())) {
      const prefix = /^\/es(?:\/|$)/.test(location.pathname) ? '/es' : '';
      const destination = currentPortfolio === 'ux' ? '/projects/'
        : currentPortfolio === 'branding' ? '/branding/#projects' : '/#portfolios';
      const target = prefix + destination;
      if (raw !== target) link.setAttribute('href', target);
      continue;
    }
    if (!/^\.{1,2}\//.test(raw)) continue;
    const url = new URL(raw, base);
    link.setAttribute('href', url.pathname + url.search + url.hash);
  }
  // Keep the external profile in the footer; the header leads into the work.
  for (const link of document.querySelectorAll('nav a[href*="linkedin.com"]')) {
    if (!link.closest('footer')) link.style.setProperty('display', 'none', 'important');
  }
}
normalizeLinks();
new MutationObserver(normalizeLinks).observe(document.documentElement, {childList:true, subtree:true, attributes:true, attributeFilter:['href']});

/* Preserve ordinary multi-page navigation on static hosting. */
document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target === '_blank' || link.hasAttribute('download')) return;
  const url = new URL(link.href, location.href);
  if (url.origin !== location.origin || (url.pathname === location.pathname && url.hash)) return;
  if (url.pathname.startsWith('/assets/')) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  location.assign(url.pathname + url.search + url.hash);
}, true);
