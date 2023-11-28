
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
    } else {
        fila += `<td><button class="btn btn-danger">Eliminar</button></td>`;
    }

    fila += `</tr>`;

    $(tabla).append(fila);
}





