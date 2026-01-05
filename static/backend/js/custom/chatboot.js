/*
 * ***************************************************************************************************************************************************
 * ***************************************************************************************************************************************************
 * **************************************************************BUILDING CHAT BOOT***************************************************************
 * ***************************************************************************************************************************************************
 * ***************************************************************************************************************************************************
 */

/**
 * -----------------------------------------------------------------
 * Predefined Variables
 * ----------------------------------------------------------------*
 */
var chatSocket = '';
var host = window.location.host;
var scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
var scheme_http = window.location.protocol;
var opponent_email = '';
var opponent_name = '';
var opponent_id = '';
var owner_email = '';
var owner_name = '';
var owner_id = '';
var iddialog = '';
var resp_msg_author = null;
var key = '';
var containerchat = document.querySelector('#contentchat');
var ppDefaultOwner = 'http://' + host + '/static/assets/img/avatars/avatar.png';
var ppDefaultOpponent = 'http://' + host + '/static/assets/img/avatars/client.png';

function initializeChat(data){
    /**User info */
    opponent_email = data.getAttribute('opponent_email');
    opponent_name = data.getAttribute('opponent_name');
    opponent_id = data.getAttribute('opponent_id');
    owner_email = data.getAttribute('owner_email');
    owner_name = data.getAttribute('owner_name');
    owner_id = data.getAttribute('owner_id');
    iddialog = data.getAttribute('iddialog');
    $('#userchat').text(opponent_name)
    
    /**Initialize html */
    $('#containerchat').empty();
    $('#emptychat').css('display', 'none');
    $('.input-group-chat').css('visibility', 'visible');
    executiondialogue(data);
}

