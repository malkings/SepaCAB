var modal = document.getElementById('modalsi');
    var botonMostrar = document.getElementById('btn-abrir');

    botonMostrar.onclick = function() {
      modal.style.display = 'block';
    }

    function btn_cerrar(){
      modal.style.display = 'none';
    }

    window.onclick = function(event){
      if (event.target == modal) {
        modal.style.display = 'none'
      }
    }
