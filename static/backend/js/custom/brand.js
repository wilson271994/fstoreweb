/** gestion des tables list */
$("#searchbrand").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterbrand tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**marques creation */
$("#addbrand").on("click", function(e){
    e.preventDefault();
    $("#brandCreation").modal("show");
})

$(".closeaddbrand").on("click", function(e){
    e.preventDefault();
    $("#brandCreation").modal("hide");
})
$(".closeupdatebrand").on("click", function(e){
    e.preventDefault();
    $("#brandUpdate").modal("hide");
})

/**administrateur mis a jour */
$(".updateBrand").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');    
    var name = $(this).data('name');
    var seller = $(this).data('seller');
    var sellerid = $(this).data('sellerid');
    var sellerselect = `<option value="`+sellerid+`" selected>`+seller+`</option>`;
    $('#sellerselectid').append(sellerselect);
    $('#brandid').val(id);
    $('#brandnameid').val(name);
    $('#brandUpdate').modal("show");
})

function brandStatus(data){
    var url = data.getAttribute('data-url');
    var token = data.getAttribute('data-token');
    var id = data.getAttribute('data-id');
    $.ajax({    
        type: 'post',
        url: url,
        data: 'id='+id+'&csrfmiddlewaretoken='+token,
        datatype: 'json',
        beforeSend: function () {
            $(document.body).css({'cursor' : 'wait'});
            $(this).find('*').prop('disabled', true);
        },
        success: function (json) {
            if (json.status == 200){
                toastr.success(json.message);
                window.location.reload();
            }else{
                toastr.error(json.message);
            }
        },
        complete: function () {
            $(document.body).css({'cursor' : 'default'});
            $(this).find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
}
