
$(document).ready(function () {
    limpiarTabla();
    listarVentaProductos();
    $('#bar_code').on('keydown', function (event) {
        // Verifica si la tecla presionada es "Enter"
        if (event.key === 'Enter') {
            // Evita que el formulario se envíe automáticamente
            event.preventDefault();

            // Llama a la función que realiza la búsqueda
            listarVentaProductos();
        }
    });
});

function limpiarTabla() {
    // Limpia el contenido de la tabla al inicio
    $('#tabla_venta tbody').html("");
}

function listarVentaProductos() {
    var bar_code = $('#bar_code').val();
    $.ajax({
        url: '/venta_List/',
        type: "get",
        data: { 'bar_code': bar_code },
        dataType: "json",
        success: function(response) {
            // Agrega filas solo si hay nuevos datos
            if (response.length > 0) {
                response.forEach(function (producto) {
                    agregarFila(producto);
                });
                $('#bar_code').val('');
            }
        },
        error: function (error) {
            console.error("Error al obtener productos:", error.responseText);
        }
    });
}

function agregarFila(producto) {
    var fila = `<tr>
                    <td>${producto.bar_code}</td>
                    <td>${producto.name}</td>
                    <td>${producto.stock}</td>
                    <td>$${producto.price_sold}</td>
                    <td><button class="btn btn-danger">Eliminar</button></td>
                </tr>`;

    // Agrega la fila a la tabla
    $("#tabla_venta tbody").append(fila);
}