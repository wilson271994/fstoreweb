/** gestion des tables list */
$("#searchproduct").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterproduct tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1) 
    });
});

/**products creation */
$("#addproduct").on("click", function(e){
    e.preventDefault();
    $("#productCreation").modal("show");
})

$("#addproduct2").on("click", function(e){
    e.preventDefault();
    $("#productCreation").modal("show");
})

const newPublish = () => {
    $('.chatmessenger').css('display', 'none');
    $('.fixed.sticky-header').css('margin-top', '-54px');
    $("#productCreation").modal("show");
}

const closePublishingModal = () => {
    $('.chatmessenger').css('display', 'block');
}

/**administrateur mis a jour */
$(".updateproductmodal").on("click", function(e){
    e.preventDefault();
    console.log('tetetetetetetet')
    var id = $(this).data('id');
    var name = $(this).data('name');
    var description = $(this).data('description');
    var price = $(this).data('price');
    var discount = $(this).data('discount');
    var quantity = $(this).data('quantity');
    var weigth = $(this).data('weigth');
    var height = $(this).data('height');
    var width = $(this).data('width');
    var depth = $(this).data('depth');
    var marque = $(this).data('marque');
    var marqueid = $(this).data('marqueid');
    var optionmarque = `<option value="`+marqueid+`" selected>`+marque+`</option>`;
    var provider = $(this).data('provider');
    var providerid = $(this).data('providerid');
    var optionprovider = `<option value="`+providerid+`" selected>`+provider+`</option>`;
    var companycom = $(this).data('companycom');

    const delta = quill.clipboard.convert(description)
    quill.setContents(delta, 'silent')
    $('.post-content-update').val(description);

    $('#productid').val(id);
    $('#productname').val(name);
    $('#productprice').val(price);
    $('#productdiscount').val(discount);
    $('#productquantity').val(quantity);
    $('#productweigth').val(weigth);
    $('#productheight').val(height);
    $('#productwidth').val(width);
    $('#productdepth').val(depth);
    $('#productmarque').append(optionmarque);
    $('#productprovider').append(optionprovider);
    $('#productcompcom').val(companycom);
    $('#productUpdate').modal("show");
})

/**Manage Category */
$("#id_parent").change(function(){
    $("#id_child").html(`<option value="" selected="">Choisir la sous-catégorie</option>`);
    $("#id_grant_child").html(`<option value="" selected="">Choisir la sous sous-catégorie</option>`);
    var parent = $( "#id_parent option:selected" ).val();
    var url = $(this).data('url');
    var token = $(this).data('token');
    // Ajax request to get all subcategorie
    $.ajax({
        url:url,
        type:"post",
        data: {
            parent_value: parent,
            csrfmiddlewaretoken: token
        },
        dataType:"json",
        success: function(data){
            if(data.status === 200){
                $("#id_child").append(data.sub_cat)
            }
        },
    })
});

$("#id_child").change(function(){
    $("#id_grant_child").html(`<option value="" selected="">Choisir la sous sous-catégorie</option>`);
    var child = $( "#id_child option:selected" ).val();
    var url = $(this).data('url');
    var token = $(this).data('token');
    // Ajax request to get all subcategorie
    $.ajax({
        url:url,
        type:"post",
        data: {
            child_value: child,
            csrfmiddlewaretoken: token
        },
        dataType:"json",
        success: function(data){
            if(data.status === 200){
                $("#id_grant_child").append(data.grant_cat)
            }
        },
    })
});

/**Manage Category */
$("#id_parent_update").change(function(){
    $("#id_child_update").html(`<option value="" selected="">Choisir la sous-catégorie</option>`);
    $("#id_grant_child_update").html(`<option value="" selected="">Choisir la sous sous-catégorie</option>`);
    var parent = $( "#id_parent_update option:selected" ).val();
    url = $(this).data('url');
    
    // Ajax request to get all subcategorie
    $.ajax({
        url:url,
        type:"post",
        data:"parent_value="+parent,
        dataType:"json",
        success: function(data){
            if(data.status === 200){
                $("#id_child_update").append(data.sub_cat)
            }
        },
    })
});

