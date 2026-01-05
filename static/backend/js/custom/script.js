/*--------------------------------------------------------------------------------------------
		Window Load START
---------------------------------------------------------------------------------------------*/
jQuery(window).on('load', function () {	
    page_loader();
});

/**Page loader  */
function page_loader() {
    $('.loading-area').fadeOut(1000)
};

/** Gestion de la Deconnexion */
$('.Logout').on('click', function(){
    var url = $(this).data('url');
    Swal.fire({
        title                   : "Êtes vous sûr?",
        text                    : "Vous serez déconnecter du système!",
        icon                    : "warning",
        showCancelButton        : true,
        confirmButtonColor      : "#000",
        confirmButtonText       : "Oui",
        cancelButtonText        : "Non",
        preConfirm: () => {
            logout_function(url);
        },
    })
    function logout_function(url){
        window.location.assign(url)
    }
})

/**Create Script */
$(document).on('submit', '.createSubmit', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
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
            $('.createbtn').text('en cours...').prop('disabled',true);
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
            $('.createbtn').text('Sauvegarder').prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

/**Update Script */
$(document).on('submit', '.updateSubmit', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
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
            $('.updatebtn').text('en cours...').prop('disabled',true);
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
            $('.updatebtn').text('Sauvegarder').prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

/** Gestion des suppression */
$('.deleteSubmit').on('click',function(){ 
    var url = $(this).data('url');
    var id = $(this).data('id');
    var token = $(this).data('token');
    var type = $(this).data('type');
    var message = $(this).data('message');
    Swal.fire({
        title                   : "Êtes-vous sûr?",
        text                    : message,
        icon                    : type,
        showCancelButton        : true,
        confirmButtonColor      : "#4675e3",
        confirmButtonText       : "Oui",
        cancelButtonText        : "Non",
        preConfirm: () => {
            delete_function(url, id, token);
        },
    })
    function delete_function(url, id, token){
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
 * Global Status Form
 */
$('.statusForm').on('click', function(){
    var url = $(this).data('url');
    var id = $(this).data('id');
    var token = $(this).data('token');
    var message = $(this).data('message');
    var type = $(this).data('type');
    Swal.fire({
        title               : "Êtes-vous sûr?",
        text                : message,
        icon                : type,
        showCancelButton    : true,
        confirmButtonColor  : "#4675e3",
        confirmButtonText       : "Oui",
        cancelButtonText        : "Non",
        preConfirm: () => {
            action_function(url, id, token);
        },
    })
    function action_function(url, id, token){
        $.ajax({    
            type: 'post',
            url: url,
            data: {
                id: id,
                csrfmiddlewaretoken: token
            },
            dataType: 'json',
            beforeSend: function () {
                $(document.body).css({'cursor' : 'wait'});
                $(this).find('*').prop('disabled', true);
            },
            success: function (json) {
                if (json.status == 200){
                    setTimeout(toastr.success(json.message), 5000);
                    window.location.reload();
                }else{
                    toastr.error(json.message)
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
 * Global Validation Form
 */
$('.validationForm').on('click', function(){
    var url = $(this).data('url');
    var id = $(this).data('id');
    var token = $(this).data('token');
    var message = $(this).data('message');
    var type = $(this).data('type');
    Swal.fire({
        title               : "Êtes-vous sûr?",
        text                : message,
        icon                : type,
        showCancelButton    : true,
        cancelButtonColor   : "#8d96b0",
        confirmButtonColor  : "#4675e3",
        confirmButtonText       : "Oui",
        cancelButtonText        : "Non",
        preConfirm: () => {
            action_function(url, id, token);
        },
    })
    function action_function(url, id, token){
        $.ajax({    
            type: 'post',
            url: url,
            data: {
                id: id,
                csrfmiddlewaretoken: token
            },
            dataType: 'json',
            beforeSend: function () {
                $(document.body).css({'cursor' : 'wait'});
                $(this).find('*').prop('disabled', true);
            },
            success: function (json) {
                if (json.status == 200){
                    setTimeout(toastr.success(json.message), 5000);
                    window.location.reload();
                }else{
                    toastr.error(json.message)
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
 

/**Username Updater */
function UsernameUpdater(email){
    $('.username').val(email);
}

$('.selectedcountry').on('change', function(){
    var countryid = $('.selectedcountry').find(":selected").val();
    var url = $('.paramsgetcities').data('url');
    var token = $('.paramsgetcities').data('token');
    getCity(countryid, url, token);
})

$('.selectedcountry2').on('change', function(){
    var countryid = $('.selectedcountry2').find(":selected").val();
    var url = $('.paramsgetcities').data('url');
    var token = $('.paramsgetcities').data('token');
    getCity(countryid, url, token);
})

/**Get City From Country */
function getCity(country, url, token){
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
            $('.cityidvalue').empty();
            if (json.status == 200){
                if(json.result){
                    var data = json.result;
                    for(i=0; data.length > i; i++){
                        $('.cityidvalue').append(
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

// Basic example
$(document).ready(function () {
    $('.table').DataTable({
      "pagingType": "simple_numbers"
    });
    $('.dataTables_length').addClass('bs-select');
});

/**Redirect Url */
function Redirect(data){
    const url = data.getAttribute('data-url')
    window.location.assign(url);
}

/**EDITOR QUILL */
var quill = {};
var quillvision = {};
var quillmission = {};
var quillpresentation = {};

$(document).ready(function(){
    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        ['blockquote', 'code-block'],
      
        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction
      
        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      
        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'font': [] }],
        [{ 'align': [] }],
    
        ['clean'],                                         // remove formatting button
        ['image'],
        ['link']
    ];
    
    quill = new Quill('.editor', {
    theme: 'snow',
    modules: { 
            toolbar: {
                container: toolbarOptions,
            }
        },
        imageHandler: imageHandler
    });

    quill = new Quill('.editorupdate', {
        theme: 'snow',
        modules: {
            toolbar: {
                container: toolbarOptions,
            }
        },
        imageHandler: imageHandler
    });

    quillvision = new Quill('.editorvision', {
        theme: 'snow',
        modules: { 
            toolbar: {
                container: toolbarOptions,
            }
        },
        imageHandler: imageHandler
    });

    quillmission = new Quill('.editormission', {
        theme: 'snow',
        modules: { 
            toolbar: {
                container: toolbarOptions,
            }
        },
        imageHandler: imageHandler
    });

    quillpresentation = new Quill('.editorpresentation', {
        theme: 'snow',
        modules: {
            toolbar: {
                container: toolbarOptions,
            }
        },
        imageHandler: imageHandler
    });

    quillpresentation = new Quill('.editorpresentationupdate', {
        theme: 'snow',
        modules: {
            toolbar: {
                container: toolbarOptions,
            }
        },
        imageHandler: imageHandler
    });

    function imageHandler(image, callback) {
        var data = new FormData();
        data.append('image', image);
    
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 200 && response.success) {
                callback(response.data.link);
            } else {
                var reader = new FileReader();
                reader.onload = function(e) {
                callback(e.target.result);
                };
                reader.readAsDataURL(image);
            }
            }
        }
        xhr.send(data);
    }
 
})

const postSubmission = function(){
    var editor = document.querySelector(".editor");
    var contentInput = document.querySelector(".post-content");
    contentInput.value = editor.innerHTML;
}

const postSubmissionUpdate = function(){
    var editor = document.querySelector(".editorupdate");
    var contentInput = document.querySelector(".post-content-update");
    contentInput.value = editor.innerHTML;
}

const postSubmissionPresentation = function(){
    var editor = document.querySelector(".editorpresentation");
    var contentInput = document.querySelector(".post-content-presentation");
    contentInput.value = editor.innerHTML;
}

const postSubmissionPresentationUpdate = function(){
    var editor = document.querySelector(".editorpresentationupdate");
    var contentInput = document.querySelector(".post-content-presentation-update");
    contentInput.value = editor.innerHTML;
}

const postSubmissionClaim = function(){
    var editor = document.querySelector(".editorclaim");
    var contentInput = document.querySelector(".post-content-claim");
    contentInput.value = editor.innerHTML;
}

const postSubmissionClaimUpdate = function(){
    var editor = document.querySelector(".editorclaimupdate");
    var contentInput = document.querySelector(".post-content-claim-update");
    contentInput.value = editor.innerHTML;
}

var postSubmissionUpdateCompanyInfo = function(){
    var editorinfo1 = document.querySelector(".editorvision");
    var editorinfo2 = document.querySelector(".editormission");

    var contentInput1 = document.querySelector(".post-content-vision");
    var contentInput2 = document.querySelector(".post-content-mission");

    contentInput1.value = editorinfo1.innerHTML;
    contentInput2.value = editorinfo2.innerHTML;
}

// Upload multiple image galery preview
$(function() {
    var imagesPreview = function(input, placeToInsertImagePreview) {

        if (input.files) {
            var filesAmount = input.files.length;

            for (i = 0; i < filesAmount; i++) {
                var reader = new FileReader();

                reader.onload = function(event) {
                    $($.parseHTML('<img>')).attr('src', event.target.result).appendTo(placeToInsertImagePreview);
                }

                reader.readAsDataURL(input.files[i]);
            }
        }

    };

    $('.add-image').on('change', function() {
        imagesPreview(this, 'div.gallerycover');
    });

    $('.add-image-update').on('change', function() {
        imagesPreview(this, 'div.gallerycoverupdate');
    });
});
