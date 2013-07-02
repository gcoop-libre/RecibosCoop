/* Set the defaults for DataTables initialisation */
$.extend( true, $.fn.dataTable.defaults, {
	"sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
	"sPaginationType": "bootstrap",
	"oLanguage": {
		"sLengthMenu": "_MENU_ records per page"
	}
} );


/* Default class modification */
$.extend( $.fn.dataTableExt.oStdClasses, {
	"sWrapper": "dataTables_wrapper form-inline"
} );


/* API method to get paging information */
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
	return {
		"iStart":         oSettings._iDisplayStart,
		"iEnd":           oSettings.fnDisplayEnd(),
		"iLength":        oSettings._iDisplayLength,
		"iTotal":         oSettings.fnRecordsTotal(),
		"iFilteredTotal": oSettings.fnRecordsDisplay(),
		"iPage":          oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
		"iTotalPages":    oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
	};
};


/* Bootstrap style pagination control */
$.extend( $.fn.dataTableExt.oPagination, {
	"bootstrap": {
		"fnInit": function( oSettings, nPaging, fnDraw ) {
			var oLang = oSettings.oLanguage.oPaginate;
			var fnClickHandler = function ( e ) {
				e.preventDefault();
				if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
					fnDraw( oSettings );
				}
			};

			$(nPaging).addClass('pagination').append(
				'<ul>'+
					'<li class="prev disabled"><a href="#">&larr; Anterior</a></li>'+
					'<li class="next disabled"><a href="#">Siguiente &rarr; </a></li>'+
				'</ul>'
			);
			var els = $('a', nPaging);
			$(els[0]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
			$(els[1]).bind( 'click.DT', { action: "next" }, fnClickHandler );
		},

		"fnUpdate": function ( oSettings, fnDraw ) {
			var iListLength = 5;
			var oPaging = oSettings.oInstance.fnPagingInfo();
			var an = oSettings.aanFeatures.p;
			var i, ien, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);

			if ( oPaging.iTotalPages < iListLength) {
				iStart = 1;
				iEnd = oPaging.iTotalPages;
			}
			else if ( oPaging.iPage <= iHalf ) {
				iStart = 1;
				iEnd = iListLength;
			} else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
				iStart = oPaging.iTotalPages - iListLength + 1;
				iEnd = oPaging.iTotalPages;
			} else {
				iStart = oPaging.iPage - iHalf + 1;
				iEnd = iStart + iListLength - 1;
			}

			for ( i=0, ien=an.length ; i<ien ; i++ ) {
				// Remove the middle elements
				$('li:gt(0)', an[i]).filter(':not(:last)').remove();

				// Add the new list items and their event handlers
				for ( j=iStart ; j<=iEnd ; j++ ) {
					sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
					$('<li '+sClass+'><a href="#">'+j+'</a></li>')
						.insertBefore( $('li:last', an[i])[0] )
						.bind('click', function (e) {
							e.preventDefault();
							oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
							fnDraw( oSettings );
						} );
				}

				// Add / remove disabled classes from the static elements
				if ( oPaging.iPage === 0 ) {
					$('li:first', an[i]).addClass('disabled');
				} else {
					$('li:first', an[i]).removeClass('disabled');
				}

				if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
					$('li:last', an[i]).addClass('disabled');
				} else {
					$('li:last', an[i]).removeClass('disabled');
				}
			}
		}
	}
} );


/*
 * TableTools Bootstrap compatibility
 * Required TableTools 2.1+
 */
if ( $.fn.DataTable.TableTools ) {
	// Set the classes that TableTools uses to something suitable for Bootstrap
	$.extend( true, $.fn.DataTable.TableTools.classes, {
		"container": "DTTT btn-group",
		"buttons": {
			"normal": "btn",
			"disabled": "disabled"
		},
		"collection": {
			"container": "DTTT_dropdown dropdown-menu",
			"buttons": {
				"normal": "",
				"disabled": "disabled"
			}
		},
		"print": {
			"info": "DTTT_print_info modal"
		},
		"select": {
			"row": "active"
		}
	} );

	// Have the collection use a bootstrap compatible dropdown
	$.extend( true, $.fn.DataTable.TableTools.DEFAULTS.oTags, {
		"collection": {
			"container": "ul",
			"button": "li",
			"liner": "a"
		}
	} );
}


/* Table initialisation */
$(document).ready(function() {


  function cambio_checkbox_recibo() {
    var a = $('.selector_recibo').map(
      function(idx, element) { return element.checked;
      });
    
    if (!this.checked){
      $('#seleccionar_todos').attr('checked', false);
      
      if ($.inArray(true, a) === -1) {
        $('#submit_pdf').attr('disabled', true);
        $('#submit_zip').attr('disabled', true);
        $('.operacion_masiva').hide();
      }
    }
    else {
        $('.operacion_masiva').show();
      if ($.inArray(false, a) === -1) {
        $('#seleccionar_todos').attr('checked', true);
      }
      $('#submit_pdf').removeAttr('disabled');
      $('#submit_zip').removeAttr('disabled');
    }
  }

  function cambio_checkbox() {
    if (this.checked){
      $('#submit_pdf').removeAttr('disabled');
      $('#submit_zip').removeAttr('disabled');
      $('.selector_recibo').attr('checked', true);
    } else { 
      $('.selector_recibo').attr('checked', false);
      $('#submit_pdf').attr('disabled', true);
      $('#submit_zip').attr('disabled', true);
    }
  }





	$('#example').dataTable( {
		"sDom": "<'row'<'span6'><'span6'f>r>t<'row'<'span6'il><'span6'p>>",
		"sPaginationType": "bootstrap",
		"oLanguage": {
			"sLengthMenu": "Mostrar _MENU_ registros por página",
			"sInfo": "Mostrando de _START_ a _END_ de _TOTAL_ registros en total",
			"sEmptyTable": "No hay datos para mostrar",
			"sInfoEmpty": "No hay elementos para mostrar"
		},
    "aoColumns": [
      {bSortable: false},
      null,
      {sClass: 'fecha'},
      {sClass: 'monto', sWidth: "80px"},
      {sClass: 'acciones', bSortable: false},
    ],
    "bServerSide": true,
    "sAjaxSource": "/obtener_retiros",
    "fnDrawCallback": function (){
        $('.selector_recibo').change(cambio_checkbox_recibo);  
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


} );
