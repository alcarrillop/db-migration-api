function deleteData(endpoint) {
    fetch(endpoint, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function limpiarTabla(tabla) {
    fetch(`/upload-csv/table-${tabla}/delete`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        // Muestra el mensaje JSON en un alerta
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while trying to send data.');
    });
}

function openNewWindow(url) {
    window.open(url, '_blank');
}

function enviarDatos(formulario, endpoint) {
    console.log("Función enviarDatos llamada con endpoint:", endpoint);  // Para depuración

    const formData = new FormData(formulario);

    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log("Respuesta del servidor:", response);  // Para depuración
        return response.json();
    })
    .then(data => {
        console.log("Datos JSON del servidor:", data);  // Para depuración
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while trying to send data.');
    });
}
