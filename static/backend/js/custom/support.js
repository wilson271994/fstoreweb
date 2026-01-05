
/**
 * #################################################################################
 * ############################## SERVICE SUPPORT ##################################
 * #################################################################################
 */
/** gestion des tables list */
$("#searchservicesupport").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterservicesupport tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

/** service support creation */
$("#addservicesupport").on("click", function(e){
    e.preventDefault();
    $("#serviceSupportCreation").modal("show");
})

/** Service Support update */
$(".updateservicesupport").on("click", function(e){
    e.preventDefault();
    var id = $(this).data('id');
    var title           = $(this).data('title');
    var description     = $(this).data('description');
    var ispayment       = $(this).data('ispayment');
    var price           = $(this).data('price');
    var selectpayment   = '';

    if(ispayment === 'True'){
        selectpayment = `<option value="True" selected >Service Payant</option>`;
    }else{
        selectpayment = `<option value="False" selected >Service Non Payant</option>`;
    }

    const delta = quill.clipboard.convert(description)
    quill.setContents(delta, 'silent')
    $('.post-content-update').val(description);

    $('#servicesupportid').val(id);
    $('#servicesupporttitle').val(title);
    $('#servicesupportprice').val(price.split(',')[0] + '.' + price.split(',').pop());
    $('#servicesupportpayment').append(selectpayment)
    $('#serviceSupportUpdateModal').modal("show");
})


/**
 * #################################################################################
 * ############################## SUPPORT TICKET ###################################
 * #################################################################################
 */

