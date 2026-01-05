/** gestion des tables list */
$("#searchdevise").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterdevise tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**devises creation */
$("#adddevise").on("click", function(e){
    e.preventDefault();
    $("#deviseCreation").modal("show");
})

$(".closeadddevise").on("click", function(e){
    e.preventDefault();
    $("#deviseCreation").modal("hide");
})


/**administrateur mis a jour */
$(".updatedevise").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var deviseorigin = $(this).data('deviseorigin');
    var exchangerate = $(this).data('exchangerate');
    var devisedestination = $(this).data('devisedestination');
    $('#deviseid').val(id);
    $('#deviseoriginid').val(deviseorigin);
    $('#devisedestinationid').val(devisedestination);
    $('#deviseexchangerateid').val(exchangerate);
    $('#deviseUpdate').modal("show");
})


$(".closeupdatedevise").on("click", function(e){
    e.preventDefault();
    $("#deviseUpdate").modal("hide");
})

function deviseActive(data){
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

function deviseStatus(data){
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

/**Update Devise  */
$("#updatedevise").on("click", function(e){
    e.preventDefault();
    var url = $(this).data('url');
    var token = $(this).data('data-token');
    $.get("https://api.exchangeratesapi.io/v1/latest?access_key=a243efa76145de931fa9ef23adc504ed", function(data){
        if(data.success){
            var base = data.base;
            for (const [key, value] of Object.entries(data.rates)){
                $.ajax({
                    url : url,
                    type : "post",
                    data : "currency="+ `${key}` + "&exchangeRate=" + `${value}` + "&basecurrency="+base, 
                    dataType : "json",
                    beforeSend : function () {},
                    success : function (json) {
                        if(json.status == true ){
                            window.location.reload();
                        }
                    },
                    complete : function () {},
                    error : function (jqXHR, textStatus, errorThrown) {}
                })
            }
        }
    });
})
