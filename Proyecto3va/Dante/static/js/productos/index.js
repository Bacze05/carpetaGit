var $ = jQuery.noConflict();

function listarProductos() {
    // Obtener el nombre de la categoría de la URL
    var nombre = window.location.pathname.split('/').filter(Boolean).pop();

    // Añadir un log para verificar el valor de nombre
    console.log("Nombre de la categoría:", nombre);

    $.ajax({
        url: `/categorias/list/${nombre}/`,
        type: "get",
        dataType: "json",
        success: function (response) {
            $('#tabla_productos tbody').html("");
            for(let i = 0;i < response.length;i++){
                let fila = '<tr>';
                fila += '<td>' + response[i]["pk"]+'</td>';
                fila += '<td>' + response[i]["fields"]['name'] + '</td>';
                fila += '<td>' + response[i]["fields"]['stock'] + '</td>';
                fila += '<td>' + response[i]["fields"]['price_sold'] + '</td>';
                fila += '<td><button type="button" class="btn btn-primary" >Editar </button> <button class= "btn btn-danger">Eliminar</button></td>';
                fila += '</tr>';
                $('#tabla_productos tbody').append(fila);
            }
            $('#tabla_productos').DataTable({
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "Mostrando START a END de TOTAL Entradas",
                    infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                    infoFiltered: "(Filtrado de MAX total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar MENU Entradas",
                    loadingRecords: "Cargando...",
                    processing: "Procesando...",
                    search: "Buscar:",
                    zeroRecords: "Sin resultados encontrados",
                    paginate: {
                      first: "Primero",
                      last: "Ultimo",
                      next: "Siguiente",
                      previous: "Anterior",
                    },
                  },
                //   "searching": false,
                pageLength: 6,
            });
        },
        error: function (error) {
            console.error("Error al obtener productos:", error.responseText);
        }
    });
}


$(document).ready(function () {
    
    listarProductos();
    
});
