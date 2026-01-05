/** Recherche de la liste */
$("#searchcolor").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtercolor tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


///**###########################################"Gestion des couleurs################################## */
$("#addcolor").on("click", function(e){
    e.preventDefault();
    $("#colorCreation").modal("show");
})

$(".closeaddcolor").on("click", function(e){
    e.preventDefault();
    $("#colorCreation").modal("hide");
})

$(".closeupdatecolor").on("click", function(e){
    e.preventDefault();
    $("#colorUpdate").modal("hide");
})


/**administrateur mis a jour */
$(".updatecolor").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    var code = $(this).data('code');
    $('#colorid').val(id);
    $('#colornameid').val(name);
    $('#colorcodeid').val(code);
    $('#colorUpdate').modal("show");
})

function colorStatus(data){
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

///**###########################################"Gestion des tailles################################## */
$("#addsize").on("click", function(e){
    e.preventDefault();
    $("#sizeCreation").modal("show");
})

$(".closeaddsize").on("click", function(e){
    e.preventDefault();
    $("#sizeCreation").modal("hide");
})

$(".closeupdatesize").on("click", function(e){
    e.preventDefault();
    $("#sizeUpdate").modal("hide");
})


/**administrateur mis a jour */
$(".updatesize").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    $('#sizeid').val(id);
    $('#sizenameid').val(name);
    $('#sizeUpdate').modal("show");
})

function sizeStatus(data){
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

///**###########################################"Gestion des matériaux################################## */
$("#addmaterial").on("click", function(e){
    e.preventDefault();
    $("#materialCreation").modal("show");
})

$(".closeaddmaterial").on("click", function(e){
    e.preventDefault();
    $("#materialCreation").modal("hide");
})

$(".closeupdatematerial").on("click", function(e){
    e.preventDefault();
    $("#materialUpdate").modal("hide");
})


/**administrateur mis a jour */
$(".updatematerial").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    var description = $(this).data('description');
    $('#materialid').val(id);
    $('#materialnameid').val(name);
    $('#materialdescriptionid').val(description);
    $('#materialUpdate').modal("show");
})

function materialStatus(data){
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