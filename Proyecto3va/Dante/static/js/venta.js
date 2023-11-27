var $ = jQuery.noConflict();

function listarVentaProductos() {
    var bar_code = $('#bar_code').val();  // Obtener el valor de bar_code dentro de la función
    
    $.ajax({
        url: '/venta_List/',
        type: "get",
        data: { 'bar_code': bar_code },  // Actualiza la clave a 'bar_code'
        dataType: "json",
        success: function(response){
            $('#tabla_venta tbody').html("");

            function agregarFila(producto) {
                var fila = `<tr >
                                <td>${producto.name}</td>
                                <td>${producto.name_category}</td>
                                <td>$${producto.price_sold}</td>
                                <td>${producto.stock}</td>
                                <td>${producto.bar_code}</td>
                                <td><button class="btn btn-danger">Eliminar</button></td>
                            </tr>`;

                // Agrega la fila a la tabla
                $("#tabla_venta").append(fila);
            }

            $.each(response, function (index, producto) {
                agregarFila(producto);
            });

            // Inicializa el DataTable
            $('#tabla_venta').DataTable({
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                    infoFiltered: "(Filtrado de _MAX_ total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar _MENU_ Entradas",
                    loadingRecords: "Cargando...",
                    processing: "Procesando...",
                    search: "Buscar:",
                    zeroRecords: "Sin resultados encontrados",
                    paginate: {
                        first: "Primero",
                        last: "Ultimo",
                        next: "Siguiente",
                        previous: "Anterior"
                    }
                },
                pageLength: 6,
            });
        },
        error: function (error) {
            console.error("Error al obtener productos:", error.responseText);
        }
    });
}

$(document).ready(function () {
    listarVentaProductos();
    $('#btnBuscar').click(function () {
        var bar_code = $('#bar_code').val();
        
        // Validar que bar_code no esté vacío y sea un número
        if (bar_code !== '' && !isNaN(bar_code)) {
            listarVentaProductos();
        } else {
            console.error("Error: El valor de bar_code no es válido");
        }
    });

});
