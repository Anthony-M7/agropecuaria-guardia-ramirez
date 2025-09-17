document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const usernameInput = document.getElementById('id_username');
    const passwordInput = document.getElementById('id_password');
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    const errorMessage = document.getElementById('error-message');
    const togglePassword = document.getElementById('togglePassword');
    const toggleIcon = document.getElementById('toggleIcon');
    
    
    let currentImageIndex = 0;
    const backgroundSlideshow = document.getElementById('background-slideshow');

    function changeBackground() {
        backgroundSlideshow.style.backgroundImage = `url('${backgroundImages[currentImageIndex]}')`;
        currentImageIndex = (currentImageIndex + 1) % backgroundImages.length;
    }
    
    changeBackground(); // Llama a la función la primera vez
    setInterval(changeBackground, 10000); // Cambia cada 10 segundos

    // Lógica para mostrar/ocultar contraseña
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        toggleIcon.classList.toggle('fa-eye');
        toggleIcon.classList.toggle('fa-eye-slash');
    });

    // Lógica para validaciones de cliente
    form.addEventListener('submit', function(event) {
        let hasError = false;
        let message = '';

        // Expresión regular: solo letras, números, _ y .
        const validCharsRegex = /^[a-zA-Z0-9_.]+$/;

        if (!validCharsRegex.test(usernameInput.value)) {
            hasError = true;
            message = 'El usuario solo puede contener letras, números, guiones bajos (_) y puntos (.).';
        } else if (!validCharsRegex.test(passwordInput.value)) {
            hasError = true;
            message = 'La contraseña solo puede contener letras, números, guiones bajos (_) y puntos (.).';
        }

        if (hasError) {
            event.preventDefault();
            errorMessage.textContent = message;
            errorModal.show();
        } else {
            // Si las validaciones del cliente pasan, muestra el cargador
            showLoader();
        }
    }); 
});

if (document.getElementById("id_email")) {
    const emailInput = document.getElementById('id_email');
    emailInput.classList.add('form-control');
}

if (document.getElementById("id_new_password1")) {
    const newPasswordInput = document.getElementById('id_new_password1');
    newPasswordInput.classList.add('form-control');
}

if (document.getElementById("id_new_password2")) {
    const newPasswordInput2 = document.getElementById('id_new_password2');
    newPasswordInput2.classList.add('form-control');
}