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

  function reemplazar_boton_generar_pdf_concatenados(){
    $("#submit_pdf").click(function(){
          $(this).attr('disabled', 'disabled');
          $.ajax({
              type: "POST",
              url: $("#formulario_recibos").attr('action'),
              data: $("#formulario_recibos").serialize(),
              dataType: "script",
              beforeSend: function(objeto){
                borrar_mensajes();
                mostrar_mensaje_progreso("Procesando...");
              },
              success: function(msg){
                borrar_mensajes();
                mostrar_mensaje("Se ha generado el PDF correctamente.");
              },
              error: function(_, _, motivo){
                borrar_mensajes();
                mostrar_mensaje(motivo, "error");
              }
          });

          return false;
      });
  }

  reemplazar_boton_generar_pdf_concatenados();
})
