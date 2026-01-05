from django.contrib.auth import get_user_model
import json
from .models import *
from core.models import *
user = get_user_model()
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import formats
from django.contrib.auth.models import User
import threading
from allauth.account.decorators import verified_email_required


class ChatConsumer(WebsocketConsumer):
    @verified_email_required
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat__%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()  
        
    #################SEND MESSAGE IN GROUP CHAT
    @verified_email_required
    def send_message(self,message):
        self.send(text_data=json.dumps(message))
        
    @verified_email_required    
    def fetch_messages(self, data):
        user_c=Dialogs.objects.get(pk=int(self.room_name))
        if(user_c.owner.username == data['user']):
            messages=Messages.objects.filter(idchat=self.room_name, supp_auth=False).order_by('-updated_date').all()
        else:
            messages=Messages.objects.filter(idchat=self.room_name, supp_dest=False).order_by('-updated_date').all()
    
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
        
    ###################FETCH OLD MESSAGE AND CONVERT TO JSON
    @verified_email_required
    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    @verified_email_required
    def new_message(self, data):
        author = data["from"]
        destinator = data["to"]
        m = Dialogs.objects.get(id=int(self.room_name))
        if User.objects.filter(id=data['messagede']):
            rep_author = User.objects.get(id=data['messagede'])
        else:
            rep_author = None
        author_user = User.objects.get(email=author)
        dest_user = User.objects.get(email=destinator)
        message = Messages.objects.create(
            destinataire = dest_user,
            idchat = m,
            author = author_user,
            mail_author=author,
            mail_destinataire=destinator,
            key=data["key"],
            content = data['message'],
            repondu = data['repondu'],
            rep_msg_author = rep_author,
            Lecture=m.opponent_is_online) 
        content = {
            'command':'new_message',
            'message':self.message_to_json(message)
        }  
        
        return self.send_chat_message(content)
    
    @verified_email_required
    def auto_response(self, message, author, destinator, data):
        author = author
        destinator = destinator
        m = Dialogs.objects.get(id=int(self.room_name))
        if User.objects.filter(id=data['messagede']):
            rep_author = User.objects.get(id=data['messagede'])
        else:
            rep_author = None
        author_user = User.objects.get(email=author)
        dest_user = User.objects.get(email=destinator)
        message = Messages.objects.create(
            destinataire = dest_user,
            idchat = m,
            author = author_user,
            mail_author=author,
            mail_destinataire=destinator,
            key=data["key"],
            content = message,
            repondu = data['repondu'],
            rep_msg_author = rep_author,
            Lecture=m.opponent_is_online) 
        content = {
            'command':'new_message',
            'message':self.message_to_json(message)
        }   
        return self.send_chat_message(content)

    @verified_email_required
    def message_to_json(self,message):
        return {
            'author':message.author.email,
            'author_name':message.author.username,
            'content':message.content,
            'updated_by':formats.date_format(message.updated_date, "SHORT_DATETIME_FORMAT"),
            'date':message.updated_date.strftime("%d/%m/%Y"),
            'heure_web':int(message.updated_date.strftime("%H"))+int(1),
            'heure':message.updated_date.strftime('%H:%M'),
            'min':message.updated_date.strftime("%M"),
            'destinataire':message.destinataire.email,
            'destinataire_name':message.destinataire.username,
            'idchat':message.idchat.id,
            'lecture':message.Lecture,
            'key': message.key,
            'idmsg': message.pk,
            'repondu':message.repondu,
            'rep_msg_author':message.rep_msg_author,
            'supp_auth':message.supp_auth,
            'supp_dest':message.supp_dest,
            'name_aut': message.author.get_full_name()
        } 
    
    @verified_email_required
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type': 'chat_message',
                'message': message 
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
        
    
    ##########################RECEIVE MESSAGE CHANNEL
    @verified_email_required
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        
        
    ############################USER IS TYPPING
    @verified_email_required
    def writting(self, data):
        content = {
            'command': 'is_writting',
            'message': data
        }
        self.send_chat_message(content)

        
    ######################ALL COMMANDS
    commands = {
            'fetch_messages':fetch_messages,
            'new_message':new_message,
            'is_writting':writting,
        }     
            
    @verified_email_required
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

