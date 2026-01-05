 
 // connecting to webSocket and responses starts here
 
 document.addEventListener('DOMContentLoaded', function(){
    const user_id = document.getElementById('user_id').value;
    const webSocketBridgeTicket= new channels.WebSocketBridge();
    webSocketBridgeTicket.connect(`/ws/notification/${user_id}/`);
    webSocketBridgeTicket.listen(function(action){
        console.log('SOCKET', action)
        const data = action.unreaded_notifications;
        var unreaded_count = action.unreaded_notification_count;
        var options = { year: 'numeric', month: 'long', day: 'numeric' };
        if(unreaded_count > 0){
            $('#notification_container').empty();
            $('#notification_counter').empty();
            for(i=0; i < data.length; i++){
                var date = data[i].creation_date;  
                var format_date = new Date(date);
                var timestamp = format_date.toLocaleDateString('fr-FR', options)
                var hour = format_date.getHours();
                var min = format_date.getMinutes();
                var final_min = '';
                if(Number(min) < 10){
                    final_min = '0'+min;
                }else{
                    final_min = min;
                }
                var id_notif = data[i].id;
                var link = data[i].link;
                var body = data[i].body;
                var cover_author = "/static/assets/img/avatars/1.png"

                $('#notification_container').prepend(
                    `   <li class="list-group-item list-group-item-action dropdown-notifications-item">
                            <div class="d-flex">
                                <div class="flex-shrink-0 me-3">
                                    <div class="avatar">
                                    <img src="`+cover_author+`" alt class="w-px-40 h-auto rounded-circle">
                                    </div>
                                </div>
                                <div class="flex-grow-1">
                                    <h6 class="mb-1">Support</h6>
                                    <p class="mb-0">`+body+`</p>
                                    <small class="text-muted">Il y a 2h</small>
                                </div>
                                <div class="flex-shrink-0 dropdown-notifications-actions">
                                    <a href="javascript:void(0)" class="dropdown-notifications-read"><span class="badge badge-dot"></span></a>
                                    <a href="javascript:void(0)" class="dropdown-notifications-archive"><span class="bx bx-x"></span></a>
                                </div>
                            </div>
                        </li>
                    `
                );

            }
            var old_count = document.getElementById("notification_counter").innerText;
            var current_count = unreaded_count;
            var final_data = Number(old_count) + Number(current_count)
            $('#notification_counter').text(final_data);
            document.querySelector("#notification_container").scrollBy(0,document.querySelector("#notification_container").scrollHeight);
        }else{
            $('#notification_container').append(
                `
                <div class="emptynotification">
                    <p>Aucune message pour l'instant!</p>
                </div>
                `
            )
        }
        
    })
    document.ws = webSocketBridgeTicket;
})
