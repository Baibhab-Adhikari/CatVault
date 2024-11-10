// code adapted from github copilot - dark and light mode functionality (I am not comfortable with JS, sorry!)

document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
  
    // Set the initial state of the toggle based on the body class
    if (document.body.classList.contains("dark-mode")) {
      themeToggle.checked = true;
    } else {
      themeToggle.checked = false;
    }
  
    themeToggle.addEventListener("change", function () {
      if (this.checked) {
        document.body.classList.add("dark-mode");
        document.body.classList.remove("light-mode");
        document.querySelectorAll("a").forEach((link) => {
          link.classList.add("dark-mode");
          link.classList.remove("light-mode");
        });
        document.querySelectorAll(".dropdown-menu").forEach((burger) => {
          burger.classList.add("dark-mode");
          burger.classList.remove("light-mode");
        });
      } else {
        document.body.classList.add("light-mode");
        document.body.classList.remove("dark-mode");
        document.querySelectorAll("a").forEach((link) => {
          link.classList.add("light-mode");
          link.classList.remove("dark-mode");
        });
        document.querySelectorAll(".dropdown-menu").forEach((burger) => {
          burger.classList.add("light-mode");
          burger.classList.remove("dark-mode");
        });
      }
    });
  });