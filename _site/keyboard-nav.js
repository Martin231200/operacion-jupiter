(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const nav = document.querySelector(".page-navigation");
    if (!nav) return;

    const prevLink = nav.querySelector(".nav-page-previous a");
    const nextLink = nav.querySelector(".nav-page-next a");

    document.addEventListener("keydown", function (e) {
      // No interferir si la persona está escribiendo en un input, textarea, o editor de código
      const tag = (document.activeElement && document.activeElement.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA" || document.activeElement.isContentEditable) return;

      if (e.key === "ArrowRight" && nextLink) {
        window.location.href = nextLink.getAttribute("href");
      } else if (e.key === "ArrowLeft" && prevLink) {
        window.location.href = prevLink.getAttribute("href");
      }
    });
  });
})();
