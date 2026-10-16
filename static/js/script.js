// For Theme Icon

const html = document.documentElement;
const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");

const savedTheme = localStorage.getItem("theme");

if (savedTheme) {
    html.setAttribute("data-bs-theme", savedTheme);
}

function updateThemeIcon() {
    const currentTheme = html.getAttribute("data-bs-theme");

    if (currentTheme === "dark") {
        themeIcon.className = "bi bi-sun-fill";
    } else {
        themeIcon.className = "bi bi-moon-fill";
    }
}

updateThemeIcon();

themeToggle.addEventListener("click", function () {
    const currentTheme = html.getAttribute("data-bs-theme");

    const newTheme =
        currentTheme === "dark" ? "light" : "dark";

    html.setAttribute("data-bs-theme", newTheme);
    localStorage.setItem("theme", newTheme);

    updateThemeIcon();
});


