function confirmarCancelar(id_ticket) {
  if (confirm('¿Seguro desea cancelar el ticket?')) {
    // Enviar una solicitud AJAX al servidor para cancelar el ticket
    fetch(`/cancelar_ticket/${id_ticket}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Ticket cancelado exitosamente');
            window.location.reload(); // Recargar la página después de la cancelación
        } else {
            alert('Hubo un error al cancelar el ticket.');
        }
    })
    .catch(error => console.error('Error:', error));
}
}