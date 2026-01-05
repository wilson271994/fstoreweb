

///**###########################################"Gestion des bannière ################################## */

/** Recherche de la liste */
$("#searchbanner").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterbanner tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

$("#addbanner").on("click", function(e){
    e.preventDefault();
    $("#bannerCreation").modal("show");
})

$(".closeaddbanner").on("click", function(e){
    e.preventDefault();
    $("#bannerCreation").modal("hide");
})

$(".closeupdatebanner").on("click", function(e){
    e.preventDefault();
    $("#bannerUpdate").modal("hide");
})


/**bannère mis a jour */
$(".updatebanner").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var title = $(this).data('title');
    var link = $(this).data('link');
    var isexternal = $(this).data('isexternal');
    var typelink = '';
    if(isexternal === 'True'){
        typelink = `<option value="True" selected>Externe</option>`
    }else{
        typelink = `<option value="False" selected>Interne</option>`
    }
    var cover = $(this).data('cover');
    $('#bannerid').val(id);
    $('#bannertitle').val(title);
    $('#bannerlink').val(link);
    $('#bannerlinktype').prepend(typelink);
    $('.imagetoupdate').attr('src', cover);
    $('#bannerUpdate').modal("show");
})

function bannerStatus(data){
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

///**###########################################"Gestion des sponsorings################################## */
$("#addsponsoring").on("click", function(e){
    e.preventDefault();
    $("#sponsoringCreation").modal("show");
})

$(".closeaddsponsoring").on("click", function(e){
    e.preventDefault();
    $("#sponsoringCreation").modal("hide");
})

$(".closeupdatesponsoring").on("click", function(e){
    e.preventDefault();
    $("#sponsoringUpdate").modal("hide");
})


/**administrateur mis a jour */
$(".updatesponsoring").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var product = `<option value="`+$(this).data('productid')+`" selected>`+$(this).data('product')+`</option>`
    var store = `<option value="`+$(this).data('storeid')+`" selected>`+$(this).data('store')+`</option>`
    var booking = `<option value="`+$(this).data('bookingid')+`" selected>`+$(this).data('booking')+`</option>`
    var start_date = $(this).data('startdate');
    var end_date = $(this).data('enddate');
    $('#sponsoringid').val(id);
    $('#sponsoringstartdate').val(start_date);
    $('#sponsoringenddate').val(end_date);
    $('#sponsoringstore').prepend(store);
    $('#sponsoringproduct').prepend(product);
    $('#sponsoringbooking').prepend(booking);
    $('#sponsoringUpdate').modal("show");
})

$('.selectedseller').on('change', function(){
    var storeid = $('.selectedseller').find(":selected").val();
    var url = $('.paramsgetproduct').data('url');

    getProduct(storeid, url);
})

/**Get Product From Store */
function getProduct(storeid, url){
    $.ajax({    
        type: 'post',
        url: url,
        data: 'storeid='+storeid,
        datatype: 'json',
        beforeSend: function () {
            $(document.body).css({'cursor' : 'wait'});
            $(this).find('*').prop('disabled', true);
        },
        success: function (json) {
            $('.productidvalue').empty();
            if (json.status === 200){
                if(json.results){
                    var data = json.results;
                    for(i=0; data.length > i; i++){
                        $('.productidvalue').prepend(
                            `<option value='`+data[i].id+`'>`+data[i].name+`</option>`
                        )
                    }
                }
            }
        },
        complete: function () {
            $(document.body).css({'cursor' : 'default'});
            $(this).find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
}

///**###########################################"Gestion des Booking ################################## */

/** Recherche de la liste */
$("#searchsponsoringbooking").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtersponsoringbooking tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

$("#addsponsoringbooking").on("click", function(e){
    e.preventDefault();
    $("#sponsoringbookingCreation").modal("show");
})

$(".closeaddsponsoringbooking").on("click", function(e){
    e.preventDefault();
    $("#sponsoringbookingCreation").modal("hide");
})

$(".closeupdatesponsoringbooking").on("click", function(e){
    e.preventDefault();
    $("#sponsoringbookingUpdate").modal("hide");
})


/**Booking mis a jour */
$(".updatesponsoringbooking").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    var periode = $(this).data('periode');
    var code_zone = `<option value="`+$(this).data('codezoneid')+`" selected>`+$(this).data('codezone')+`</option>`
    var sponsoringprice = $(this).data('sponsoringprice');
    var finalprice = sponsoringprice.split(',')[0] + '.' + sponsoringprice.split(',').pop();
    $('#sponsoringbookingid').val(id);
    $('#sponsoringbookingname').val(name);
    $('#sponsoringbookingperiode').val(periode);
    $('#sponsoringbookingcodezone').prepend(code_zone);
    $('#sponsoringbookingprice').val(finalprice);
    $('#sponsoringbookingUpdate').modal("show");
})

///**###########################################"Gestion des Zones ################################## */

/** Recherche de la liste */
$("#searchsponsoringzone").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtersponsoringzone tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

$("#addsponsoringzone").on("click", function(e){
    e.preventDefault();
    $("#sponsoringzoneCreation").modal("show");
})

$(".closeaddsponsoringzone").on("click", function(e){
    e.preventDefault();
    $("#sponsoringzoneCreation").modal("hide");
})

$(".closeupdatesponsoringzone").on("click", function(e){
    e.preventDefault();
    $("#sponsoringzoneUpdate").modal("hide");
})


/**zone mis a jour */
$(".updatesponsoringzone").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var name = $(this).data('name');
    var code = $(this).data('codezone');
    $('#sponsoringzoneid').val(id);
    $('#sponsoringzonename').val(name);
    $('#sponsoringzonecode').val(code);
    $('#sponsoringzoneUpdate').modal("show");
})
