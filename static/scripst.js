document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.querySelector('input[type="file"]');
    const uploadButton = document.querySelector('button');

    uploadButton.addEventListener('click', function (event) {
        if (!fileInput.value) {
            event.preventDefault();
            alert('Por favor, selecciona un archivo para subir.');
        }
    });
});
