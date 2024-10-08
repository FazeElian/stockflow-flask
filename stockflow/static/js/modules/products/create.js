const fileInput = document.getElementById('custom-file-input');
const imagePreview = document.getElementById('image-preview');

fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'flex';
        }
        reader.readAsDataURL(file);
    } else {
        imagePreview.style.display = 'none';
        alert('Por favor, selecciona un archivo de imagen válido.');
    }
});