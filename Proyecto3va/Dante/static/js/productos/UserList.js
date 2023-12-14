
var $ = jQuery.noConflict();

function listarUsuarios() {
    $.ajax({
        url: `/usuarios/`,
        type: "get",
        dataType: "json",
        success: function (response) {
            $('#tabla_usuarios tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + response[i]["fields"]['rut'] + '</td>';
                fila += '<td>' + response[i]["fields"]['username'] + '</td>';
                fila += '<td>' + response[i]["fields"]['first_name'] + ' ' + response[i]["fields"]['last_name'] + '</td>';
                fila += '<td>' + response[i]["fields"]['fecha_nacimiento'] + '</td>';


                // Obtener nombres de grupos
                let groupNames = [];
                for (let j = 0; j < response[i]["fields"]['groups'].length; j++) {
                    let groupId = response[i]["fields"]['groups'][j];
                    let groupName = getGroupName(groupId);
                    groupNames.push(groupName);
                }

                fila += '<td>' + groupNames.join(', ') + '</td>';
                // COMENTADO POR AHORA DESPUES HARE UN VENTANA PARA QUE SALGAN CON MAS DETALLE CADA USUARIO
                // fila += '<td>' + response[i]["fields"]['email'] + '</td>';

                fila += '<td><a href="/usuarios/edit/' + response[i]["pk"] + '" class="btn btn-primary"  >Editar </a> <a href="/usuarios/desactivar/' + response[i]["pk"] + '" class="btn btn-danger"  >Eliminar </a></td>';
                fila += '</tr>';
                $('#tabla_usuarios tbody').append(fila);
            }

            $('#tabla_usuarios').DataTable({
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
                pageLength: 6,
                columnDefs: [
                    { targets: [0,3,5], searchable: false }  // Desactiva la búsqueda para las columnas 0, 2 y 3
                ],
            });
        },
        error: function (error) {
            console.error("Error al obtener usuarios:", error.responseText);
        }
    });
}

// Función para obtener el nombre de un grupo por su ID
function getGroupName(groupId) {
    // Ajusta la URL según tu configuración
    var groupName = '';
    $.ajax({
        url: '/obtener_nombre_grupo/' + groupId,
        type: 'GET',
        async: false,  // Usamos async: false para esperar la respuesta antes de continuar
        success: function (data) {
            groupName = data.nombre_grupo;  // Ajusta esto según la estructura de tu respuesta
        },
        error: function (error) {
            console.error('Error al obtener el nombre del grupo', error);
            groupName = 'Desconocido';  // O proporciona un valor predeterminado
        }
    });

    return groupName;
}

$(document).ready(function () {
    listarUsuarios();
});
// Agregar evento de clic al botón "Crear Usuario"
$(document).on('click', '.btn-crear-usuario', function () {
    $.ajax({
        url: '/usuarios/',
        type: 'get',
        success: function (response) {
            // Actualizar el contenido del modal con el formulario
            $('#modalContent').html(response);
            // Mostrar el modal
            $('#creacion').modal('show');
        },
        error: function (error) {
            console.error('Error al cargar el formulario de creación de usuario:', error.responseText);
        }
    });
});

// Agregar evento de clic al botón "Guardar" dentro del modal
$(document).on('click', '#btn-guardar-usuario', function () {
    var formData = $('#tuFormulario').serialize();
    $.ajax({
        url: '/usuarios/',
        type: 'post',
        data: formData,
        success: function (response) {
            if (response.success) {
                // Si el formulario es válido, cierra el modal
                $('#creacion').modal('hide');
                // Actualizar la tabla de usuarios
                listarUsuarios();
            } else {
                // Si el formulario no es válido, actualiza el contenido del modal con los errores
                $('#modalContent').html(response.html_form);
            }
        },
        error: function (error) {
            console.error('Error al guardar el usuario:', error.responseText);
        }
    });
});
