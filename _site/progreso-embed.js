(function () {
  const STORAGE_KEY = "operacion-jupiter-progreso";
  const mapa = {
    "/python/01-introduccion.html": "py-01",
    "/python/02-entrada-datos-operadores.html": "py-02",
    "/python/03-funciones.html": "py-03",
    "/python/04-estructuras-datos.html": "py-04",
    "/python/05-arreglos.html": "py-05",
    "/python/06-funciones-estadisticas.html": "py-06",
    "/r/01-introduccion.html": "r-01",
    "/r/02-tipos-y-variables.html": "r-02",
    "/r/03-estructuras-control.html": "r-03",
    "/r/04-estructuras-datos.html": "r-04",
    "/r/05-funciones.html": "r-05",
    "/r/06-particularidades.html": "r-06",
    "/julia/01-introduccion.html": "jl-01",
    "/julia/02-tipos-y-variables.html": "jl-02",
    "/julia/03-estructuras-control.html": "jl-03",
    "/julia/04-estructuras-datos.html": "jl-04",
    "/julia/05-funciones.html": "jl-05",
    "/julia/06-particularidades.html": "jl-06",
    "/tutoriales/quiz-comparativo.html": "tut-quiz",
    "/tutoriales/ejercicios-python.html": "tut-py",
    "/tutoriales/ejercicios-r.html": "tut-r",
    "/tutoriales/ejercicios-julia.html": "tut-jl",
  };

  function rutaActual() {
    let p = window.location.pathname;
    // normaliza por si el sitio vive bajo /operacion-jupiter/
    const idx = p.indexOf("/", 1);
    for (const key of Object.keys(mapa)) {
      if (p.endsWith(key)) return key;
    }
    return null;
  }

  const key = rutaActual();
  if (!key) return;
  const id = mapa[key];

  function cargarEstado() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function guardarEstado(estado) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(estado));
  }

  document.addEventListener("DOMContentLoaded", function () {
    const titleEl = document.querySelector(".title") || document.querySelector("h1");
    if (!titleEl) return;

    const estado = cargarEstado();

    const wrap = document.createElement("label");
    wrap.style.cssText = "display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;background:#F0F4F8;padding:6px 12px;border-radius:8px;cursor:pointer;margin:8px 0 1rem;";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = !!estado[id];
    cb.style.cssText = "width:18px;height:18px;cursor:pointer;";
    cb.onchange = function () {
      const e = cargarEstado();
      e[id] = cb.checked;
      guardarEstado(e);
    };

    const span = document.createElement("span");
    span.textContent = "Marcar esta sección como completada";

    wrap.appendChild(cb);
    wrap.appendChild(span);
    titleEl.insertAdjacentElement("afterend", wrap);
  });
})();
