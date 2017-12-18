$(document).ready( function() {

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });

//    para agregar formularios de medicamentos.
    $('#formset').formset({
        addText: 'Agregar Medicamento',
        deleteText: 'Quitar Medicamento'
    });


});


