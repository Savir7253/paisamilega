const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");
if (menuToggle && navMenu) {
  menuToggle.addEventListener("click", () => navMenu.classList.toggle("open"));
}
document.querySelectorAll("a[href]").forEach(a => {
  a.addEventListener("click", () => {
    if (navMenu) navMenu.classList.remove("open");
  });
});
