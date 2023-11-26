$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        var cod_barra = $('#cod_barra').val();

        $.ajax({
            type: 'GET',
            url: '/venta/agregar_producto/',
            data: { 'bar_code': cod_barra },
            success: function (data) {
                console.log(data);
                // $('#tabla-productos').append(data);
                // $('#cod_barra').val('');

                // // No es necesario recargar toda la página aquí
                // // Actualizar la calculadora es suficiente
                // actualizarCalculadora();
            },
            error: function (error) {
                console.error('Error al agregar producto:', error.responseText);
            }
        });
    });

    function restar_stock() {
        var productosProductos = $('#tabla-productos tr');

        productosProductos.each(function () {
            var productoCodBarra = $(this).find('td:eq(4)').text();
            var productoStock = parseInt($(this).find('td:eq(3)').text());

            // Reducir el stock solo si es mayor que cero
            if (productoStock > 0) {
                productoStock = productoStock - 1;
                $(this).find('td:eq(3)').text(productoStock);

                // Llamada AJAX para restar el stock en el servidor
                $.get('/venta/reducir_stock/', { cod_barra: productoCodBarra }, function (data) {
                    // Manejar la respuesta del servidor si es necesario
                });
            }
        });
    }

    // Asignar función restar_stock al botón de confirmar
    $(document).on('click', '.reducir-stock-btn', function () {
        restar_stock();
        console.log("Btn presionado");
        // No es necesario recargar toda la página aquí
        // Actualizar la calculadora es suficiente
        actualizarCalculadora();
    });

    // Función para eliminar una fila
    function eliminarFila(button) {
        var fila = $(button).closest('tr');
        fila.remove();
        actualizarCalculadora();
    }

    // Asigna el evento onclick a los botones de eliminar
    $(document).on('click', '.btn-danger', function () {
        eliminarFila(this);
    });

    function actualizarCalculadora() {
        var productosProductos = $('#tabla-productos tr');
        var productosCalculadora = $('#tabla-calculadora');

        productosCalculadora.empty(); // Limpiar la tabla de la calculadora
        var productosContados = {}; // Objeto para llevar un registro de las cantidades

        productosProductos.each(function () {
            var productoNombre = $(this).find('td:eq(0)').text();
            var productoPrecio = parseFloat($(this).find('td:eq(2)').text().replace('$', ''));
            var productoStock = parseInt($(this).find('td:eq(3)').text());

            var productoKey = productoNombre + '_' + productoPrecio;

            if (productosContados[productoKey]) {
                productosContados[productoKey].cantidad++;
            } else {
                productosContados[productoKey] = {
                    cantidad: 1,
                    nombre: productoNombre,
                    precio: productoPrecio,
                    stockOriginal: productoStock,
                    stock: productoStock > 0 ? productoStock - 1 : 0,
                };
            }
        });

        var totalCalculadora = 0;

        for (var productoId in productosContados) {
            var producto = productosContados[productoId];
            var productoPrecio = parseFloat(producto.precio);
            var subtotal = producto.cantidad * productoPrecio;

            var nuevaFila = `
            <tr>
            <td>${producto.nombre}</td>
            <td>${producto.cantidad}</td>
            <td>$${productoPrecio}</td>
            <td class="stock-column">${producto.stock}</td>
            <td><span id="subtotal-${productoId}">$${subtotal}</span></td>
            </tr>`;

            productosCalculadora.append(nuevaFila);
            totalCalculadora += subtotal;

            $('#subtotal-' + productoId).text('$' + subtotal);
        }

        $('#totalCalculadora').text('$' + totalCalculadora);
    }
});
