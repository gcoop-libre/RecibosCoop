$(document).ready(function (){

  function mostrar_mensaje(mensaje, tipo) {
    var tipo = tipo || 'success';
    var placeholder = $(".contenido .span8 form");
    var template = '<div class="alert alert-block alert-{{tipo}}">{{{close_button}}} <p>{{{mensaje}}}</p></div>';
    var values = {
        close_button: '<a class="close" data-dismiss="alert" href="#">×</a>',
        mensaje: mensaje,
        tipo: tipo 
    }
    var html = Mustache.render(template, values);

    placeholder.before(html);
  }

  function borrar_mensajes() {
    $(".close").click();
  }

  function mostrar_mensaje_progreso(mensaje){
    var imagen = "<img src='/static/images/progress.gif'> ";
    mostrar_mensaje(imagen + mensaje, 'info');
  }
})
