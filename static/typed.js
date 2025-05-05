const words = ["Jual Bot Crypto", "Kelola Lisensi", "Dapatkan Penghasilan"];
let i = 0, j = 0, current = '', isDeleting = false;
function type() {
  const display = document.getElementById("typed-text");
  if (i < words.length) {
    current = words[i];
    if (!isDeleting) {
      display.innerHTML = current.substring(0, j++);
      if (j > current.length + 10) isDeleting = true;
    } else {
      display.innerHTML = current.substring(0, j--);
      if (j === 0) {
        isDeleting = false;
        i = (i + 1) % words.length;
      }
    }
    setTimeout(type, isDeleting ? 50 : 100);
  }
}
document.addEventListener("DOMContentLoaded", type);
