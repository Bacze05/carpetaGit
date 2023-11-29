
// Inicializa DataTables para las dos tablas fuera de las funciones
$(document).ready(function () {
    limpiarTabla('#tabla_venta tbody');
    limpiarTabla('#tabla_subtotal tbody');
    $('#bar_code').on('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            listarVentaProductos();
            listarVentaDetalle();
        }
    });

 
});

function limpiarTabla(tabla) {
    $(tabla).html("");
}

function mostrarMensaje(mensaje) {
    // Mostrar el mensaje en un elemento en la página, por ejemplo, un div con el id 'mensaje'
    $('#mensaje').text(mensaje).fadeIn().delay(3000).fadeOut();
}

function listarVentaProductos() {
    var bar_code = $('#bar_code').val();
    $.ajax({
        url: '/venta_List/',
        type: "get",
        data: { 'bar_code': bar_code },
        dataType: "json",
        success: function(response) {
            if (response.length > 0) {
                response.forEach(function (producto) {
                    agregarFila('#tabla_venta tbody', producto, false);
                });
                $('#bar_code').val('');
            } else {
                // Mostrar mensaje indicando que el código de barras no existe
                mostrarMensaje("Código de barras no encontrado.");
            }
        },
        error: function (error) {
            console.error("Error al obtener productos:", error.responseText);
        }
    });
}

function listarVentaDetalle() {
    var bar_code = $('#bar_code').val();
    $.ajax({
        url: '/venta_List/',
        type: "get",
        data: { 'bar_code': bar_code },
        dataType: "json",
        success: function(response) {
            if (response.length > 0) {
                response.forEach(function (producto) {
                    agregarFila('#tabla_subtotal tbody', producto, true);
                });
                $('#bar_code').val('');
            } else {
                // Mostrar mensaje indicando que el código de barras no existe
                mostrarMensaje("Código de barras no encontrado.");
            }
        },
        error: function (error) {
            console.error("Error al obtener productos:", error.responseText);
        }
    });
}
function actualizarTotal() {
    var total = 0;

    // Itera sobre las filas de la tabla de subtotales y suma los valores
    $('#tabla_subtotal tbody tr').each(function() {
        var subtotal = parseFloat($(this).find('td.subtotal').text().replace('$', '').trim());
        total += isNaN(subtotal) ? 0 : subtotal;
    });

    // Actualiza el valor en el elemento totalCalculadora
    $('#totalCalculadora').text(total.toFixed(0)); // Puedes ajustar el número de decimales según tu necesidad
}
// Función para eliminar una fila
function eliminarFila(button) {
    var fila = $(button).closest('tr');
    var esSubtotal = fila.closest('table').attr('id') === 'tabla_subtotal'; // Verifica si la fila pertenece a la tabla de subtotales

    if (esSubtotal) {
        restarCantidad(fila);
    } else {
        fila.remove();
    }
}

// Función para restar 1 a la cantidad y actualizar la fila de subtotal
function restarCantidad(fila) {
    var cantidad = parseInt(fila.find('td.cantidad').text());

    if (cantidad > 1) {
        // Si la cantidad es mayor a 1, restar 1 y actualizar la fila
        cantidad -= 1;
        fila.find('td.cantidad').text(cantidad);
        var producto = obtenerDatosProducto(fila);
        var subtotal = cantidad * producto.price_sold;
        fila.find('td.subtotal').text(`$${subtotal}`);
    } else {
        // Si la cantidad es 1 o menos, eliminar la fila
        fila.remove();
    }

    actualizarTotal();
}

// Función para obtener los datos del producto desde la fila
function obtenerDatosProducto(fila) {
    return {
        bar_code: fila.data('producto'),
        name: fila.find('td:first-child').text(),
        price_sold: parseFloat(fila.find('td:last-child').text().replace('$', '').trim())
    };
}



// Asigna el evento onclick a los botones de eliminar
$(document).on('click', '.btn-danger', function () {
    eliminarFila(this);
});
function agregarFila(tabla, producto, esSubtotal) {
    var cantidad = 1; // Define la cantidad según tu lógica
    var subtotal = cantidad * producto.price_sold;

    var filaExistente = $(`${tabla} tr[data-producto="${producto.bar_code}"]`);

    if (filaExistente.length > 0 && esSubtotal) {
        // Si ya existe una fila para este producto en la tabla subtotal, actualiza la cantidad y el subtotal
        cantidad = parseInt(filaExistente.find('td.cantidad').text()) + 1;
        filaExistente.find('td.cantidad').text(cantidad);

        subtotal = cantidad * producto.price_sold;
        filaExistente.find('td.subtotal').text(`$${subtotal}`);
        actualizarTotal();

        return;
    }

    var fila = `<tr data-producto="${producto.bar_code}">
                    <td>${producto.name}</td>`;

    if (!esSubtotal) {
        fila += `<td>${producto.bar_code}</td>
                 <td>${producto.stock}</td>`;
    }

    fila += `<td>$${producto.price_sold}</td>`;

    if (esSubtotal) {
        fila += `<td class="cantidad">${cantidad}</td>
                 <td class="subtotal">$${subtotal}</td>`;
    } 
    else {
        fila += `<td><button class="btn btn-danger">Eliminar</button></td>`;
    }

    fila += `</tr>`;

    $(tabla).append(fila);
    actualizarTotal();

}



