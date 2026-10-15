(function () {
  // Guarda la última página de tutorial que se visitó, para «Continuar donde lo dejaste».
  document.addEventListener("DOMContentLoaded", function () {
    var ruta = window.location.pathname;
    var m = ruta.match(/\/(python|r|julia|tutoriales)\//);
    if (!m) return;
    var h1 = document.querySelector("h1.title");
    var titulo = (h1 ? h1.textContent : document.title).trim();
    try {
      localStorage.setItem("operacion-jupiter-ultima", JSON.stringify({
        href: ruta,
        titulo: titulo,
        seccion: m[1]
      }));
    } catch (e) { /* localStorage no disponible: no pasa nada */ }
  });
})();
