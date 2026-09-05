(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const main = document.querySelector("main.content") || document.querySelector("main");
    const titleEl = document.querySelector(".title") || document.querySelector("h1");
    if (!main || !titleEl) return;

    const text = main.innerText || "";
    const words = text.trim().split(/\s+/).filter(Boolean).length;
    if (words < 40) return; // páginas muy cortas no necesitan esto

    const minutos = Math.max(1, Math.round(words / 200));

    const badge = document.createElement("p");
    badge.style.cssText = "font-size:13px;color:#6B7280;margin:-6px 0 1rem;";
    badge.textContent = "⏱ Tiempo de lectura estimado: " + minutos + " min";

    titleEl.insertAdjacentElement("afterend", badge);
  });
})();
