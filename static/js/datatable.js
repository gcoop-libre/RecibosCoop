$(document).ready(function() {
  $.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
  });

  $('#retiros').dataTable({
    bLengthChange: false,
    bInfo: true,
    bPaginate: true,
    bSortable: false,
    bSort: false,

    /* Traducciones */
    oLanguage: {
			sSearch: "Buscar:",
			sZeroRecords: "No hay nada que mostrar",
			sInfo: "Mostrando de _START_ a _END_ (hay _TOTAL_ registros en total)",
			sInfoEmpty: "No hay registros que mostrar",
			sInfoFiltered: "(filtrado de _MAX_ registros)",
		},

    "bServerSide": true,
    "sAjaxSource": "/obtener_retiros",
  });


});
