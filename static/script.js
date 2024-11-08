// code adapted from github copilot - dark and light mode functionality (I am not comfortable with JS, sorry!)

document.getElementById("theme").addEventListener("change", function () {
  if (this.checked) {
    document.body.classList.add("dark-mode");
    document.body.classList.remove("light-mode");
    document.querySelectorAll("a").forEach((link) => {
      link.classList.add("dark-mode");
      link.classList.remove("light-mode");
    });
  } else {
    document.body.classList.add("light-mode");
    document.body.classList.remove("dark-mode");
    document.querySelectorAll("a").forEach((link) => {
      link.classList.add("light-mode");
      link.classList.remove("dark-mode");
    });
  }
});