$("#id_child_update").change(function(){
    $("#id_grant_child_update").html(`<option value="" selected="">Choisir la sous sous-catégorie</option>`);
    var child = $( "#id_child_update option:selected" ).val();
    url = $(this).data('url');
    // Ajax request to get all subcategorie
    $.ajax({
        url:url,
        type:"post",
        data:"child_value="+child,
        dataType:"json",
        success: function(data){
            if(data.status === 200){
                $("#id_grant_child_update").append(data.grant_cat)
            }
        },
    })
});

/**
 * ##########################################################################################
 * ############################## MANAGE SPONSORiNG #######################################
 * ##########################################################################################
 */

$(".addsponsoring").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var person = $(this).data('person');
    $("#sponsoringproduct").val(id);
    $("#sponsoringperson").val(person);
    $("#sponsoringCreation").modal("show");
})

/**
 * Manage Booking
 */
const handleBooking = (attribute) => {
    const url = attribute.getAttribute('url');
    const token = attribute.getAttribute('token');
    var current_balance = attribute.getAttribute('wallet');
    const id    = attribute.value;
    $('#pricebooking').html('');
    const data = {
        id                          : id,
        csrfmiddlewaretoken         : token
    }
    $.ajax({    
        type: 'post',
        url: url,
        data: data,
        datatype: 'json',
        beforeSend: function () {
            $(document.body).css({'cursor' : 'wait'});
        },
        success: function (json) {
            if (json.status === 200){
                const result = json.result;
                const id    = result.id;
                const price = result.price;
                const periode   = result.periode;
                const name      = result.name;
                var ref_current_balabce = current_balance.split(',')[0]+'.'+current_balance.split(',').pop();
                var html_content = `Vous avez choisie le bouquet <span id="namebooking">`+name+`</span> vous coûtera <span id="sponsoringprice">`+price+` FR CFA</span> sur une période de <span id="sponsoringperiode">`+periode+` heures</span>`
                $('#pricebooking').append(html_content);
                if(Number(ref_current_balabce) < Number(price)){
                    $('#submitsponsoring').attr('disabled', true);
                    $('.error_message').text('Votre solde est insuffisant pour ce forfait veuillez recharger votre portefeuille')
                }else{
                    $('.error_message').text('');
                    $('#submitsponsoring').attr('disabled', false);
                }
            }else{
                toastr.error(json.message);
            }
        },
        complete: function () {
            $(document.body).css({'cursor' : 'default'});
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
}


/**
 * ##########################################################################################
 * ############################## MANAGE PRESENTATION #######################################
 * ##########################################################################################
 */
//**Manage Presentation */
$(".addpresentation").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    $("#productpresentationid").val(id);
    $("#presentationCreation").modal("show");
})

/**Update Presentation  */
$("#updatepresentation").on("click", function(e){
    e.preventDefault();
    var presentationid = $(this).data('presentationid');
    var presentation = $(this).data('presentation'); 
    var product = $(this).data('productid'); 

    const delta = quillpresentation.clipboard.convert(presentation)
    quillpresentation.setContents(delta, 'silent');
    $('#post-content-update').val(presentation);

    $("#presentationproductid").val(product);
    $("#presentationid").val(presentationid);
    $("#presentationUpdate").modal("show");
})

/**Create Presentation Request */
$(document).on('submit', '#createSubmitPresentation', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
    var valBtn = $('.createbtnpresentation').text();
    $.ajax({    
        type: 'post',
        url: url,
        data: data,
        contentType: false,
        processData: false, 
        datatype: 'json',
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            //Download progress
            xhr.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    progressElem.html(Math.round(percentComplete * 100) + "%");
                }
            }, false);
            return xhr;
        },
        beforeSend: function () {
            $('.createbtnpresentation').text('en cours...').prop('disabled',true);
            $(document.body).css({'cursor' : 'wait'});
            form.find('*').prop('disabled', true);
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
            $('.createbtnpresentation').empty();
            $('.createbtnpresentation').text(valBtn).prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

/**Update Presentation Request */
$(document).on('submit', '#updateSubmitPresentation', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
    var valBtn = $('.updatebtnpresentation').text();
    $.ajax({    
        type: 'post',
        url: url,
        data: data,
        contentType: false,
        processData: false,
        datatype: 'json', 
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            //Download progress
            xhr.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    progressElem.html(Math.round(percentComplete * 100) + "%");
                }
            }, false);
            return xhr;
        },
        beforeSend: function () {
            $('.updatebtnpresentation').text('en cours...').prop('disabled',true);
            $(document.body).css({'cursor' : 'wait'});
            form.find('*').prop('disabled', true);
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
            $('.updatebtnpresentation').empty();
            $('.updatebtnpresentation').text(valBtn).prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

/**
 * ####################################################################################
 * ""################################## MANAGE ATTRIBUTES #############################
 * #################################################################################### 
 * */
$(".addattribut").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    $("#productattributid").val(id);
    $("#attributCreation").modal("show");
})

