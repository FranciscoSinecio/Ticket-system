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
    // agregar aquí la lógica para confirmar los cambios antes de enviar el formulario.
    // mostrar un mensaje de confirmación o solicitar una confirmación adicional.
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
