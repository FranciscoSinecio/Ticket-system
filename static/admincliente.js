// Script actual y nuevo script
function openEditModal() {
    document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

function openPasswordModal() {
    document.getElementById('passwordModal').style.display = 'block';
}

function closePasswordModal() {
    document.getElementById('passwordModal').style.display = 'none';
}

function confirmProfileChanges() {

    //OBTENEMOS LOS DATOS DEL formulario
    var formData = new  FormData(document.getElementById('editModal').querySelector('form'));

    fetch('/edit_profile',{
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok){
            throw new Error('Hubo un problema al guardar los cambios.');
        }
        //si la respuesta es exitosa, mostrar un mensaje y recargar la pagina
        alert('¡Los cambios se han guardado exitosamente!');
        window.location.reload(); 
    })
    .catch(error =>{
        alert(error.message);
    });
}

function confirmPasswordChange() {
    // agregar aquí la lógica para confirmar la contraseña antes de enviar el formulario.
    // comparar la nueva contraseña con la confirmación.
}

const draggable = new Draggable(document.querySelectorAll('.draggable'), {
    handle: '.modal-header',
});

let lastScrollTop = 0;

window.addEventListener("scroll", function () {
    var st = window.pageYOffset || document.documentElement.scrollTop;
    if (st > lastScrollTop) {
        document.querySelector('.footer').classList.add('scrolling');
    } else {
        document.querySelector('.footer').classList.remove('scrolling');
    }
    lastScrollTop = st <= 0 ? 0 : st;
});

function goBack() {
    window.history.back();
}
