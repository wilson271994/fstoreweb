
from .models import *

def define_usertype(request):
    """
    Ce preprocesseur de context permet de charger une instance du particulier connecter
    dans les templates.
    :param request:
    :return:
    """
    
    ctx = {}
    
    try:
        if request.user.is_authenticated:
            ctx['is_authenticated'] = True
        else:
            ctx['is_authenticated'] = False
    except Exception as e:
        print(e)
    
    try:
        if request.user.is_superuser:
            ctx['is_superuser'] = True
        else:
            ctx['is_superuser'] = False
    except Exception as e:
        print(e)

    try:
        if Persons.objects.filter(user=request.user, is_staff=True):
            ctx['is_staff'] = True
        else:
            ctx['is_staff'] = False
    except Exception as e:
        print(e)
        
    return ctx