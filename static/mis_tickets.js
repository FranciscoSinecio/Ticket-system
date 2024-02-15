function confirmarCancelar(ticketId) {
    if (confirm('¿Seguro desea cancelar el ticket?')) {
      // lógica para cancelar el ticket
      // enviar una solicitud AJAX al servidor para eliminar el ticket de la base de datos
      // mensaje de confirmación
      alert('Ticket cancelado exitosamente');
      // mensaje de alerta indicando que el ticket fue cancelado
    }
  }
  