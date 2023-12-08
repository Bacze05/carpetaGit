var $ = jQuery.noConflict();

function listarProveedores() {

    $.ajax({
        url: `/proveedores/`,
        type: "get",
        dataType: "json",
        success: function (response) {
            $('#tabla_proveedores tbody').html("");
            for(let i = 0;i < response.length;i++){
                let fila = '<tr>';
                fila += '<td>' + response[i]["fields"]['run']+'</td>';
                fila += '<td>' + response[i]["fields"]['name'] + '</td>';
                fila += '<td>' + response[i]["fields"]['email'] + '</td>';
                fila += '<td>' + response[i]["fields"]['cellphone'] + '</td>';
                fila += '<td><a href="/proveedor/edit/' + response[i]["pk"] + '" class="btn btn-primary"  >Editar </a> <a href="/proveedor/eliminado/' + response[i]["pk"] + '" class="btn btn-danger"  >Eliminar </a></td>';
                fila += '</tr>';
                $('#tabla_proveedores tbody').append(fila);
            }
            $('#tabla_proveedores').DataTable({
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "",
                    infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                    infoFiltered: "(Filtrado de MAX total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "",
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
                  
                pageLength: 6,
                columnDefs: [
                    { targets: [ 2, 3,4], searchable: false }  // Desactiva la búsqueda para las columnas 0, 2 y 3
                ],
            });
        },
        error: function (error) {
            console.error("Error al obtener productos:", error.responseText);
        }
    });
}


$(document).ready(function () {
    
    listarProveedores();
    
});
