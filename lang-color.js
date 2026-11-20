/* Marca con data-lang lo que pertenece a Julia (jl), Python (py) o R (r)
   para que styles.css lo pinte con el color de ese lenguaje. */
(function () {
  var MAPA = { julia: 'jl', python: 'py', r: 'r' };
  function clave(t) { return MAPA[(t || '').replace(/\s+/g, ' ').trim().toLowerCase()] || null; }

  function aplicar() {
    var m = /\/(julia|python|r)\//i.exec(location.pathname);
    if (m && document.body) document.body.setAttribute('data-lang', MAPA[m[1].toLowerCase()]);

    var selectores = [
      '.navbar-nav .nav-link',
      '.sidebar .menu-text',
      '.panel-tabset .nav-link',
      'main h2', 'main h3', 'main h4',
      'main th', 'main summary', 'main strong',
      'main a'
    ].join(',');
    document.querySelectorAll(selectores).forEach(function (el) {
      if (el.hasAttribute('data-lang')) return;
      var k = clave(el.textContent);
      if (k) el.setAttribute('data-lang', k);
    });
  }

  function iniciar() { aplicar(); setTimeout(aplicar, 800); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
