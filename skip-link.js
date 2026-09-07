(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const main = document.querySelector("main.content") || document.querySelector("main");
    if (!main) return;
    if (!main.id) main.id = "contenido-principal";

    const link = document.createElement("a");
    link.href = "#" + main.id;
    link.className = "skip-to-content";
    link.textContent = "Saltar al contenido";
    document.body.insertBefore(link, document.body.firstChild);
  });
})();