function executiondialogue(data) {
    //connexion websoket
    var ws_path = scheme + '://' + host + '/ws/chat/' + iddialog + '/';
    chatSocket = new ReconnectingWebSocket(ws_path);

    function fetchMessages() {
        chatSocket.send(JSON.stringify({ 'command': 'fetch_messages', 'user': owner_email }));
    }

    chatSocket.onopen = function(e) {
        // afficharge des anciens messages
        fetchMessages();
    }

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        console.log(data)
        affichargeMessage(data);
    };

    function affichargeMessage(data) {
        if (data['command'] === "messages") {
            let j = data['messages'].length;
            for (let i = j; i >= 0; i--) {
                if (data['messages'][i] != undefined) {
                    createMessageAncien(data['messages'][i]);
                }
            }
            document.querySelector("#contentchat").scrollBy(0, document.querySelector("#contentchat").scrollHeight);
        } else if (data.message['command'] === "new_message") {
            if (!data.message.message.lecture) {
            }else {
                idMessage = "";
                createMessage(data['message']);
            }
            document.querySelector("#contentchat").scrollBy(0, document.querySelector("#contentchat").scrollHeight);
        } else if (data.message['command'] === "is_writting") {
            if (data.message.message['to'] === owner_email) {
                $('.writechatbox').css('display', 'block');
                $(".write_chat").text(data.message.message['from_name']+' écris...');
            }
        }
    }

    function createMessage(data) {
        var author = '';
        var content = data.message['content'];
        var repondu = data.message['repondu'];
        var read = data.message['Lecture'];
        var date2 = data.message['date'];
        var heure_web2 = data.message['heure_web'];
        var min = data.message['min'];
        if (data.message != undefined) {
            author = data.message['author'];
        } else {
            author = data.author;
        }
        var d = new Date();
        var date1 = d.toLocaleDateString();
        var heure_web1 = d.getHours();

        final_date = "   " + heure_web2 + "h" + min;
      
        /**Right */
        var div1TagRight = document.createElement('div');
        var div2TagRight = document.createElement('div');
        var spanTagRight = document.createElement('span');
        var timeTagRight = document.createElement('time');
        var ppTagRight = document.createElement('img');
 
        /**Left */
        var div1TagLeft = document.createElement('div');
        var div2TagLeft = document.createElement('div');
        var spanTagLeft = document.createElement('span');
        var timeTagLeft = document.createElement('time');
        var ppTagLeft = document.createElement('img');

        if (author === owner_email) {
            containerchat.appendChild(div1TagRight);
            div1TagRight.appendChild(div2TagRight);
            div2TagRight.appendChild(spanTagRight);
            div2TagRight.appendChild(timeTagRight);
            div1TagRight.appendChild(ppTagRight);
            div1TagRight.className = 'media media-chat media-chat-right';
            div2TagRight.className = 'text-content';
            spanTagRight.className = 'message';
            timeTagRight.className = 'time';
            if (repondu) {
            }else{
                spanTagRight.append(content);
                timeTagRight.append(final_date);
                div1TagRight.className = 'media media-chat media-chat-right chatrighttime';
            }

            if(heure_web1 != heure_web2 ){
                ppTagRight.className = 'rounded-circle chatimage';
                ppTagRight.src = ppDefaultOwner;
            }

            if (read) {
            } else {
            }

        } else {
            containerchat.appendChild(div1TagLeft);
            div1TagLeft.appendChild(div2TagLeft);
            div2TagLeft.appendChild(spanTagLeft);
            div2TagLeft.appendChild(timeTagLeft);
            div1TagLeft.prepend(ppTagLeft)
            div1TagLeft.className = 'media media-chat';
            div2TagLeft.className = 'text-content';
            spanTagLeft.className = 'message';
            timeTagLeft.className = 'time';
            if (repondu) {
            }else{
                spanTagLeft.append(content);
                timeTagLeft.append(final_date);
                div1TagLeft.className = 'media media-chat chatlefttime';
            }

            if(heure_web1 != heure_web2 ){
                ppTagLeft.className = 'rounded-circle chatimage';
                ppTagLeft.src = ppDefaultOpponent;
            }
        }
    }

    function createMessageAncien(data) {
        var author = data['author'];
        var content = data['content'];
        var d = new Date();
        var date2 = data.date;
        var date1 = d.toLocaleDateString();
        var final_date = ''

        /**Right */
        var div1TagRight = document.createElement('div');
        var div2TagRight = document.createElement('div');
        var spanTagRight = document.createElement('span');
        var timeTagRight = document.createElement('time');
        var ppTagRight = document.createElement('img');

        /**Left */
        var div1TagLeft = document.createElement('div');
        var div2TagLeft = document.createElement('div');
        var spanTagLeft = document.createElement('span');
        var timeTagLeft = document.createElement('time');
        var ppTagLeft = document.createElement('img');

        /**Time Day Separator */
        var divTagTime = document.createElement('div')
        var spanTagTime = document.createElement('span')

        if (date1 == date2) {
            final_date = 'Aujourd\'hui à ' + data.heure_web + "h" + data.min;
        } else {
            final_date = data.updated_by;
        }

        if (author === owner_email) {
            containerchat.appendChild(div1TagRight);
            div1TagRight.appendChild(div2TagRight);
            div2TagRight.appendChild(spanTagRight);
            div2TagRight.appendChild(timeTagRight);
            div1TagRight.appendChild(ppTagRight);
            div1TagRight.className = 'media media-chat media-chat-right';
            div2TagRight.className = 'text-content';
            spanTagRight.className = 'message';
            timeTagRight.className = 'time';
            ppTagRight.className = 'rounded-circle chatimage';
            ppTagRight.src = ppDefaultOwner;
            if (data.repondu) {
            }else{
                spanTagRight.append(content);
                timeTagRight.append(final_date);
            }
        } else {
            containerchat.appendChild(div1TagLeft);
            div1TagLeft.appendChild(div2TagLeft);
            div2TagLeft.appendChild(spanTagLeft);
            div2TagLeft.appendChild(timeTagLeft);
            div1TagLeft.prepend(ppTagLeft)
            div1TagLeft.className = 'media media-chat';
            div2TagLeft.className = 'text-content';
            spanTagLeft.className = 'message';
            timeTagLeft.className = 'time';
            ppTagLeft.className = 'rounded-circle chatimage';
            ppTagLeft.src = ppDefaultOpponent;
            if (data.repondu) {
            }else{
                spanTagLeft.append(content);
                timeTagLeft.append(final_date);
            }
          

            if (date1 != date2) {
                containerchat.appendChild(divTagTime);
                divTagTime.appendChild(spanTagTime);
                divTagTime.className = 'daytimeseparator';
                spanTagTime.append(final_date);
            }
        }
    }

    function entrain_ecrire_msg() {
        chatSocket.send(JSON.stringify({
            'command': 'is_writting',
            'from': owner_email,
            'from_name': owner_name,
            'at': iddialog,
            'to': opponent_email,
            'to_name': opponent_name,
        }));
    }

    // envoyer le message apres avoir appuuyer sur la touche entrer du clavier
    $("#new-message").on('keypress', function(e){
        entrain_ecrire_msg();
        if (e.which == 13) {
            var messagetest1 = undefined;
            var message = e.target.value;
            var repondu = ''
            if (message != "") {
                e.preventDefault();
                if (messagetest1 == "") {
                    key = "emoji";
                    sendejsonmessage(message, key, repondu);
                } else {
                    key = "texte";
                    sendejsonmessage(message, key, repondu);
                }
            }
            if (e.key === "Enter") {
                document.getElementById('new-message').value = '';
            }
        }else{
            $('.writechatbox').css('display', 'none');
        }
    })

    function sendejsonmessage(message, key, repondu) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'command': 'new_message',
            'from': owner_email,
            'at': iddialog,
            'to': opponent_email,
            'key': key,
            'repondu': repondu,
            'messagede': resp_msg_author,
        }));
    }

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };



    //fin chat sms
    return false
}

/** Filtre des dialogues */
$("#searchdialogue").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#filterdialog li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

