/** Recherche dans la liste list */
$("#searchuser").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filteruser tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

$(document).ready(function(){
    $('.infoenterprise').css('display', 'none');
    $('.infodistributor').css('display', 'none');
})

$('#type_user').on('change', function(e){
    e.preventDefault();
    var type_user = $('#type_user').find(":selected").val();
    if(type_user === 'seller'){
        $('.infoenterprise').css('display', 'block');
    }else{
        $('.infoenterprise').css('display', 'none');
    }

    if(type_user ===  'distributor'){
        $('.infodistributor').css('display', 'block');
    }else{
        $('.infodistributor').css('display', 'none');
    }
})

/**Users creation */
$("#adduser").on("click", function(e){
    e.preventDefault();
    $("#userCreation").modal("show");
})

$(".closeadduser").on("click", function(e){
    e.preventDefault();
    $("#userCreation").modal("hide");
})
$(".closeupdateuser").on("click", function(e){
    e.preventDefault();
    $("#userUpdate").modal("hide");
})

/**administrateur detail */
$(".detailadmin").on("click", function(e){
    e.preventDefault();
    var email = $(this).data('email');
    var phone = $(this).data('phone');
    var pp = $(this).data('pp');
    $('#emailadmin').text(email);
    $('#phoneadmin').text(phone);
    $('#phototoupdate').attr('src', pp);
    $('#adminDetail').modal("show");
})


/**administrateur mis a jour */
$(".updateuser").on("click", function(e){
    e.preventDefault();
    var id                  = $(this).data('id');
    var iduser              = $(this).data('userid');
    var firstname           = $(this).data('firstname');
    var lastname            = $(this).data('lastname');
    var ownersexe           = $(this).data('ownersexe');
    var ownerbithday        = $(this).data('ownerbithday');
    var email               = $(this).data('email');
    var phone               = $(this).data('phone');
    var address             = $(this).data('address');
    var description         = $(this).data('description');
    var codepostal          = $(this).data('codepostal');
    var countryname         = $(this).data('countryname');
    var countryid           = $(this).data('countryid');
    var city                = $(this).data('city');
    var cityid              = $(this).data('cityid');
    var pp                  = $(this).data('pp');
    var identification      = $(this).data('identification');
    var type_identification = $(this).data('typeidentification');
    var identificationID    = $(this).data('identificationid');
    var documentrc          = $(this).data('documentrc');
    var nametypeNID         = '';
    if(type_identification === 1){
        nametypeNID = 'CNI'
    }else{
        nametypeNID = 'PassePort'
    }

    const delta = quill.clipboard.convert(description)
    quill.setContents(delta, 'silent')
    $('.post-content-update').val(description);

    var storenumberrc = $(this).data('storenumberrc');
    var resaonsocial = $(this).data('resaonsocial');
    var googlemap = $(this).data('googlemap');
    var typeuser = $(this).data('typeuser');
    var optionsexe = `<option value="`+ownersexe+`" selected>`+ownersexe+`</option>`;
    var optioncountry = `<option value="`+countryid+`" selected>`+countryname+`</option>`;
    var optioncity = `<option value="`+cityid+`" selected>`+city+`</option>`;
    var optionniddoc = `<option value="`+type_identification+`" selected>`+nametypeNID+`</option>`;
    if(typeuser == 'store'){
        $('.infoenterprise').css('display', 'block');
        $('#goodlemapid1').val(googlemap);
    }else{
        $('.infoenterprise').css('display', 'none');
    }
    if(typeuser == 'distributor'){
        $('.infodistributor').css('display', 'block');
        $('#goodlemapid2').val(googlemap);
    }else{
        $('.infodistributor').css('display', 'none');
    }
    $('#personid').val(id);
    $('#adminownerfirstnameid').val(firstname);
    $('#adminownerlastnameid').val(lastname);
    $('#adminownersexeid').append(optionsexe);    
    $('.admincountry').append(optioncountry);
    $('.cityuseridvalue').append(optioncity);
    $('.typenidcart').append(optionniddoc);
    $('#adminownerbirthdayid').val(ownerbithday);
    $('#adminemailid').val(email);
    $('#adminphoneid').val(phone);
    $('#adminaddressid').val(address);
    $('#admincodepostalid').val(codepostal);
    $('#descriptionid').val(description);
    $('#rcnumberid').val(storenumberrc);
    $('#resaonsocialid').val(resaonsocial);
    $('#phototoupdate').attr('src', pp);
    $('#nidtoupdate').attr('value', identification);
    $('#typenid').val(type_identification);
    $('#useridentificationID').val(identificationID);
    $('#rctoupdate').attr('value', documentrc);
    $('#userUpdate').modal("show");
})

/**mot de passe mis a jour */ 
$(".resetpassuser").on("click", function(e){
    e.preventDefault();
    var email = $(this).data('email');
    $('#userinfo').val(email);
    $('#userPassword').modal("show");
})
$(".closeupdatepass").on("click", function(e){
    e.preventDefault();
    $("#userPassword").modal("hide");
})

function userStatus(data){
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

$('.selectedcountry3').on('change', function(){
    var countryid = $('.selectedcountry3').find(":selected").val();
    var url = $('.paramsgetcities').data('url');
    var token = $('.paramsgetcities').data('token');
    getCity(countryid, url, token);
})

function getUserCity(country, url, token){
    $.ajax({    
        type: 'post',
        url: url,
        data: {
            country:country,
            csrfmiddlewaretoken:token
        },
        datatype: 'json',
        beforeSend: function () {
            $(document.body).css({'cursor' : 'wait'});
            $(this).find('*').prop('disabled', true);
        },
        success: function (json) {
            $('.cityuseridvalue').empty();
            if (json.status == 200){
                if(json.result){
                    var data = json.result;
                    for(i=0; data.length > i; i++){
                        $('.cityuseridvalue').append(
                            `<option value='`+data[i].cityid+`'>`+data[i].cityname+`</option>`
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

