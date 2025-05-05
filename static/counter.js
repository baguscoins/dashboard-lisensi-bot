const counters = document.querySelectorAll(".count");
counters.forEach(counter => {
  const update = () => {
    const target = +counter.dataset.target;
    const current = +counter.innerText;
    const increment = Math.ceil(target / 100);
    if (current < target) {
      counter.innerText = current + increment;
      setTimeout(update, 40);
    } else {
      counter.innerText = target;
    }
  };
  update();
});
