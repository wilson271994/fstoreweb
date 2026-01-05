/** Recherche dans la liste list */
$("#searchcustomer").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filtercustomer tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});


/**Customer detail */
$(".detailcustomer").on("click", function(e){
    e.preventDefault();
    var email = $(this).data('email');
    var phone = $(this).data('phone');
    var pp = $(this).data('pp');
    $('#emailcustomer').text(email);
    $('#phonecustomer').text(phone);
    $('#phototoupdate').attr('src', pp);
    $('#customerDetail').modal("show");
})


/**customer update */
$(".updatecustomer").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var firstname = $(this).data('firstname');
    var lastname = $(this).data('lastname');
    var ownersexe = $(this).data('sexe');
    var ownerbithday = $(this).data('bithday');
    var email = $(this).data('email');
    var phone = $(this).data('phone');
    var address = $(this).data('address');
    var countryname = $(this).data('countryname');
    var countryid = $(this).data('countryid');
    var city = $(this).data('city');
    var pp = $(this).data('pp');
    var optionsexe = `<option value="`+ownersexe+`" selected>`+ownersexe+`</option>`;
    var optioncountry = `<option value="`+countryid+`" selected>`+countryname+`</option>`;
    var optioncity = `<option value="`+city+`" selected>`+city+`</option>`;
    $('#individualid').val(id);
    $('#customerfirstnameid').val(firstname);
    $('#customerlastnameid').val(lastname);
    $('#customersexeid').append(optionsexe);    
    $('#customercountryid').append(optioncountry);
    $('.cityidvalue').append(optioncity);
    $('#customerbirthdayid').val(ownerbithday);
    $('#customeremailid').val(email);
    $('#customerphoneid').val(phone);
    $('#customeraddressid').val(address);
    $('#phototoupdate').attr('src', pp);
    $('#customerUpdate').modal("show");
})

$(".closeupdatecustomer").on("click", function(e){
    e.preventDefault();
    $("#customerUpdate").modal("hide");
})

/**mot de passe mis a jour */
$(".resetpasscustomer").on("click", function(e){
    e.preventDefault();
    var email = $(this).data('email');
    $('#customerinfo').val(email);
    $('#customerPassword').modal("show");
})

$(".closeupdatepass").on("click", function(e){
    e.preventDefault();
    $("#customerPassword").modal("hide");
})

function customerStatus(data){
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
