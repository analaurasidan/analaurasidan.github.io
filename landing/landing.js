/* Falso 3D de la landing: el escenario se inclina hacia el mouse y las capas
   (fondo, retrato, chips) se desplazan a distinta velocidad.
   Se desactiva con prefers-reduced-motion y en pantallas táctiles. */
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = window.matchMedia('(pointer: coarse)').matches;
  const scene = document.querySelector('.scene');
  const stage = scene && scene.querySelector('.stage');
  if (!scene || !stage || reduce || coarse) return;

  const MAX_TILT_X = 3;   // grados de giro horizontal (rotateY)
  const MAX_TILT_Y = 2.2;   // grados de giro vertical (rotateX)
  let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0, live = false;

  const render = () => {
    cx += (tx - cx) * 0.085;
    cy += (ty - cy) * 0.085;
    // Variables que consumen las capas en CSS
    stage.style.setProperty('--px', cx.toFixed(4));
    stage.style.setProperty('--py', cy.toFixed(4));
    stage.style.setProperty('--rx', (cx * MAX_TILT_X).toFixed(3) + 'deg');
    stage.style.setProperty('--ry', (-cy * MAX_TILT_Y).toFixed(3) + 'deg');
    if (Math.abs(tx - cx) > 0.0015 || Math.abs(ty - cy) > 0.0015) raf = requestAnimationFrame(render);
    else { raf = 0; if (!live) stage.classList.remove('is-live'); }
  };

  const onMove = (e) => {
    const r = scene.getBoundingClientRect();
    tx = Math.max(-1, Math.min(1, ((e.clientX - r.left) / r.width - 0.5) * 2));
    ty = Math.max(-1, Math.min(1, ((e.clientY - r.top) / r.height - 0.5) * 2));
    live = true; stage.classList.add('is-live');
    if (!raf) raf = requestAnimationFrame(render);
  };
  const onLeave = () => { tx = 0; ty = 0; live = false; if (!raf) raf = requestAnimationFrame(render); };

  // Escuchamos en toda la ventana para que la escena reaccione aunque el mouse esté sobre el título
  window.addEventListener('pointermove', onMove, { passive: true });
  document.addEventListener('pointerleave', onLeave);
  window.addEventListener('blur', onLeave);
})();
