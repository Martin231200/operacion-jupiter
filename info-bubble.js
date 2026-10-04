(function () {
  document.addEventListener("click", function (e) {
    const term = e.target.closest(".info-term");
    if (!term) return;

    const next = term.nextElementSibling;
    if (next && next.classList.contains("info-bubble")) {
      next.remove();
      return;
    }

    document.querySelectorAll(".info-bubble").forEach(function (b) { b.remove(); });

    const bubble = document.createElement("div");
    bubble.className = "info-bubble";
    bubble.textContent = term.getAttribute("data-info");
    term.insertAdjacentElement("afterend", bubble);
  });
})();