$(".closeaddattribut").on("click", function(e){
    e.preventDefault();
    $("#attributCreation").modal("hide");
})

$(".updateattribut").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('attribut');
    var sizeselect = eval($(this).data('sizeselect'))
    var materialselect = eval($(this).data('materialselect'))
    var colorselect = eval($(this).data('colorselect'))
    var allsize = $(this).data('allsize')
    var allmaterial = $(this).data('allmaterial')
    var allcolor = $(this).data('allcolor')
    for(i=0; i < sizeselect.length ; i++){
        console.log(sizeselect[0])
        $("#selectsize").append('<option value="'+sizeselect[i].id+'" selected>'+sizeselect[i].name+'</option>');
    }
    $("#selectsize").selectpicker("refresh");
    for(i=0; i < materialselect.length ; i++){
        console.log(materialselect[0])
        $("#selectmaterial").append('<option value="'+materialselect[i].id+'" selected>'+materialselect[i].name+'</option>');
    }
    $("#selectmaterial").selectpicker("refresh");
    for(i=0; i < colorselect.length ; i++){
        console.log(colorselect[0])
        $("#selectcolor").append('<option value="'+colorselect[i].id+'" selected>'+colorselect[i].name+'</option>');
    }
    $("#selectcolor").selectpicker("refresh");
    $("#attributid").val(id);
    $("#attributUpdate").modal("show");
})

$(".closeupdateattribut").on("click", function(e){
    e.preventDefault();
    $("#attributUpdate").modal("hide");
})

/**Create Attribute Request */
$(document).on('submit', '#createSubmitAttribute', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
    var valBtn = $('.createbtnattribute').text();
    $.ajax({    
        type: 'post',
        url: url,
        data: data,
        contentType: false,
        processData: false, 
        datatype: 'json',
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            //Download progress
            xhr.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    progressElem.html(Math.round(percentComplete * 100) + "%");
                }
            }, false);
            return xhr;
        },
        beforeSend: function () {
            $('.createbtnattribute').text('en cours...').prop('disabled',true);
            $(document.body).css({'cursor' : 'wait'});
            form.find('*').prop('disabled', true);
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
            $('.createbtnattribute').empty();
            $('.createbtnattribute').text(valBtn).prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

/**Update Attribute Request */
$(document).on('submit', '#updateSubmitAttribute', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
    var valBtn = $('.updatebtnattribute').text();
    $.ajax({    
        type: 'post',
        url: url,
        data: data,
        contentType: false,
        processData: false,
        datatype: 'json', 
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            //Download progress
            xhr.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    progressElem.html(Math.round(percentComplete * 100) + "%");
                }
            }, false);
            return xhr;
        },
        beforeSend: function () {
            $('.updatebtnattribute').text('en cours...').prop('disabled',true);
            $(document.body).css({'cursor' : 'wait'});
            form.find('*').prop('disabled', true);
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
            $('.updatebtnattribute').empty();
            $('.updatebtnattribute').text(valBtn).prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

/**""##################################MANAGE PROMOTIONS FLASH############################### */
$(".addflash").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    $("#productflashid").val(id);
    $("#addFlashProduct").modal("show");
})

