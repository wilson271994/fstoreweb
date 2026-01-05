"""
ASGI config for mabounia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

###############################CONFIGURATION LOCAL####################""
import os
import django
from channels.routing import ProtocolTypeRouter , URLRouter 
from channels.security.websocket import AllowedHostsOriginValidator 
from fstore.routing import ws_pattern

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fstore.settings')
django.setup()

application = ProtocolTypeRouter({
    "websocket" : AllowedHostsOriginValidator (
        URLRouter(
            ws_pattern
        )
    )
})


###########################CONFIGURATION PRODUCTION ######################""
# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fstore.settings')

# import django
# django.setup()


# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from fstore.routing import ws_pattern

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             ws_pattern
#         )
#     ),
# })


