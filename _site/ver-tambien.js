(function () {
  // Mapa de subtemas equivalentes entre los 3 lenguajes
  const subtemas = [
    { nombre: "Introducción e instalación",
      python: "/python/01-introduccion.html", r: "/r/01-introduccion.html", julia: "/julia/01-introduccion.html" },
    { nombre: "Tipos de datos y variables",
      python: "/python/02-entrada-datos-operadores.html", r: "/r/02-tipos-y-variables.html", julia: "/julia/02-tipos-y-variables.html" },
    { nombre: "Estructuras de control / Funciones",
      python: "/python/03-funciones.html", r: "/r/03-estructuras-control.html", julia: "/julia/03-estructuras-control.html" },
    { nombre: "Estructuras de datos",
      python: "/python/04-estructuras-datos.html", r: "/r/04-estructuras-datos.html", julia: "/julia/04-estructuras-datos.html" },
    { nombre: "Funciones",
      python: "/python/05-arreglos.html", r: "/r/05-funciones.html", julia: "/julia/05-funciones.html" },
    { nombre: "Particularidades",
      python: "/python/06-funciones-estadisticas.html", r: "/r/06-particularidades.html", julia: "/julia/06-particularidades.html" },
    { nombre: "Ejercicios de ingeniería",
      python: "/python/07-ejercicios-ingenieria.html", r: "/r/07-ejercicios-ingenieria.html", julia: "/julia/07-ejercicios-ingenieria.html" },
    { nombre: "Visualización",
      python: "/python/08-visualizacion.html", r: "/r/08-visualizacion.html", julia: "/julia/08-visualizacion.html" },
  ];

  const nombresLenguaje = { python: "Python", r: "R", julia: "Julia" };

  function rutaActual() {
    return window.location.pathname;
  }

  document.addEventListener("DOMContentLoaded", function () {
    const path = rutaActual();
    let match = null, idiomaActual = null;

    for (const tema of subtemas) {
      for (const idioma of ["python", "r", "julia"]) {
        if (path.endsWith(tema[idioma])) {
          match = tema;
          idiomaActual = idioma;
          break;
        }
      }
      if (match) break;
    }

    if (!match) return;

    const otros = ["python", "r", "julia"].filter(l => l !== idiomaActual);

    const box = document.createElement("div");
    box.className = "callout callout-note";
    box.style.cssText = "border-left:4px solid #2C5F8A; border-radius:10px; padding:12px 18px; margin:1.5rem 0;";

    const title = document.createElement("p");
    title.style.cssText = "font-weight:600; margin:0 0 6px;";
    title.textContent = "Ver también — " + match.nombre + " en:";
    box.appendChild(title);

    const linksWrap = document.createElement("div");
    linksWrap.style.cssText = "display:flex; gap:14px;";
    otros.forEach(l => {
      const a = document.createElement("a");
      a.href = match[l];
      a.textContent = nombresLenguaje[l];
      linksWrap.appendChild(a);
    });
    box.appendChild(linksWrap);

    const main = document.querySelector("main.content") || document.querySelector("main");
    if (main) main.appendChild(box);
  });
})();
