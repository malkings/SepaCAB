document.getElementById('Verclave').addEventListener('click', function() {
    var passwordField = document.getElementById('claveingreso');
    var fieldType = passwordField.getAttribute('type');
    if (fieldType === 'password') {
        passwordField.setAttribute('type', 'text');
        this.classList.remove('lni-magnifier');
        this.classList.add('lni-close');
    } else {
        passwordField.setAttribute('type', 'password');
        this.classList.remove('lni-close');
        this.classList.add('lni-magnifier');
    }
});

// Función para mostrar u ocultar el botón de inicio de sesión
function verBotonLogin() {
    var btn_ingresar = document.getElementById("btn_ingresar");
    if (navigator.onLine) {
        btn_ingresar.style.display = "block"; // Mostrar el botón si hay conexión a Internet
    } else {
        btn_ingresar.style.display = "none"; // Ocultar el botón si no hay conexión
    }
}

 // Llamar a la función al cargar la página
window.onload = function() {
            verBotonLogin();
};

// Volver a verificar la conexión cada 5 segundos
setInterval(verBotonLogin, 5000);
