/** gestion des tables list */
$("#searchbank").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterbank tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**devises creation */
$("#addbank").on("click", function(e){
    e.preventDefault();
    $("#BankCreation").modal("show");
})

/**administrateur mis a jour */
$(".updatebank").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    var country = $(this).data('country');
    var countryid = $(this).data('countryid');
    var description = $(this).data('description');
    var perctransaction = $(this).data('perctransaction');
    var cover = $(this).data('cover');
    $('.ql-editor p').html(description);
    $('.post-content-update').val(description);

    $('#bankid').val(id);
    $('#bankname').val(name);
    $('#banktransactionperc').val(perctransaction);
    $('#bankcountry').append(`<option value='`+countryid+`' selected>`+country+`</option>`);
    $('#bankcover').attr('src', cover);
    $('#BankUpdate').modal("show");
})
