// JS code using fetch api to dynamically update the output box in generate passwords page

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("generator-form");
  const output = document.getElementById("output");

  if (form && output) {
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
  } else {
    console.error("Form or output element not found in the DOM.");
  }
});
