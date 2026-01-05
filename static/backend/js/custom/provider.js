/** gestion des tables list */
$("#searchprovider").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterprovider tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**marques creation */
$("#addprovider").on("click", function(e){
    e.preventDefault();
    $("#providerCreation").modal("show");
})

/**administrateur mis a jour */
$(".updateProvider").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');    
    var name = $(this).data('name');
    var logo = $(this).data('logo');
    $('#providerid').val(id);
    $('#providername').val(name);
    $('#providerUpdate').modal("show");
})