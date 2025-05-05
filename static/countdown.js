const end = new Date();
end.setMinutes(end.getMinutes() + 5); // 5 minutes from now
function updateTimer() {
  const now = new Date();
  const diff = end - now;
  const mins = Math.floor(diff / 60000);
  const secs = Math.floor((diff % 60000) / 1000);
  document.getElementById("timer").innerText = mins + "m " + secs + "s";
  if (diff > 0) setTimeout(updateTimer, 1000);
}
updateTimer();
