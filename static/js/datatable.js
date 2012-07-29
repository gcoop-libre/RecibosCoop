$(document).ready(function() {
  $.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
  });

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
  });

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
