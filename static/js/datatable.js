$(document).ready(function() {
        $('#retiros').dataTable({
            "bLengthChange": false,
            //"bInfo": true,
            //"bPaginate": true,
            //"bSortable": false,

            //"bSort": true,
            "bServerSide": true,
            "sAjaxSource": "/obtener_retiros",
    });
});
