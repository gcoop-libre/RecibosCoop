$(document).ready(function() {
  $.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
  });

  function cambio_checkbox_recibo(){
    if (!this.checked){
      $('#seleccionar_todos').attr('checked', false);
    }
  }

  function cambio_checkbox(){
    if (this.checked){
      $('.selector_recibo').attr('checked', true);
    } else { 
      $('.selector_recibo').attr('checked', false);
    }
  }

  var table = $('#retiros').dataTable({
    bLengthChange: false,
    bInfo: true,
    bPaginate: true,
    bSortable: false,
    bSort: false,
    iDisplayLength: 12,

    /* Traducciones */
    oLanguage: {
      sSearch: "Buscar:",
    sZeroRecords: "No hay nada que mostrar",
    sInfo: "Mostrando de _START_ a _END_ (hay _MAX_ registros en total)",
    sInfoEmpty: "No hay registros que mostrar",
    sInfoFiltered: "(filtrado de _MAX_ registros)",
    },

    "bServerSide": true,
    "sAjaxSource": "/obtener_retiros",
    "fnDrawCallback": function (){
      $('.selector_recibo').each(function(id){
        $(this).change(cambio_checkbox_recibo);
      });  
    }
  });

  $('#seleccionar_todos').change(cambio_checkbox);  
  
  /* Obtiene los parametos de la URL */
  function get_url_param(name) {
    var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);

    if (results)
      return results[1];
    else
      return null;
  }

  if (get_url_param('s')) {
    var busqueda = get_url_param('s').replace(/%2F/gi, "/");

    $("input[aria-controls='retiros']").val(busqueda);
    table.fnFilter(busqueda);
  } 

});
