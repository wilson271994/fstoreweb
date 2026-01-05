/**#########################################################################Category Grant Child ###############################################"" */

/** gestion des tables list */
$("#searchgrantchildcategory").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtergrantchildcategory tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**grantchildcategorys creation */
$("#addgrantchildcategory").on("click", function(e){
    e.preventDefault();
    $("#grantchildcategoryCreation").modal("show");
})

$(".closeaddgrantchildcategory").on("click", function(e){
    e.preventDefault();
    $("#grantchildcategoryCreation").modal("hide");
})


/**administrateur mis a jour */
$(".updategrantchildcategory").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    $('#grandchildid').val(id);
    $('#grandchildname').val(name);
    $('#grantchildcategoryUpdate').modal("show");
})


$(".closeupdategrantchildcategory").on("click", function(e){
    e.preventDefault();
    $("#grantchildcategoryUpdate").modal("hide");
})


function grantchildcategoryStatus(data){
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





/**##########################################################Category Child ##################################################### */

/** gestion des tables list */
$("#searchchildcategory").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterchildcategory tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**childcategorys creation */
$("#addchildcategory").on("click", function(e){
    e.preventDefault();
    $("#childcategoryCreation").modal("show");
})

$(".closeaddchildcategory").on("click", function(e){
    e.preventDefault();
    $("#childcategoryCreation").modal("hide");
})
$(".closeupdatechildcategory").on("click", function(e){
    e.preventDefault();
    $("#childcategoryUpdate").modal("hide");
})

/**administrateur mis a jour */
$(".updatechildcategory").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    $('#childid').val(id);
    $('#childname').val(name);
    $('#childcategoryUpdate').modal("show");
})

function childcategoryStatus(data){
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

/**####################################################Category Parent ########################################"" */

/** gestion des tables list */
$("#searchparentcategory").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterparentcategory tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**parentcategorys creation */
$("#addparentcategory").on("click", function(e){
    e.preventDefault();
    $("#parentcategoryCreation").modal("show");
})

$(".closeaddparentcategory").on("click", function(e){
    e.preventDefault();
    $("#parentcategoryCreation").modal("hide");
})
$(".closeupdateparentcategory").on("click", function(e){
    e.preventDefault();
    $("#parentcategoryUpdate").modal("hide");
})

/**administrateur mis a jour */
$(".updateparentcategory").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    $('#parentid').val(id);
    $('#parentname').val(name);
    $('#parentcategoryUpdate').modal("show");
})

function parentcategoryStatus(data){
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