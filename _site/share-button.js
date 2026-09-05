(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const titleEl = document.querySelector(".title") || document.querySelector("h1");
    if (!titleEl) return;

    const btn = document.createElement("button");
    btn.textContent = "🔗 Compartir esta página";
    btn.style.cssText = "font-size:13px;padding:6px 12px;border-radius:8px;border:1px solid #D6DCE2;background:#F0F4F8;cursor:pointer;margin:4px 0 1rem;";

    btn.onclick = function () {
      const url = window.location.href;
      if (navigator.share) {
        navigator.share({ title: document.title, url: url }).catch(() => {});
      } else {
        navigator.clipboard.writeText(url).then(function () {
          const original = btn.textContent;
          btn.textContent = "✓ Link copiado";
          setTimeout(function () { btn.textContent = original; }, 2000);
        });
      }
    };

    titleEl.insertAdjacentElement("afterend", btn);
  });
})();
