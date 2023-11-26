$(document).ready(function () {
    // Captura el evento de envío del formulario
    $('form').on('submit', function (event) {
        // Evita la recarga de la página
        event.preventDefault();

        // Obtiene el valor del código de barras del formulario
        var cod_barra = $('#cod_barra').val();

        // Realiza la solicitud AJAX para agregar el producto
        $.ajax({
            type: 'GET',
            url: '/venta/agregar_producto/',
            data: { 'cod_barra': cod_barra },
            dataType:"json",
            success: function (respuestaJSON) {
                // Verifica si la respuesta es exitosa
                if (respuestaJSON.status === 'success') {
                    // Recorre los productos y agrega las filas a la tabla
                    respuestaJSON.productos.forEach(function (producto) {
                        agregarFila(producto);
                    });

                    
                } else {
                    console.error('Error al agregar producto:', respuestaJSON.error);
                }
            },
            error: function (error) {
                console.error('Error en la solicitud AJAX:', error.responseText);
            }
        });
    });
});

// Función para agregar las filas a la tabla
function agregarFila(producto) {
    var fila = `<tr data-producto_id="${producto.id}">
                    <td>${producto.name}</td>
                    <td>${producto.name_category}</td>
                    <td>$${producto.price_sold}</td>
                    <td>${producto.stock}</td>
                    <td>${producto.bar_code}</td>
                    <td><button class="btn btn-danger">Eliminar</button></td>
                </tr>`;
    
    // Agrega la fila a la tabla
    $("#tabla-productos").append(fila);
}



