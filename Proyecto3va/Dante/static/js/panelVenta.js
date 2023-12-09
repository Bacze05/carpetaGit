// Inicializa DataTables para las dos tablas fuera de las funciones
$(document).ready(function () {
  limpiarTabla("#tabla_venta tbody");
  limpiarTabla("#tabla_subtotal tbody");
  $("#bar_code").on("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      listarVentaProductos();
      listarVentaDetalle();
    }
  });
});

//esta funcion limpiara la tabla
function limpiarTabla(tabla) {
  $(tabla).html("");
}

function mostrarMensaje(mensaje) {
  // Mostrar el mensaje en un elemento en la página, por ejemplo, un div con el id 'mensaje'
  $("#mensaje").text(mensaje).fadeIn().delay(3000).fadeOut();
}

function listarVentaProductos() {
  //creamos una variable para ingresar el bar_code
  var bar_code = $("#bar_code").val();
  $.ajax({
    url: "/listaVenta/",
    type: "get",
    data: { bar_code: bar_code },
    dataType: "json",
    success: function (response) {
      if (response.length > 0) {
        response.forEach(function (producto) {
          agregarFila("#tabla_venta tbody", producto, false);
        });
        $("#bar_code").val("");
      } else {
        // Mostrar mensaje indicando que el código de barras no existe
        mostrarMensaje("Código de barras no encontrado.");
        $("#bar_code").val("");
      }
    },
    error: function (error) {
      console.error("Error al obtener productos:", error.responseText);
    },
  });
}

function listarVentaDetalle() {
  var bar_code = $("#bar_code").val();

  $.ajax({
    url: "/listaVenta/",
    type: "get",
    data: { bar_code: bar_code },
    dataType: "json",
    success: function (response) {
      if (response.length > 0) {
        response.forEach(function (producto) {
          agregarFila("#tabla_subtotal tbody", producto, true);
        });

        $("#bar_code").val("");
      } else {
        // Mostrar mensaje indicando que el código de barras no existe
        mostrarMensaje("Código de barras no encontrado.");
      }
    },
    error: function (error) {
      console.error("Error al obtener productos:", error.responseText);
    },
  });
}

function actualizarTotal() {
  var total = 0;

  // Itera sobre las filas de la tabla de subtotales y suma los valores
  $("#tabla_subtotal tbody tr").each(function () {
    var subtotal = parseFloat(
      $(this).find("td.subtotal").text().replace("$", "").trim()
    );
    total += isNaN(subtotal) ? 0 : subtotal;
  });

  // Actualiza el valor en el elemento totalCalculadora
  $("#totalCalculadora").text(total.toFixed(0)); // Puedes ajustar el número de decimales según tu necesidad
}

function agregarFila(tabla, producto, esSubtotal) {
  var cantidad = 1; // Define la cantidad según tu lógica
  var subtotal = cantidad * producto.price_sold;
  var filaExistente = $(`${tabla} tr[data-producto="${producto.bar_code}"]`);
 
  if (filaExistente.length > 0 && esSubtotal) {
     // Si ya existe una fila para este producto en la tabla subtotal, actualiza la cantidad y el subtotal
     cantidad = parseInt(filaExistente.find("td.cantidad").text()) + 1;
     filaExistente.find("td.cantidad").text(cantidad);
 
     subtotal = cantidad * producto.price_sold;
     filaExistente.find("td.subtotal").text(`$${subtotal}`);
     actualizarTotal();
 
     return;
  }
 
  var fila = `<tr data-producto="${producto.bar_code}"> <input type="hidden" value="${producto.id}" name="producto_id" />
                     <td>${producto.name}</td>`;
 
  if (!esSubtotal) {
     fila += `<td>${producto.bar_code}</td>
                  <td>${producto.stock}</td>`;
  }
 
  fila += `<td >$${producto.price_sold}</td> <input type="hidden" value="${producto.price_sold}" name="price_sold" />`;
 
  if (esSubtotal) {
    fila += `<td class="cantidad">${cantidad}</td> 
             <td class="subtotal">$${subtotal}</td>`;

 
  }
  // else {
  //     fila += `<td><button class="btn btn-danger">Eliminar</button></td>`;
  // }
 
 
  console.log(fila)
  $(tabla).append(fila);


  actualizarTotal();
  // Actualiza los campos ocultos en el formulario de venta
  $("#producto_id").val(producto.id);
  $("#bar_code").val(producto.bar_code);
  $("#cantidad").val(cantidad);
  $("#price_sold").val(producto.price_sold);
  console.log("Campos ocultos actualizados. Datos enviados al formulario de venta:");
  console.log("producto_id:", producto.id);  // Verifica que esto imprima algo en la consola
  console.log("price_sold",producto.price_sold)
  console.log("bar_code:", producto.bar_code);
  console.log("cantidad:", cantidad);
  console.log("totalCalculadora",subtotal )
 }
