/** Recherche dans la liste list */
$("#searchtraficcustomer").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtertraficcustomer tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


function traficcustomerStatus(data){
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