$(".closeaddflash").on("click", function(e){
    e.preventDefault();
    $("#addFlashProduct").modal("hide");
})

/**Create Script */
$(document).on('submit', '#createSubmitFlash', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
    var valBtn = $('.createbtnflash').text();
    $.ajax({    
        type: 'post',
        url: url,
        data: data,
        contentType: false,
        processData: false, 
        datatype: 'json',
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            //Download progress
            xhr.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = evt.loaded / evt.total;
                    progressElem.html(Math.round(percentComplete * 100) + "%");
                }
            }, false);
            return xhr;
        },
        beforeSend: function () {
            $('.createbtnflash').text('en cours...').prop('disabled',true);
            $(document.body).css({'cursor' : 'wait'});
            form.find('*').prop('disabled', true);
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
            $('.createbtnflash').empty();
            $('.createbtnflash').text(valBtn).prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

/** Supprimer le produit de la vente flash */
$('.deleteflash').on('click', function(){
    var url = $(this).data('url');
    var id = $(this).data('id');
    var token = $(this).data('token');
    Swal.fire({
        title: "Êtes vous sûr?",
        text: "cet Article sera supprimer de la vente flash!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#00457E",
        confirmButtonText: "Oui",
        cancelButtonText: "Non",
        preConfirm: () => {
            deleteflash_function(url, id, token);
        },
    })
    function deleteflash_function(url, id, token){
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
})

/**
 * #################################################################################################################
 *############################################### Manage Upload Image ##############################################
 ###################################################################################################################
 */
const readImageFrontURL = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preloaderfrontimgid').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
const readImageBackURL = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preloaderbackimgid').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
const readImageLeftURL = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preloaderleftimgid').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
const readImageRightURL = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preloaderrightimgid').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
const readImageTopURL = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preloadertopimgid').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
const readImageBottomURL = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preloaderbottomimgid').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

const toggleImageFront = () => {
    $('#productimagefront').click();
}
$('#productimagefront').on('change', function(e){
    $('#preloaderfrontimgid').css('display', 'block');
    $('#preloaderfront').html('');
    readImageFrontURL(this)
})

const toggleImageBack = () => {
    $('#productimageback').click();
}
$('#productimageback').on('change', function(e){
    $('#preloaderbackimgid').css('display', 'block');
    $('#preloaderback').html('');
    readImageBackURL(this)
})

const toggleImageLeft = () => {
    $('#productimageleft').click();
}
$('#productimageleft').on('change', function(e){
    $('#preloaderleftimgid').css('display', 'block');
    $('#preloaderleft').html('');
    readImageLeftURL(this)
})

const toggleImageRight = () => {
    $('#productimageright').click();
}
$('#productimageright').on('change', function(e){
    $('#preloaderrightimgid').css('display', 'block');
    $('#preloaderright').html('');
    readImageRightURL(this)
})

const toggleImageTop = () => {
    $('#productimagetop').click();
}
$('#productimagetop').on('change', function(e){
    $('#preloadertopimgid').css('display', 'block');
    $('#preloadertop').html('');
    readImageTopURL(this)
})

const toggleImageBottom = () => {
    $('#productimagebottom').click();
}
$('#productimagebottom').on('change', function(e){
    $('#preloaderbottomimgid').css('display', 'block');
    $('#preloaderbottom').html('');
    readImageBottomURL(this)
})








