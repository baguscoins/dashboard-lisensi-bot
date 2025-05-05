let idx = 0;
const slides = document.querySelectorAll(".slide");
function showSlide() {
  slides.forEach((slide, i) => {
    slide.style.transform = "translateX(" + ((i - idx) * 100) + "%)";
  });
}
setInterval(() => { idx = (idx + 1) % slides.length; showSlide(); }, 4000);
showSlide();
