// Muestra el cargador y bloquea la interacción
function showLoader() {
    const loaderContainer = document.getElementById('loader-container');
    if (loaderContainer) {
        loaderContainer.style.display = 'flex';
    }
}

// Oculta el cargador y permite la interacción
function hideLoader() {
    const loaderContainer = document.getElementById('loader-container');
    if (loaderContainer) {
        loaderContainer.style.display = 'none';
    }
}

// Lógica para el cargador global
document.addEventListener('DOMContentLoaded', () => {
    // Muestra el cargador inmediatamente al cargar la página
    showLoader();

    // Oculta el cargador una vez que la página está completamente cargada
    window.addEventListener('load', () => {
        hideLoader();
    });

    // Escucha todas las peticiones fetch (GET, POST, etc.)
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        // Muestra el cargador antes de la petición
        showLoader();

        return originalFetch(...args)
            .finally(() => {
                // Oculta el cargador cuando la petición ha terminado
                hideLoader();
            });
    };

    // Escucha los cambios en el historial para navegación
    window.addEventListener('popstate', () => {
        showLoader();
    });
    
    // Oculta el cargador al final de la carga de la navegación popstate
    window.addEventListener('load', () => {
        hideLoader();
    });
});