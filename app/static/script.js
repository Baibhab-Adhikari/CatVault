// code adapted from github copilot - dark and light mode functionality (I am not comfortable with JS, sorry!)

document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("theme-toggle");

  // Load the user's theme preference from localStorage
  const userTheme = localStorage.getItem("theme");

  if (userTheme === "dark") {
    document.body.classList.add("dark-mode");
    document.body.classList.remove("light-mode");
    themeToggle.checked = true;
  } else if (userTheme === "light") {
    document.body.classList.add("light-mode");
    document.body.classList.remove("dark-mode");
    themeToggle.checked = false;
  } else {
    // Default to dark mode if no preference is set
    document.body.classList.add("dark-mode");
    themeToggle.checked = true;
  }

  themeToggle.addEventListener("change", function () {
    if (this.checked) {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
      localStorage.setItem("theme", "dark");
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
      localStorage.setItem("theme", "light");
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
  // Hide flash messages after 2.5 seconds
  const flashMessages = document.getElementById("flash-messages");
  if (flashMessages) {
    setTimeout(() => {
      flashMessages.style.display = "none";
    }, 2500);
  }
});

// js code for the range slider

function rangeSlider(value) {
  document.getElementById("range-val").innerHTML = value;
}

// JS code using fetch api to dynamically update the output box in generate passwords page (adapted from copilot)

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("generator-form");
  const output = document.getElementById("output");

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const formData = new FormData(form);

    fetch("/generate", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        output.value = data.password; // Update the input box with the generated password
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});
