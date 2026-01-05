from django.urls import re_path
from dashboard.consumers import *

ws_pattern = [
    re_path(r'^ws/chat/(?P<room_name>[-:\w]+)/$' , ChatConsumer),
]
