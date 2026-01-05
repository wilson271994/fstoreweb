from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from allauth.account.decorators import verified_email_required
from django.contrib import messages
from django.contrib.auth import login
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate 
from allauth.account.models import EmailAddress
from .forms import *
from .models import *
import json
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from cities_light.models import City, Country
import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError 
# Create your views here.

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import requests

########################################################
###################ACCESS CONTROLLER
@verified_email_required
def ValidationSuperAdmin(request):
    try:
        if request.user.is_superuser:
            return True
        else:
            return False
    except:
        pass

def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    
def AuthHome(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'core/auth.html') 

#User Creation By Customers Method
def CreateUser(request):
    if request.method == 'POST':
        email               = request.POST['email']
        username            = request.POST['username']
        password            = request.POST['password1']

        if email != '' and User.objects.filter(email=email).exists():
            return JsonResponse({'status':500, 'message':str('Cette utilisateur existe déjà.')})
        elif username != '' and User.objects.filter(username=username).exists():
            return JsonResponse({'status':500, 'message':str('Désolé ce nom d\'utilisateur est déjà utilisé, essayez un autre.')})
        else:
            pass

        if request.POST['password1'] == request.POST['password2']:
            pass
        else:
            return JsonResponse({'status':500, 'message':str('Les mots de passe sont différents')})
        
        form = SignupUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # save the user here
            user.is_active = True
            user.save()

            EmailAddress.objects.create(
                user=user, 
                email=user.email,
                verified=True, 
                primary=True
            )

            person = None
            formperson = SignupPersonForm({
                'phone'     : request.POST['phone'],
                'country'   : request.POST['country'],
                'city'      : request.POST['city'],
                'sexe'      : request.POST['sexe'],
                'shop'      : user.username,
                'user'      : user.id
            })
            if formperson.is_valid():
                person = formperson.save()
                
                if 'pp' in request.POST and request.POST['pp']:
                    person.pp = request.FILE['pp']

            if request.POST['type_user'] == 'staff':
                if person is not None:
                    person.is_staff = True
                    person.save()

                    try:
                        #Send Staff credential By EMAIL
                        context = {
                            "username"     : username,
                            "password"     : password,
                            "date"         : datetime.now().strftime("%d-%m-%Y %H:%M")
                        }

                        receiver_email = user.email
                        template_name = "core/mail/staff_account_info.html"
                        convert_to_html_content =  render_to_string(
                            template_name=template_name,
                            context=context
                        )
                        plain_message = strip_tags(convert_to_html_content)
                        send_mail(
                            subject                         = _('Fstore'),
                            message                         = plain_message,
                            from_email                      = settings.EMAIL_HOST_USER,
                            recipient_list                  = [receiver_email,],
                            html_message                    = convert_to_html_content,
                            fail_silently                   = True
                        ) 
                    except Exception as error:
                        print(error)

            if request.POST['type_user'] == 'customer':
                if person is not None:
                    person.is_customer = True
                    person.save()
                    
                    try:
                        #Send Customer credential By EMAIL
                        context = {
                            "username"     : username,
                            "password"     : password,
                            "date"         : datetime.now().strftime("%d-%m-%Y %H:%M")
                        }

                        receiver_email = user.email
                        template_name = "core/mail/customer_account_info.html"
                        convert_to_html_content =  render_to_string(
                            template_name=template_name,
                            context=context
                        )
                        plain_message = strip_tags(convert_to_html_content)
                        send_mail(
                            subject                         = _('Fstore'),
                            message                         = plain_message,
                            from_email                      = settings.EMAIL_HOST_USER,
                            recipient_list                  = [receiver_email,],
                            html_message                    = convert_to_html_content,
                            fail_silently                   = True
                        ) 
                    except Exception as error:
                        print(error)

            return JsonResponse({'status':200, 'message':str('Utilisateur créé avec succès.')})
        else:
            error = form.errors.get_json_data()
            error_message = ''
            if 'password2' in error:
                error_message = error['password2'][0]['message']
            if 'username' in error:
                error_message = error['username'][0]['message']
            return JsonResponse({'status':500, 'message':error_message }, safe=False)
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire.') })

