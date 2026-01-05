/**Script Kops Market Auth */

/**Login Script */
$(document).on('submit', '#LoginSubmit', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
    var valBtn = $('.adminloginbtn').text();
    $.ajax({    
        type: 'post',
        url: url,
        data: data,
        contentType: false,
        processData: false,
        datatype: 'json',
        beforeSend: function () {
            $('.adminloginbtn').text('en cours...').prop('disabled',true);
            $(document.body).css({'cursor' : 'wait'});
            form.find('*').prop('disabled', true);
        },
        success: function (json) {
            if (json.status === 200){
                toastr.success(json.message);
                window.location.assign(json.url);
            }else{
                toastr.error(json.message);
            }
        },
        complete: function () {
            $('.adminloginbtn').text(valBtn).prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

