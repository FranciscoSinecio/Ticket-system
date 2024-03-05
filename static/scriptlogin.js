document.querySelector("#loginForm").addEventListener("submit", function(event) {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if (!isValidEmail(username) || !isValidPassword(password)) {
        event.preventDefault(); // Evita que se envíe el formulario
        document.getElementById("errorMessage").innerText = "Verifica que tu correo o contraseña sean correctos.";
    }
});

// Función para validar el correo electrónico
function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

