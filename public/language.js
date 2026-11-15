(() => {
  const spanish = /^\/es(?:\/|$)/.test(location.pathname);
  const dictionary = window.portfolioSpanish || {};
  const normalize = text => text.replace(/\s+/g, ' ').trim();
  const basePath = location.pathname.replace(/^\/es(?=\/|$)/, '') || '/';
  const globe = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/></svg>';
  function picker() {
    const control = document.createElement('details');
    control.className = 'language-picker';
    control.addEventListener('click', event => event.stopPropagation());
    control.innerHTML = '<summary aria-label="Language">' + globe + '<span>Language</span><svg class="language-chevron" viewBox="0 0 12 12" aria-hidden="true"><path d="m3 4.5 3 3 3-3"/></svg></summary><div class="language-options"><a lang="en" data-language="en">English<span aria-hidden="true"></span></a><a lang="es-AR" data-language="es">Español<span aria-hidden="true"></span></a></div>';
    for (const a of control.querySelectorAll('a')) {
      const selected = (a.dataset.language === 'es') === spanish;
      a.href = (a.dataset.language === 'es' ? '/es' : '') + basePath + location.search + location.hash;
      if (selected) { a.setAttribute('aria-current', 'true'); a.lastElementChild.textContent = '✓'; }
    }
    return control;
  }
  function update() {
    if (spanish) {
      document.documentElement.lang = 'es-AR';
      // The original UX components can insert English after hydration.
      for (const el of document.querySelectorAll('h1,h2,h3,h4,p')) {
        if (el.closest('.language-picker')) continue;
        const value = dictionary[normalize(el.textContent)];
        if (value && el.textContent !== value) el.textContent = value;
      }
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      for (const node of nodes) {
        if (node.parentElement.closest('script,style,.language-picker')) continue;
        const value = dictionary[normalize(node.textContent)];
        if (value && normalize(node.textContent) !== value) node.textContent = value;
      }
      for (const el of document.querySelectorAll('[alt],[aria-label]')) {
        for (const attr of ['alt','aria-label']) {
          const key = el.getAttribute(attr);
          if (key && dictionary[normalize(key)] && dictionary[normalize(key)] !== key) el.setAttribute(attr, dictionary[normalize(key)]);
        }
      }
      for (const a of document.querySelectorAll('a[href]')) {
        const raw = a.getAttribute('href');
        if (a.closest('.language-picker') || !raw.startsWith('/') || raw.startsWith('//') || raw.startsWith('/es/') || raw.startsWith('/assets/') || raw.startsWith('/landing/')) continue;
        a.setAttribute('href', '/es' + raw);
      }
    }
    for (const nav of document.querySelectorAll('header.nav, nav[aria-label="Main navigation"]')) {
      if (nav.matches('nav')) nav.parentElement.classList.add('portfolio-nav-shell');
      if (!nav.querySelector('.language-picker')) nav.append(picker());
      if (!nav.querySelector('.portfolio-mobile-menu')) {
        const mobile = document.createElement('details');
        mobile.className = 'portfolio-mobile-menu';
        mobile.addEventListener('click', event => event.stopPropagation());
        mobile.innerHTML = '<summary aria-label="' + (spanish ? 'Abrir menú' : 'Open menu') + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></summary><div class="portfolio-mobile-menu__panel"></div>';
        const panel = mobile.lastElementChild;
        const originals = nav.querySelectorAll('.nav__links a');
        if (originals.length) for (const a of originals) panel.append(a.cloneNode(true));
        else {
          const prefix = spanish ? '/es' : '';
          const projects = basePath.startsWith('/branding') ? '/branding/#projects' : basePath.startsWith('/ux-ui') || basePath.startsWith('/projects') ? '/projects/' : '/#portfolios';
          for (const [path,label] of [[projects,spanish?'Proyectos':'Projects'],['/about/',spanish?'Sobre mí':'About'],['/contact/',spanish?'Contacto':'Contact']]) {
            const a = document.createElement('a'); a.href = prefix + path; a.textContent = label; panel.append(a);
          }
        }
        panel.append(picker()); nav.append(mobile);
      }
    }
  }
  let scheduled = false;
  const observer = new MutationObserver(() => {
    if (scheduled) return;
    scheduled = true;
    queueMicrotask(() => { observer.disconnect(); update(); scheduled = false; observer.observe(document.body, {childList:true,subtree:true,characterData:true}); });
  });
  update(); observer.observe(document.body, {childList:true,subtree:true,characterData:true});
  window.addEventListener('hashchange', () => {
    for (const a of document.querySelectorAll('[data-language]')) a.href = (a.dataset.language === 'es' ? '/es' : '') + basePath + location.search + location.hash;
  });
  document.addEventListener('click', event => {
    for (const el of document.querySelectorAll('.language-picker[open]')) if (!el.contains(event.target)) el.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') for (const el of document.querySelectorAll('.language-picker[open]')) { el.open = false; el.querySelector('summary').focus(); }
  });
})();
