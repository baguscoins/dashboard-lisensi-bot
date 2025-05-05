document.addEventListener("DOMContentLoaded", function () {
  const animElements = document.querySelectorAll(".fade-in, .fade-in-up");

  function checkVisible() {
    animElements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top <= window.innerHeight - 100) {
        el.classList.add("visible");
      }
    });
  }

  window.addEventListener("scroll", checkVisible);
  checkVisible();
});
