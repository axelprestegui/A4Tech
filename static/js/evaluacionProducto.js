const opiniones = document.getElementsByClassName('opiniones');
const escribeResenia = document.getElementById('escribeResenia');
const resenia = document.getElementById('resenia');

escribeResenia.removeAttribute('disabled');

/** 
 * Función usada para hacer aparecer el recuadro de escribir la reseña y poder enviarla cuando el botón
 * de escribeResenia está habilitado.
 */
const apareceResenia = () => {
    escribeResenia.addEventListener('click', () => {
        resenia.classList.remove('resenia');
    })
}

const obtenerComentarios = () => {
    
}

apareceResenia();