#Account Activation Method
def accountActivationMethod(request): 
    if request.method == 'POST':
        code                = request.POST['code']
        email               = request.POST['email']
        password            = request.POST['password']
        url             = reverse_lazy('master:home-user-account')
        if AccountActivationCode.objects.filter(code=code, person__user__email=email, is_expired=False):
            try:
                userEmail = EmailAddress.objects.get(email=email)
                userEmail.verified = True
                userEmail.save()
            except Exception as e:
                userEmail = None
                
            try:
                user_active = User.objects.get(email=email)
                user_active.is_active = True
                user_active.save()
            except Exception as e:
                user_active = None
            
            try:
                person = Persons.objects.get(user=User.objects.get(email=email))
            except Exception as e:
                person = None

            #update activation code to expired
            activation_code = AccountActivationCode.objects.filter(code=code, person__user__email=email, is_expired=False)[0]
            activation_code.is_expired = True

            form = LoginEmailForm(request.POST)
            if form.is_valid():
                if userEmail is None or person is None:
                    auth_message = "Adresse mail incorrect, ou compte bloqué. Si cette erreur persiste, contactez l'administrateur."
                else:
                    try:
                        user = authenticate(email=email, password=password)
                    except Exception as e:
                        user = None
                    if user is None:
                        auth_message = "Mot de passe incorrect"
                    else:
                        if userEmail.verified == True:
                            auth_message = "Connexion réussie"
                            login(request, user)
                            return JsonResponse({"status":200,"message": auth_message, 'url':url})
                        else:
                            auth_message = "Votre compte est désactivé, veuillez contacter l'administrateur"
                return JsonResponse({"status":500, "message": auth_message})
            return JsonResponse({"status":500, "message": "Une erreur est survenue lors de la connexion, Rechargez et rééssayez"})
        return JsonResponse({"status":500, "message": "Le code que vous avez saisi est incorrect ou inactif, vérifiez-le et essayez à nouveau."})
    return JsonResponse({'status':500, 'message':str("Une erreur s'est produite veuillez contacter l'administrateur.")})

#Update User Info Method
def UpdateUser(request):
    if request.method == 'POST' and ValidationSuperAdmin(request) == True:
        person = Persons.objects.get(id=request.POST["person_id"])

        formperson = UpdatePersonForm(request.POST, request.FILES, instance=person)
        if formperson.is_valid():
            person = formperson.save()
        else:
            print('error form person', formperson.errors)
        
        user = User.objects.get(id=person.user.id)
        user.first_name                 = request.POST['first_name']
        user.last_name                  = request.POST['last_name']
        user.email                      = request.POST['email'] 
        user.username                   = request.POST['username']
        
        try:
            if request.POST['new_password1'] and  str(request.POST['new_password1']) == str(request.POST['new_password2']):
                user.password = make_password(request.POST['new_password1'])
        except Exception as e:
            pass
        user.save()
        
        if Distributors.objects.filter(person=person):
            distributor = Distributors.objects.get(person=person)
            formdistributor = UpdateDistributorForm(request.POST, request.FILES, instance=distributor)
            if formdistributor.is_valid():
                formdistributor.save()
            else:
                print('distrubutor form', formdistributor.errors)
        return JsonResponse({'status':200, 'message':str('Utilisateur créer avec succès')})
    else:
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite veuillez contacter l\administrateur.')})

#Authentification Method
def userLoginMethod(request):
    username            = request.POST['username']
    password            = request.POST['password']
    url                 = reverse_lazy('dashboard:home')
    if validateEmail(username):
        try:
            userEmail = EmailAddress.objects.get(email=username)
        except Exception as e:
            userEmail = None
        if userEmail is None:
            auth_message = "Adresse mail incorrect"
        else:
            try:
                user = authenticate(username=username, password=password)
            except Exception as e:
                user = None
            if user is None:
                auth_message = "Mot de passe incorrect"
            else:
                if userEmail.verified and user.is_active:
                    auth_message = "Connexion réussie"
                    login(request, user)
                    return JsonResponse({"status":200,"message": auth_message, 'url':url})
                else:
                    auth_message = "Votre compte est désactivé, veuillez contacter l'administrateur"
    else:
        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            print(e)
            user = None

        if user is None:
            auth_message = "Mot de passe ou nom d'utilisateur incorrect"
        else:
            if user.is_active:
                auth_message = "Connexion réussie"
                login(request, user)
                return JsonResponse({"status":200,"message": auth_message, 'url':url})
            else:
                auth_message = "Votre compte est désactivé, veuillez contacter l'administrateur"
    return JsonResponse({"status":500, "message": auth_message})

#User Password Reset Method
def userChangePassword(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.POST['useremail'])
        if str(request.POST['new_password1']) == str(request.POST['new_password2']):
            user.password = make_password(request.POST['new_password1'])
            user.save()
            return JsonResponse({"status":200, "message": str('Votre mot de passe a bien été mis a jour !')})   
        else:
            return JsonResponse({"status":500, "message": str('Les mots de passe sont différents!')})
    return JsonResponse({"status":500, "message": str("Une erreur est survenue lors de la connexion, Recharger et rééssayer")})

#System Logout User Method
@verified_email_required
def userLogOut(request):
    if request.user.is_authenticated:
        try:
            person = Persons.objects.get(user=request.user)
            person.is_online = False
            person.save()
        except Exception as e:
            print(e)
    logout(request)
    return redirect('core:auth-login')

#Get Cities By Country Method
def getCityFromCountry(request):
    if request.method == 'POST':
        countryid = request.POST['country']
        cities = []
        allcity = City.objects.filter(country_id=countryid)
        for cit in allcity:
            cities.append({
                'cityid'    : cit.id,
                'cityname'  : cit.name
            })
    return JsonResponse({'status':200, 'result':cities})