//initial 
var deletemessageurl    = '';
var token               = '';
//Open Chat
const openTicketChat = (attribute) => {
    token                 = attribute.getAttribute('token');
    deletemessageurl      = attribute.getAttribute('deletemessageurl');
    const url                   = attribute.getAttribute('url');
    const ticket                = attribute.getAttribute('ticket');
    const data = {
        ticket                      : ticket,
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
                $('#chatticketexchange').html('');
                const defaultcustomerpp     = '/static/front/assets/images/default_pp.png';
                const defaultagentimage     = '/static/front/assets/images/default_operator_pp.png';

                const messages = json.messages;
                const ticket  = json.ticketInfo;
                $('#ticketid').val(ticket.id);
                $('#numberticket').text(ticket.ticketnumber);
                $('#statusticket').text(ticket.status);
                $('#serviceticket').text(ticket.service);
                $('#resumeticket').text(ticket.resume);

                for(i=0; messages.length > i ; i++){
                    var messageid               = messages[i].messageid;
                    var customer_name           = messages[i].customer_name;
                    var customer_pp             = messages[i].customer_pp != '' ? messages[i].customer_pp : defaultcustomerpp;
                    var operator_name           = messages[i].operator_name;
                    var operator_pp             = messages[i].operator_pp != '' ? messages[i].operator_pp : defaultagentimage;
                    var message                 = messages[i].message;
                    var rep_message             = messages[i].rep_message;
                    var is_customer_message     = messages[i].is_customer_message;
                    var is_operator_message     = messages[i].is_operator_message;
                    var created_date            = moment(messages[i].created_date).fromNow();

                    if(is_customer_message){
                        $('#chatticketexchange').append(`
                            <div class="currentmessage-`+messageid+`" id="leftticketchat">
                                <div class="headerchatticketmessage">
                                    <div class="row">
                                        <div class="col-lg-10 profilheaderticketmessage">
                                            <img src="`+customer_pp+`" alt="" class="ppchat">
                                            <h4>`+customer_name+`</h4>
                                        </div>
                                    </div>
                                </div>
                                <div class="bodychatticketmessage">
                                    <p>`+message+`</p>
                                    <time>`+created_date+`</time>
                                </div>
                            </div>
                        `);
                    }
                    if(is_operator_message){
                        $('#chatticketexchange').append(`
                            <div class="currentmessage-`+messageid+`" id="rightticketchat">
                                <div class="headerchatticketmessage">
                                    <div class="row">
                                        <div class="col-lg-10 profilheaderticketmessage">
                                            <img src="`+customer_pp+`" alt="" class="ppchat">
                                            <h4>`+customer_name+`</h4>
                                        </div>
                                        <div class="optionmessage col-lg-2">
                                            <div class="row">
                                                <button class="col-lg-4"><i class="fa fa-edit"></i></button>
                                                <button class="col-lg-4" 
                                                    url="`+deletemessageurl+`" 
                                                    token="`+token+`"
                                                    message="`+messageid+`"
                                                    onClick="deleteMessageTicketChat(this)"><i class="fa fa-trash"></i></button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="bodychatticketmessage">
                                    <p>`+message+`</p>
                                    <time>`+created_date+`</time>
                                </div>
                            </div>
                        `);
                    }
                }

                const ticketbloclistcontain        = document.getElementById('ticketlistbloc');
                const ticketmessagelistcontain     = document.getElementById('ticketcontain');
                ticketbloclistcontain.style.display = 'none';
                ticketmessagelistcontain.style.display = 'block';
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

//close chat
const closeTicketChat = (attribute) => {
    const ticketbloclistcontain        = document.getElementById('ticketlistbloc');
    const ticketmessagelistcontain     = document.getElementById('ticketcontain');
    ticketbloclistcontain.style.display = 'block';
    ticketmessagelistcontain.style.display = 'none';
}

/**New Ticket Modal */
$("#newticket").on("click", function(e){
    e.preventDefault();
    $("#newTicketModal").modal("show");
})

/**Create Message Request */
$(document).on('submit', '.createTicketMessageSubmit', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var form = $(this);
    var formdata = (window.FormData) ? new FormData(form[0]) : null;
    var data = (formdata !== null) ? formdata : form.serialize();
    var valBtn = $('.createbtnticketmessage').text();
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
            $('.createbtnticketmessage').text('en cours...').prop('disabled',true);
            $(document.body).css({'cursor' : 'wait'});
            form.find('*').prop('disabled', true);
        },
        success: function (json) {
            if (json.status == 200){
                const defaultagentimage     = '/static/front/assets/images/default_operator_pp.png';

                const message               = json.message;
                var messageid               = message.messageid;
                var operator_name           = message.operator_name;
                var operator_pp             = message.operator_pp != '' ? message.operator_pp : defaultagentimage;
                var tmessage                = message.message;
                var rep_message             = message.rep_message;
                var is_operator_message     = message.is_operator_message;
                var created_date            = moment(message.created_date).fromNow();

                if(is_operator_message){
                    $('#chatticketexchange').append(`
                        <div class="currentmessage-`+messageid+`" id="rightticketchat">
                            <div class="headerchatticketmessage">
                                <div class="row">
                                     <div class="col-lg-10 profilheaderticketmessage">
                                        <img src="`+operator_pp+`" alt="" class="ppchat">
                                        <h4>`+operator_name+`</h4>
                                    </div>
                                    <div class="optionmessage col-lg-2">
                                        <div class="row">
                                            <button class="col-lg-4"><i class="fa fa-edit"></i></button>
                                            <button class="col-lg-4" 
                                                url="`+deletemessageurl+`" 
                                                token="`+token+`"
                                                message="`+messageid+`"
                                                onClick="deleteMessageTicketChat(this)"><i class="fa fa-trash"></i></button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="bodychatticketmessage">
                                <p>`+tmessage+`</p>
                                <time>`+created_date+`</time>
                            </div>
                        </div>
                    `);
                }
                $('#chattextbox').val('');
            }else{
                toastr.error(json.message);
            }
        },
        complete: function () {
            $('.createbtnticketmessage').empty();
            $('.createbtnticketmessage').text(valBtn).prop('disabled',false);
            $(document.body).css({'cursor' : 'default'});
            form.find('*').prop('disabled', false);
        },
        error: function(jqXHR, textStatus, errorThrown){}
    });
});

//Delete Message Ticket
const deleteMessageTicketChat = (attribute) => {
    const token         = attribute.getAttribute('token');
    const url           = attribute.getAttribute('url');
    const message       = attribute.getAttribute('message');
    Swal.fire({
        title                   : "Êtes vous sûr?",
        text                    : "Ce Message sera definitivement supprimer!",
        icon                    : "warning",
        showCancelButton        : true,
        confirmButtonColor      : "#0637a8",
        confirmButtonText       : "Oui",
        cancelButtonText        : "Non",
        preConfirm: () => {
            actionDeletefunction(token, url, message);
        },
    })
    function actionDeletefunction(token, url, message){
        actionDeleteMessageTicketChat(token, url, message);
    }
}
const actionDeleteMessageTicketChat = (token, url, message) => {
    const data = {
        id                      : message,
        csrfmiddlewaretoken     : token
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
                $('.currentmessage-'+message).remove();
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
