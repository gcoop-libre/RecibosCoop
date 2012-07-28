$(document).ready(function() {
  $.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
  });

  $('#retiros').dataTable({
    "bLengthChange": false,
    "bInfo": true,
    "bPaginate": true,
    "bSortable": false,
    "bSort": false,
   
    "bServerSide": true,
    "sAjaxSource": "/obtener_retiros",
    "sDom": "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>",
  });


});
