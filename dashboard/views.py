from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from core.models import *
from allauth.account.decorators import verified_email_required
from core.models import *
from core.forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
from cities_light.models import City, Country
from .forms import *
import json
from decimal import Decimal
from django.utils.timezone import now
from uuid import getnode as get_mac
from django.http import Http404 
import requests
from django.contrib.sessions.models import Session
from django.utils import timezone

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .utils import *

# Create your views here.

###################ACCESS CONTROLLER

def is_auth(request):
    try:
        if request.user.is_authenticated:
            return True
        else:
            return False
    except:
        return False

def is_superuser(request):
    try:
        if request.user.is_superuser:
            return True
        else:
            return False
    except:
        return False

@verified_email_required
def is_staff(request):
    try:
        person = Persons.objects.get(user=request.user)
        if person.is_staff:
            return True
        else:
            return False
    except:
        return False

#########################################################################################
################################ MARKET PLACE INFO ###################################### 
#########################################################################################
#Home Company
def indexAboutCompany(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if Company.objects.all().first():
                companyinfo = Company.objects.all().first()
                all_phone = []
                all_email = []
                all_value = []
                all_social = []
                all_planning = []
                all_address = []
                commission_sales        = 0
                commission_product      = 0
                if companyinfo.phones.all().count() > 0:
                    for ph in companyinfo.phones.all():
                        all_phone.append({
                            'id':ph.pk,
                            'phone':ph.phone
                        })
                if companyinfo.emails.all().count() > 0:
                    for em in companyinfo.emails.all():
                        all_email.append({
                            'id':em.pk,
                            'email':em.email
                        })
                if companyinfo.values.count() > 0:
                    for val in companyinfo.values.all():
                        all_value.append({
                            'id':val.pk,
                            'label':val.label,
                            'value':val.value
                        })
                if companyinfo.socials.count() > 0:
                    for soc in companyinfo.socials.all():
                        all_social.append({
                            'id':soc.pk,
                            'name':soc.name,
                            'logo':soc.logo,
                            'link':soc.link
                        })
                if companyinfo.addresses.count() > 0:
                    for address in companyinfo.addresses.all():
                        all_address.append({
                            'id':address.pk,
                            'continent':address.continent,
                            'country':address.country,
                            'city':address.city,
                            'address':address.address,
                            'is_default':address.is_default,
                        })
                company = {
                    'id'                    : companyinfo.pk,
                    'name'                  : companyinfo.name,
                    'vision'                : companyinfo.vision,
                    'mission'               : companyinfo.mission,
                    'values'                : all_value,
                    'contacts'              : all_phone,
                    'emails'                : all_email,
                    'socials'               : all_social,
                    'planning'              : all_planning,
                    'addresses'             : all_address,
                    'logo'                  : companyinfo.logo,
                }
            else:
                company = None
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/company.html', locals())
        return render(request, 'dashboard/401.html', locals())
    return redirect('core:auth-home')

def updateInfoCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':    
            if Company.objects.all().first():
                current = Company.objects.first()
                current.name=request.POST['name']
                current.vision=request.POST['vision']
                current.mission=request.POST['mission']
                current.logo=request.FILES['logo'] if request.FILES else current.logo
                current.save()
            else:
                company = Company.objects.create(
                    name=request.POST['name'],
                    vision=request.POST['vision'],
                    mission=request.POST['mission'],
                    logo=request.FILES['logo'] if request.FILES else None,
                    create_by=request.user,
                )
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def valueCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':   
            current = Company.objects.all().first() 
            companyvalue = CompanyValues.objects.create(
                label=request.POST['label'],
                value=request.POST['value'],
            )
            current.values.add(companyvalue)
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def contactCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':   
            current = Company.objects.all().first() 
            phone = CompanyPhones.objects.create(
                phone=request.POST['phone'],
            )
            current.phones.add(phone)
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def emailCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':   
            current = Company.objects.all().first() 
            email = CompanyEmails.objects.create(
                email=request.POST['email'],
            )
            current.emails.add(email)
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def socialCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':   
            current = Company.objects.all().first() 
            social = CompanySocial.objects.create(
                name=request.POST['name'],
                link=request.POST['link'],
                logo=request.FILES['logo'],
            )
            current.socials.add(social)
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def deleteContactComapnyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            company = Company.objects.first()
            current = CompanyPhones.objects.get(id=request.POST['id'])
            company.phones.remove(current)
            current.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def deleteEmailComapnyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            company = Company.objects.first()
            current = CompanyEmails.objects.get(id=request.POST['id'])
            company.emails.remove(current)
            current.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def deleteSocialComapnyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            company = Company.objects.first()
            current = CompanySocial.objects.get(id=request.POST['id'])
            company.socials.remove(current)
            current.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def deleteValueComapnyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            company = Company.objects.first()
            current = CompanyValues.objects.get(id=request.POST['id'])
            company.values.remove(current)
            current.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

#manage Adress company
def createAddressCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':   
            current = Company.objects.all().first() 
            address = CompanyAddress.objects.create(
                continent=request.POST['continent'],
                country=request.POST['country'],
                city=request.POST['city'],
                address=request.POST['address'],
                postal=request.POST['postal'],
            )
            current.addresses.add(address)
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def updateAddressCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':   
            current = CompanyAddress.objects.filter(id=request.POST['id']) 
            current.update(
                continent=request.POST['continent'],
                country=request.POST['country'],
                city=request.POST['city'],
                address=request.POST['address'],
                postal=request.POST['postal'],
            )
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def deleteAddressCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            current = CompanyAddress.objects.get(id=request.POST['id'])
            company = Company.objects.first()
            company.addresses.remove(current)
            current.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def defaultAddressCompanyMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            current = CompanyAddress.objects.get(id=request.POST['id'])
            current.is_default = True
            current.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

#Partner Management
def indexCompanyPartnerMethod(request):
    if is_auth(request):
        module = 'analytics'
        if is_superuser(request) or is_staff(request):
            allpartner = []
            company = Company.objects.first()
            for item in company.partners.all():
                allpartner.append({
                    'id':item.pk,
                    'name' : item.name,
                    'description' : item.description,
                    'link' : item.link,
                    'logo' : item.logo,
                    'is_active' : item.is_active,
                    'is_approuved' : item.is_approuved,
                    'approuved_by' : item.approuved_by.get_full_name if item.approuved_by else 'En attente...',
                    'created_date' : item.created_date
                })
            return render(request, 'dashboard/home/partner.html', locals())
        return render(request, 'dashboard/401.html', locals())
    return redirect('core:auth-home')

def createCompanyPartnerMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            company = Company.objects.first()
            partner = CompanyPartner.objects.create(
                name=request.POST['name'],
                description=request.POST['description'],
                link=request.POST['link'],
                logo=request.FILES['logo'],
                create_by=request.user,
            )
            company.partners.add(partner)
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def updateCompanyPartnerMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            current = CompanyPartner.objects.get(id=request.POST['id'])
            current.name=request.POST['name'],
            current.description=request.POST['description'],
            current.link=request.POST['link'],
            current.logo=request.FILES['logo'] if request.FILES else current[0].logo
            current.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def statusCompanyPartnerMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            current = CompanyPartner.objects.get(id=request.POST['id'])
            if current.is_active:
                current.is_active = False
            else:
                current.is_active = True
            current.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def validateCompanyPartnerMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            current = CompanyPartner.objects.get(id=request.POST['id'])
            if current.is_approved:
                current.is_approved = False
                current.approved_by = None
            else:
                current.is_approved = True
                current.approved_by = request.user
            current.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def deleteCompanyPartnerMethod(request):
    if is_superuser(request):
        if request.method == 'POST':
            company = Company.objects.first()
            current = CompanyPartner.objects.get(id=request.POST['id'])
            company.partners.remove(current)
            current.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

def currencyToggle(request):
    currency = None
    try:
        person = Persons.objects.get(user=request.user)
        currency = Currency.objects.get(devise_destination=person.currency)
    except Exception as e:
        print(e)
    return currency

def userPermission(person):
    userprofil = UserProfil.objects.get(person=person)
    allmenu = []
    for menu in ParentMenus.objects.filter(is_active=True):
        allsubmenu = []
        for permmenu in userprofil.profil.permissions.all():
            parentmenu = ParentMenus.objects.get(menus__id=permmenu.menu.pk)
            if menu.pk == parentmenu.pk:
                allsubmenu.append({
                    'id' : permmenu.menu.pk,
                    'title' : permmenu.menu.title,
                    'link'  : permmenu.menu.link,
                    'code'  : permmenu.menu.code
                })
                allmenu.append({
                    'id' : menu.pk,
                    'title' : menu.title,
                    'label' : menu.label,
                    'icon'  : menu.icon,
                    'submenus' : allsubmenu
                })
    return allmenu

#########################################################################################
################################LOADING AND USERS DASHBOARD##############################
#########################################################################################
#Home Page Dashboard
def HomeAnalytics(request):
    if is_auth(request):
        globaltrafic    = 0
        for finan in Finances.objects.filter():
            globaltrafic += round(finan.total_price, 0)
        
        totalsell           = 0
        pendingdelivered    = 0
        completedelivered   = 0
        pendingcomplaints   = 0
        activesessions      = 0
        for comm in Commands.objects.filter(is_pay=True):
            totalsell += 1

        for livpend in Commands.objects.filter(is_pay=True, is_delivery=False):
            pendingdelivered += 1

        for livcomp in Commands.objects.filter(is_pay=True, is_delivery=True):
            completedelivered += 1

        for complain in customerSupportTicket.objects.filter(is_resolv=False):
            pendingcomplaints += 1
            
        
        allcustomer     = Persons.objects.filter(is_active=True, is_customer=True).count()
        allprovider     = Providers.objects.filter(is_active=True).count()

        try:
            current_person  = Persons.objects.get(user=request.user)
            permissions     = userPermission(current_person)
        except Exception as error:
            pass

        try:
            activesessions = Session.objects.filter(expire_date__gte=timezone.now()).count()
        except Exception as error:
            pass
        return render(request, 'dashboard/index.html', locals())
    return redirect('core:auth-home')

#User list Home
def UsersHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allperson           = []
            identification      = ''
            type_identification = ''
            identificationID    = ''
            useractive          = 0
            userinactive        = Persons.objects.filter(is_active=False).count()
            for item in Persons.objects.all().order_by('-created_date'):
                if item.is_active:
                    useractive += 1 
                allperson.append({
                    'id'                    : item.pk,
                    'id_user'               : item.user.pk,
                    'name'                  : item.user.get_full_name,
                    'first_name'            : item.user.first_name,
                    'last_name'             : item.user.last_name,
                    'sexe'                  : item.sexe,
                    'phone'                 : item.phone,
                    'email'                 : item.user.email,
                    'address'               : item.address,
                    'codepostal'            : item.codepostal,
                    'country'               : item.country.name if item.country is not None else '',
                    'countryid'             : item.country.pk if item.country is not None else '',
                    'birthday_date'         : str(item.birthday_date),
                    'city'                  : item.city.name if item.city is not None else '',
                    'cityid'                : item.city.pk if item.city is not None else '',
                    'identification'        : identification,
                    'type_identification'   : type_identification,
                    'identificationID'      : identificationID,
                    'pp'                    : item.pp,
                    'is_active'             : item.is_active,
                    'created_date'          : item.created_date,
                    'is_staff'              : item.is_staff,
                    'is_customer'           : item.is_customer
                })
            countalluser = len(allperson)
            allcountry = Country.objects.all()
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/users.html', locals())
        return render(request, 'dashboard/errors/401.html')
    return redirect('core:auth-home')

#User Management Methods
def userStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            print(request.POST['id'])
            user = Persons.objects.get(id=request.POST['id'])
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Delete User Account
def userDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            user = User.objects.get(id=request.POST['id'])
            user.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#MANAGE DEVISES 
def currencyHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            form = CreateCurrencyForm()
            form_update = UpdateCurrencyForm()
            allcurrency = []
            for item in Currency.objects.all():
                allcurrency.append({
                    'id'                            : item.pk,
                    'currency_origin_country'       : item.currency_origin_country,
                    'currency_origin_code'          : item.currency_origin_code,
                    'currency_destination_country'  : item.currency_destination_country,
                    'currency_destination_code'     : item.currency_destination_code,
                    'exchange_rate'                 : item.exchange_rate,
                    'creator'                       : item.creator.get_full_name,
                    'is_active'                     : item.is_active,
                    'is_default'                    : item.is_default,
                    'updated_date'                  : item.updated_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/finance/currency.html', locals())
        return render(request, 'dashboard/errors/401.html')
    return redirect('core:auth-home')

def createCurrencyMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateCurrencyForm(request.POST)
            if form.is_valid():
                devise = form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateCurrencyMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            devise = Currency.objects.get(id=request.POST['id'])
            form = UpdateCurrencyForm(request.POST, instance=devise)
            if form.is_valid():
                devise = form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def currencyStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            devise = Currency.objects.get(id=request.POST['id'])
            if devise.is_active:
                devise.is_active = False
            else:
                devise.is_active = True
            devise.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def currencyActiveMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            devise = Currency.objects.get(id=request.POST['id'])
            if Currency.objects.filter(is_default=True):
                for dev in Currency.objects.filter(is_default=True):
                    dev.is_default = False
                devise.is_default = True
            else:
                devise.is_default = True
            devise.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def currencyDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            devise = Currency.objects.get(id=request.POST['id'])
            devise.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

##############################################################################
################################Gestion des Categories########################
##############################################################################
#Grant Child Category
def categoryGrantChildHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            form = CreateGrantChildCategoryForm()
            allparentcategory = []
            for category in categoriesGrantChild.objects.all():
                allparentcategory.append({
                    'id':category.pk,
                    'name' : category.name,
                    'creator':category.creator.get_full_name,
                    'is_active' : category.is_active,
                    'updated_date' : category.updated_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/grantchildCategory.html', locals())
        return render(request, 'dashboard/errors/401.html')
    return redirect('core:auth-home')

def createGrantChildCategoryMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateGrantChildCategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                print(category)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def grantChildCategoryUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = categoriesGrantChild.objects.get(id=request.POST['id'])
            category.name = request.POST['name']
            category.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def grantChildCategoryStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = categoriesGrantChild.objects.get(id=request.POST['id'])
            if category.is_active:
                category.is_active = False
            else:
                category.is_active = True
            category.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def grantChildCategoryDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = categoriesGrantChild.objects.get(id=request.POST['id'])
            category.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#CildCategory
def categoryChildHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            grantchild = categoriesGrantChild.objects.all()
            allchildcategory = []
            for category in categoriesChild.objects.all():
                allgrantchild = []
                for item in category.grantchilds.all():
                    grantcategory = categoriesGrantChild.objects.get(id=item.pk)
                    allgrantchild.append({
                        'name':grantcategory.name
                    })  
                allchildcategory.append({
                    'id':category.pk,
                    'name' : category.name,
                    'creator':category.creator.get_full_name,
                    'grantchildcategory':allgrantchild,
                    'is_active' : category.is_active,
                    'updated_date' : category.updated_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/childCategory.html', locals())
        return render(request, 'dashboard/errors/401.html')
    return redirect('core:auth-home')

def createChildCategoryMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateChildCategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                if request.POST.getlist('grantchildcategory'):
                    for item in request.POST.getlist('grantchildcategory'):
                        category.grantchilds.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def childCategoryUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = categoriesChild.objects.get(id=request.POST['id'])
            form = UpdateChildCategoryForm({
                    'name':request.POST['name']
                }, instance=category)
            if form.is_valid():
                category = form.save(commit=True)
                if request.POST.getlist('grantchildcategory'):
                    category.grantchilds.clear()
                    for item in request.POST.getlist('grantchildcategory'):
                        category.grantchilds.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def childCategoryStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = categoriesChild.objects.get(id=request.POST['id'])
            if category.is_active:
                category.is_active = False
            else:
                category.is_active = True
            category.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def childCategoryDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = categoriesChild.objects.get(id=request.POST['id'])
            category.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Parent Category
def categoryParentHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            childs = categoriesChild.objects.all()
            allparentcategory = []
            for category in parentCategory.objects.all():
                allchildcategory = []
                for item in category.childs.all():
                    childcategory = categoriesChild.objects.get(id=item.pk)
                    allchildcategory.append({
                        'name':childcategory.name
                    })  
                allparentcategory.append({
                    'id':category.pk,
                    'name' : category.name,
                    'cover' : category.cover,
                    'creator':category.creator.username,
                    'childcategory':allchildcategory,
                    'is_active' : category.is_active,
                    'updated_date' : category.updated_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/parentCategory.html', locals())
        return render(request, 'dashboard/errors/401.html')
    return redirect('core:auth-home')

def createParentCategoryMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateParentCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.save()
                for item in request.POST.getlist('childcategory'):
                    category.childs.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def parentCategoryUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = parentCategory.objects.get(id=request.POST['id'])
            form = UpdateParentCategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                category = form.save(commit=True)
                if request.POST.getlist('childcategory'):
                    category.childs.clear()
                    for item in request.POST.getlist('childcategory'):
                        category.childs.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def parentCategoryStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = parentCategory.objects.get(id=request.POST['id'])
            if category.is_active:
                category.is_active = False
            else:
                category.is_active = True
            category.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def parentCategoryDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = parentCategory.objects.get(id=request.POST['id'])
            category.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

################################################################
####################### Gestion des Marques ####################
################################################################
def brandHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            parentcategory  = parentCategory.objects.all()
            allbrand        = []
            activebrand     = Brands.objects.filter(is_active=True).count()
            inactivebrand   = Brands.objects.filter(is_active=False).count()
            brands          = Brands.objects.all().count()
            
            for brand in Brands.objects.all():
                brandcategory = []
                for item in brand.categories.all():
                    brandcategory.append({
                        'name':item.name
                    })
                allbrand.append({
                    'id'                : brand.pk,
                    'name'              : brand.name,
                    'categories'        : brandcategory,
                    'creator'           : brand.creator.username,
                    'logo'              : brand.logo,
                    'is_active'         : brand.is_active,
                    'is_approved'      : brand.is_approved,
                    'created_date'      : brand.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/brand.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def createBrandMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreatebrandForm(request.POST, request.FILES)
            if form.is_valid():
                brand = form.save()
                for item in request.POST.getlist('categories'):
                    brand.categories.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def brandUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            brand = Brands.objects.get(id=request.POST['id'])
            form = UpdatebrandForm(request.POST, instance=brand)
            if form.is_valid():
                try:
                    brand = form.save(commit=True)
                    if request.POST.getlist('categories'):
                        brand.c.clear()
                        for item in request.POST.getlist('categories'):
                            brand.categories.add(item)
                    if request.FILES['logo']:
                        brand.logo = request.FILES['logo']
                        brand.save() 
                except Exception as e:
                    print(e)
                
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def brandValidateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            brand = Brands.objects.get(id=request.POST['id'])
            if brand.is_approved:
                brand.is_approved = False
            else:
                brand.is_approved = True
            brand.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def brandStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            brand = Brands.objects.get(id=request.POST['id'])
            if brand.is_active:
                brand.is_active = False
            else:
                brand.is_active = True
            brand.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def brandDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            brand = Brands.objects.get(id=request.POST['id'])
            brand.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

##########################################################################################
######################################GESTION DES ATTRIBUTES###############################
###########################################################################################
def attributeHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            colors = DefaultsColors.objects.filter(is_active=True).count()
            materials = DefaultsMaterial.objects.filter(is_active=True).count()
            sizes = DefaultSize.objects.filter(is_active=True).count()
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/attributes.html', locals())
        return render(request, 'dashboard/errors/401.html')
    return redirect('core:auth-home')

#############################COLORS
def colorHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allcolor = []
            for color in DefaultsColors.objects.all():
                allcolor.append({
                    'id':color.pk,
                    'name' : color.name,
                    'creator':color.creator.get_full_name, 
                    'code':color.code,
                    'is_active' : color.is_active,
                    'created_date' : color.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/colors.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def createColorMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            user = User.objects.get(id=request.user.pk)
            form = CreateColorForm({
                    'creator':user,
                    'name':request.POST['name'],
                    'code':request.POST['code'],
                }, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def colorUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            color = DefaultsColors.objects.get(id=request.POST['id'])
            form = UpdateColorForm(
                    {
                        'name':request.POST['name'],
                        'code':request.POST['code']
                    }, 
                    instance=color)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def colorStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            color = DefaultsColors.objects.get(id=request.POST['id'])
            if color.is_active:
                color.is_active = False
            else:
                color.is_active = True
            color.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def colorDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            color = DefaultsColors.objects.get(id=request.POST['id'])
            color.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
            
#############################SIZES
def sizeHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allsize = []
            for size in DefaultSize.objects.all():
                allsize.append({
                    'id':size.pk,
                    'name' : size.name,
                    'creator':size.creator.get_full_name,
                    'is_active' : size.is_active,
                    'created_date' : size.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/sizes.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def createSizeMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            user = User.objects.get(id=request.user.pk)
            form = CreateSizeForm({
                    'creator':user,
                    'name':request.POST['name']
                }, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sizeUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            size = DefaultSize.objects.get(id=request.POST['id'])
            form = UpdateSizeForm(
                    {
                        'name':request.POST['name']
                    }, 
                    instance=size)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sizeStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            size = DefaultSize.objects.get(id=request.POST['id'])
            if size.is_active:
                size.is_active = False
            else:
                size.is_active = True
            size.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sizeDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            size = DefaultSize.objects.get(id=request.POST['id'])
            size.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
            
#############################MATERIALS
def materialHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allmaterial = []
            for material in DefaultsMaterial.objects.all():
                allmaterial.append({
                    'id'                : material.pk,
                    'name'              : material.name,
                    'description'       : material.description,
                    'creator'           : material.creator.get_full_name(),
                    'is_active'         : material.is_active,
                    'created_date'      : material.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/materials.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def createMaterialMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            user = User.objects.get(id=request.user.pk)
            form = CreateMaterialForm({
                    'creator'        : user,
                    'name'          : request.POST['name'],
                    'description'   : request.POST['description']
                }, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def materialUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            material = DefaultsMaterial.objects.get(id=request.POST['id'])
            form = UpdateMaterialForm({
                    'name':request.POST['name'],
                    'description':request.POST['description']
                }, 
                instance=material)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def materialStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            material = DefaultsMaterial.objects.get(id=request.POST['id'])
            if material.is_active:
                material.is_active = False
            else:
                material.is_active = True
            material.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def materialDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            material = DefaultsMaterial.objects.get(id=request.POST['id'])
            material.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

################################################################
####################### Gestion des Fournisseurs ###############
################################################################
def providerHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allprovider         = []
            activeprovider      = Providers.objects.filter(is_approved=True).count()
            inactiveprovider    = Providers.objects.filter(is_approved=False).count()
            providers           = Providers.objects.all().count()
            for item in Providers.objects.all():
                allprovider.append({
                    'id'                : item.pk,
                    'name'              : item.name,
                    'creator'           : item.creator.username,
                    'logo'              : item.logo,
                    'is_active'         : item.is_active,
                    'is_approved'       : item.is_approved,
                    'created_date'      : item.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/provider.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def createProviderMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                form = CreateProviderForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'status':200, 'message':str('Opération réussie!')})
                else:
                    print(form.errors)
                    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

def providerUpdateMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                provider = Providers.objects.get(id=request.POST['id'])
                form = UpdateProviderForm(request.POST, instance=provider)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'status':200, 'message':str('Opération réussie!')})
                return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

def providerValidateMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                provider = Providers.objects.get(id=request.POST['id'])
                if provider.is_approved:
                    provider.is_approved = False
                else:
                    provider.is_approved = True
                provider.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

def providerStatusMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                provider = Providers.objects.get(id=request.POST['id'])
                if provider.is_active:
                    provider.is_active = False
                else:
                    provider.is_active = True
                provider.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

def providerDeleteMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                provider = Providers.objects.get(id=request.POST['id'])
                provider.delete()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

#####################################################################  
#############################PRODUCTS################################
#####################################################################
def productHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            products                    = Products.objects.all().count()
            productinactive             = Products.objects.filter(is_active=False).count()
            productactive               = Products.objects.filter(is_active=True).count()
            productfavorite             = Products.objects.all().count()
            product_form                = CreateProductForm()
            product_update_form         = UpdateProductForm()
            all_brand                   = Brands.objects.filter(is_active=True)
            all_provider                = Providers.objects.filter(is_active=True)
            all_parent_cat              = parentCategory.objects.filter(is_active=True)
            all_color                   = DefaultsColors.objects.filter(is_active=True)
            all_size                    = DefaultSize.objects.filter(is_active=True)
            all_material                = DefaultsMaterial.objects.filter(is_active=True)
            allproduct                  = []
            for product in Products.objects.all().order_by('-id'):
                is_attribut         = False
                is_flash_sell       = False
                sizes               = []
                colors              = []
                materials           = []
                images              = []
                videos              = []
                attribut            = None
                if ProductCaracteristque.objects.filter(product=product):
                    is_attribut = True
                    attribut = ProductCaracteristque.objects.get(product=product)
                    for item in attribut.size.all():
                        sizes.append({
                            'id'        : item.pk,
                            'name'      : item.name
                        })
                    for item in attribut.color.all():
                        colors.append({
                            'id'        : item.pk,
                            'name'      : item.name,
                            'code'      : item.code
                        })
                    for item in attribut.material.all():
                        materials.append({
                            'id'            : item.pk,
                            'name'          : item.name,
                            'description'   : item.description
                        })
                    
                    #manage attachs
                    for item in product.images.all():
                        images.append({
                            'id'            : item.pk,
                            'image'         : item.image,
                            'label'         : item.label
                        })
                    for item in product.videos.all():
                        images.append({
                            'id'            : item.pk,
                            'video'         : item.video,
                            'label'         : item.label
                        })
                else:
                    is_attribut = False
                if PromotionsProducts.objects.filter(product=product):
                    is_flash_sell = True
                else:
                    is_flash_sell = False
                allproduct.append({
                    'id'                    : product.pk,
                    'name'                  : product.name,
                    'description'           : product.description,
                    'category'              : product.category,
                    'brand'                 : product.brand,
                    'provider'              : product.provider,
                    'providerid'            : product.provider.pk,
                    'quantity'              : product.quantity,
                    'price'                 : product.price,
                    'discount'              : product.discount,
                    'is_active'             : product.is_active,
                    'created_date'          : product.created_date,
                    'presentation'          : product.presentation,
                    'is_attribut'           : is_attribut,
                    'attribut'              : attribut,
                    'sizes'                 : sizes,
                    'colors'                : colors,
                    'materials'             : materials,
                    'is_flash_sell'         : is_flash_sell,
                    'is_approved'           : product.is_approved,
                    'weigth'                : product.weigth,
                    'height'                : product.height,
                    'width'                 : product.width,
                    'depth'                 : product.depth,
                    'images'                : images,
                    'videos'                : videos,
                    'cover'                 : product.images.first(),
                    'commission_company'    : Decimal(product.commission_company),
                })
            currency = currencyToggle(request) 
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/product/product.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

#compress image function
def CompressImage(image_field):
    img = Image.open(image_field)
    
    # Convert to RGB if not already, to handle various image formats consistently
    if img.mode != 'RGB':
        img = img.convert('RGB')

    thumb_io = BytesIO()
    # Adjust quality as needed (0-100)
    img.save(thumb_io, 'JPEG', quality=70) 
    
    # Create a new InMemoryUploadedFile from the compressed data
    new_image = InMemoryUploadedFile(
        thumb_io,
        'FileField',
        f"{image_field.name.split('.')[0]}.jpg",
        'image/jpeg', 
        thumb_io.tell(),
        None
    )
    return new_image
        
#Creer Un Produit
def createProductMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                form = CreateProductForm(request.POST)
                if form.is_valid():
                    product = form.save()
                    if 'weigth' in request.POST:
                        product.weigth = request.POST['weigth']
                    
                    if 'height' in request.POST:
                        product.height = request.POST['height']
                    
                    if 'width' in request.POST:
                        product.width = request.POST['width']
                    
                    if 'depth' in request.POST:
                        product.depth = request.POST['depth']

                    if 'brand' in request.POST and request.POST['brand'] != '':
                        product.brand = Brands.objects.get(id=int(request.POST['brand']))

                    if request.FILES.getlist('images'):
                        for item in request.FILES.getlist('images'):
                            #compress and record images 
                            newproductimage = CompressImage(item)
                            imageproduct = ProductImages.objects.create(
                                creator     = request.user,
                                label       = f'Image-{product.name}',
                                image       = newproductimage
                            )
                            product.images.add(imageproduct)
                    
                    product.save()
                    return JsonResponse({'status':200, 'message':str('Opération réussie!')})
                else:
                    print(form.errors)
                    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

#Mettre a jour un Produit
def productUpdateMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                product = Products.objects.get(id=request.POST['product'])
                form = UpdateProductForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    newproduct = form.save(commit=False)
                    if 'category' in request.POST and request.POST['category'] != '':
                        newproduct.category = request.POST['category']

                    if 'weigth' in request.POST:
                        newproduct.weigth = request.POST['weigth']
                    
                    if 'height' in request.POST:
                        newproduct.height = request.POST['height']
                    
                    if 'width' in request.POST:
                        newproduct.width = request.POST['width']
                    
                    if 'depth' in request.POST:
                        newproduct.depth = request.POST['depth']
                        
                    if 'brand' in request.POST and request.POST['brand'] != '':
                        newproduct.brand = Brands.objects.get(id=int(request.POST['brand']))
                
                    if request.FILES.getlist('images'):
                        for item in request.FILES.getlist('images'):
                            #compress and record images 
                            newproductimage = CompressImage(item)
                            imageproduct = ProductImages.objects.create(
                                creator     = request.user,
                                label       = f'Image-{product.name}',
                                image       = newproductimage
                            )
                            newproduct.images.add(imageproduct)
                            
                    newproduct.save()
                    return JsonResponse({'status':200, 'message':str('Opération réussie!')})
                else:
                    print(form.errors)
                    return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

#Bloquer ou debloquer un Produit
def productStatusMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                product = Products.objects.get(id=request.POST['id'])
                if product.is_active:
                    product.is_active = False
                else:
                    product.is_active = True
                product.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

#Approuver un Produit
def validateProductMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request): 
            if request.method == 'POST':
                product = Products.objects.get(id=request.POST['id'])
                if product.is_approved:
                    product.is_approved = False
                    product.approved_by = None
                else:
                    product.is_approved = True
                    product.approved_by = request.user
                product.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

#Supprimer un Produit
def productDeleteMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                product = Products.objects.get(id=request.POST['id'])
                product.delete()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

# get sub catregory
def childCategoryMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == "POST":
                html = ''
                get_parent = parentCategory.objects.get(id=int(request.POST['parent_value']))
                childs = get_parent.childs.all()
                for child in childs:
                    html += "<option value=" + str(child.pk) + ">" + str(child.name) + "</option>"
                return HttpResponse(json.dumps({'status' : 200, 'sub_cat': html}), content_type='application/json')
            return JsonResponse({"status":500, "message":"une erreur cest produite"})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

# get grant category
def grantCategoryMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == "POST":
                html = ''
                get_child = categoriesChild.objects.get(id=int(request.POST['child_value']))
                grant_childs = get_child.grantchilds.all()
                for grant in grant_childs:
                    html += "<option value=" + str(grant.pk) + ">" + str(grant.name) + "</option>"
                return HttpResponse(json.dumps({'status' : 200, 'grant_cat': html}), content_type='application/json')
            return JsonResponse({"status":500, "message":"une erreur cest produite"})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

#Create Product Presentation
def createPresentationMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                product = Products.objects.get(id=int(request.POST['id']))
                product.presentation = request.POST['presentation']
                product.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifier. Vous n\'êtes pas reconnu par le système.')}) 

#Update Product Presentation
def updatePresentationMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            product = Products.objects.get(id=int(request.POST['id']))
            product.presentation = request.POST['presentation']
            product.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Product Attributes
def createAttributMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateCaractProductForm(request.POST)
            if form.is_valid():
                product_caract = form.save()
                for item in request.POST.getlist('size'):
                    product_caract.size.add(item)
                for item in request.POST.getlist('material'):
                    product_caract.material.add(item)
                for item in request.POST.getlist('color'):
                    product_caract.color.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateAttributMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            pass
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Product Flash
def addFlashProductMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = AddFlashProductForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Delete Product Flash
def deleteFlashProductMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            product = Products.objects.get(id=request.POST['id'])
            flash = PromotionsProducts.objects.get(product=product)
            flash.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

###################################################################################################
################################## GESTION DES POINTS DE LIVRAISONS ###############################
###################################################################################################
def deliveredZoneHomeMethod(request):
    if is_auth(request): 
        if is_superuser(request):
            allzone          = []
            approvedzone     = CompanyDeliveryZone.objects.filter(is_approved=True).count()
            inapprovedzone   = CompanyDeliveryZone.objects.filter(is_approved=False).count()
            for zone in CompanyDeliveryZone.objects.all().order_by('-created_date'):
                allzone.append({
                    'id'                        : zone.pk,
                    'title'                     : zone.title,
                    'description'               : zone.description,
                    'price'                     : zone.price,
                    'googlemap'                 : zone.googlemap,
                    'is_active'                 : zone.is_active,
                    'is_approved'               : zone.is_approved,
                    'created_date'              : zone.created_date,
                })
            allcountry = Country.objects.all()
            currency = currencyToggle(request) 
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/deliveredzone/zone.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def deliveredCreate(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateDeliveredZoneForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deliveredUpdate(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            zone = CompanyDeliveryZone.objects.get(id=request.POST['id'])
            form = UpdateDeliveredZoneForm(request.POST, instance=zone)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deliveredStatus(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            zone = CompanyDeliveryZone.objects.get(id=request.POST['id'])
            if zone.is_active:
                zone.is_active = False
            else:
                zone.is_active = True
            zone.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deliveredValidate(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            zone = CompanyDeliveryZone.objects.get(id=request.POST['id'])
            if zone.is_approved:
                zone.is_approved = False
                zone.approved_by = None
            else:
                zone.is_approved = True
                zone.approved_by = request.user
            zone.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deliveredDelete(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            zone = CompanyDeliveryZone.objects.get(id=request.POST['id'])
            zone.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#################################################################################
###################################FOLLOW UP DELIVERED###########################
#################################################################################
def traficHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            alltrafic = []
            starttrafic = Commands.objects.filter(is_delivery=True, is_pay=True, is_delivery_start=True).count()
            endtrafic = Commands.objects.filter(is_delivery=True, is_pay=True, is_delivery_end=True).count()
            for trafic in Commands.objects.all().order_by('-created_date'):
                all_product = []
                if ProductBaskets.objects.filter(basket=trafic.basket):
                    for baskitem in ProductBaskets.objects.filter(basket=trafic.basket):
                        all_product.append({
                            'name'      : baskitem.product.name,
                            'cover'     : baskitem.product.images[0],
                            'provider'  : baskitem.product.provider.name
                        })
                if trafic.product:
                    all_product.append({
                        'name'      : trafic.product.name,
                        'cover'     : trafic.product.images[0],
                        'seller'    : trafic.product.provider.name
                    })
                alltrafic.append({
                    'id'                    : trafic.pk,
                    'distributionzone'      : trafic.delivery.title,
                    'customer'              : trafic.customer.user.get_full_name(),
                    'products'              : all_product,
                    'to'                    : trafic.customer.address,
                    'is_delivery'           : trafic.is_delivery,
                    'is_delivery_start'     : trafic.is_delivery_start,
                    'is_delivery_end'       : trafic.is_delivery_end,
                    'delivery_start_datetime' : trafic.delivery_start_datetime,
                    'delivery_end_datetime'   : trafic.delivery_end_datetime,
                    'is_pay'                : trafic.is_pay
                })
            numberalltrafic = len(alltrafic)
            currency = currencyToggle(request) 
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/deliveredzone/trafic.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def traficDeliveredStart(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            trafic = Commands.objects.get(id=request.POST['id'])
            trafic.is_delivery_start = True
            trafic.delivery_start_datetime = datetime.now()
            trafic.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def traficDeliveredEnd(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            trafic = Commands.objects.get(id=request.POST['id'])
            trafic.is_delivery_end = True
            trafic.delivery_end_datetime = datetime.now()
            trafic.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#####################################################################################
################################## BILLING MANAGEMENT ###############################
#####################################################################################
def invoiceHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allinvoice = []
            for invoice in Commands.objects.filter(is_pay=True): 
                allinvoice.append({
                    'id'                    : invoice.pk,
                    'customer_name'         : invoice.customer.user.get_full_name(),
                    'created_date'          : invoice.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/invoice/invoices.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def invoiceTemplateMethod(request, command_id):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            StaticUrl = STATIC_URL
            commandinfo = dict()
            company = Company.objects.first()
            command = Commands.objects.get(id=int(command_id))
            allproduct = []
            for item in ProductBaskets.objects.filter(basket=command.basket):
                allproduct.append({
                    'name'      : item.product.name,
                    'total'     : item.one_price,
                    'quantity'  : item.quantity
                })
            commandinfo = {
                'id'                    : command.pk,
                'customer_name'         : command.customer.user.get_full_name(),
                'customer_phone'        : command.customer.phone,
                'customer_address'      : command.customer.address,
                'created_date'          : command.created_date,
                'company_name'          : company.name,
                'company_address'       : company.addresses.first(),
                'company_phone'         : company.phones.first(),
                'items'                 : allproduct,
                'item_number'           : command.item_number,
                'total_price'           : round(command.total_price, 0)
            }
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass

            pdf = render_to_pdf("dashboard/invoice/template.html", locals())

            if pdf:
                response = HttpResponse(pdf,content_type='application/pdf')
                filename = "FRIPME_CMD_%s.pdf" %(command.pk)
                content = "inline; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                return response
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

############################################################################################
######################################### FINANCE ##########################################
############################################################################################
##############Finance Provider
def homeFinanceProviderMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allfinanceprovider = []
            globalamount = 0
            amountreceive = 0
            pendingamount = 0
            for finance in Finances.objects.all():
                if finance.provider_is_pay:
                    amountreceive = Decimal(amountreceive) + Decimal(finance.provider_commission)
                else:
                    pendingamount = Decimal(amountreceive) + Decimal(finance.provider_commission)
                    
                allfinanceprovider.append({
                    'id'                    : finance.pk,
                    'logo'                  : finance.command.product.provider.logo,
                    'provider'              : finance.command.product.provider.name,
                    'command'               : finance.command.pk,
                    'transaction_date'      : finance.created_date,
                    'provider_commission'   : Decimal(finance.provider_commission),
                    'provider_is_pay'       : finance.provider_is_pay,
                })
            globalamount = amountreceive + pendingamount
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/finance/financeprovider.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def statusFinanceProviderMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            transaction = Finances.objects.get(id=request.POST['id'])
            if transaction.provider_is_pay:
                transaction.provider_is_pay = False
            else:
                transaction.provider_is_pay = True
            transaction.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

##################Finance Product
def homeFinanceProductMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allfinanceproduct = []
            globalamount        = 0
            paymentcomplete     = 0
            paymentcancel       = 0
            product_infos       = ''
            commission_company  = 0
            company             = Company.objects.first()
            for command in Commands.objects.all():
                commission_per_product = 0
                for item in ProductBaskets.objects.filter(basket=command.basket):
                    commission_company      = Decimal(item.product.commission_company) * Decimal(item.one_price) / 100
                    commission_per_product  += (item.one_price - commission_company)
                    if item.is_pay:
                        paymentcomplete += round((item.one_price - commission_company), 0)
                    else:
                        paymentcomplete += round((item.one_price - commission_company), 0)
                    allfinanceproduct.append({
                        'id'                : item.pk,
                        'customer'          : item.basket.customer.user.get_full_name(),
                        'product'           : item.product.name,
                        'transaction_date'  : command.created_date,
                        'transaction_price' : round(item.one_price - commission_company, 0),
                        'customer_has_pay'  : item.is_pay,
                    })
            globalamount = paymentcomplete + paymentcancel
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/finance/financeproduct.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def productFinanceStatus(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            product_basket = ProductBaskets.objects.get(id=request.POST['id'])
            if product_basket.is_pay:
                product_basket.is_pay = False
            else:
                product_basket.is_pay = True
            product_basket.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#################Finance Distributor
def homeFinanceDistributorMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allfinancedistributor = []
            globalamount = 0
            amountreceive = 0
            pendingamount = 0
            for finance in Finances.objects.all():
                if finance.delivered_is_pay:
                    amountreceive   += Decimal(amountreceive) + Decimal(finance.delivered_commission)
                else:
                    pendingamount   += Decimal(amountreceive) + Decimal(finance.delivered_commission)
                distributor_command = CompanyDeliveryZone.objects.get(command=finance.command)
                allfinancedistributor.append({
                    'id'                : finance.pk,
                    'logo'              : '',
                    'distributor'       : distributor_command.title,
                    'transaction_date'  : finance.created_date,
                    'delivered_price'   : Decimal(finance.delivered_commission),
                    'delivered_is_pay'  : finance.delivered_is_pay,
                })
            globalamount = amountreceive + pendingamount
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/finance/financedistributor.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def distributorFinanceStatus(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            financedistributor = Finances.objects.get(id=request.POST['id'])
            if financedistributor.delivered_is_pay:
                financedistributor.delivered_is_pay = False
            else:
                financedistributor.delivered_is_pay = True
            financedistributor.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#all payment
def homePaymentMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            alltransaction = []
            totalcompany = 0
            totalprovider = 0
            totalbank = 0
            totaldistributor = 0
            for finance in Finances.objects.order_by('-id').all():
                if finance.command.product.commission_provider > 0:
                    totalprovider += Decimal(totalprovider) + Decimal(finance.command.product.commission_provider)
                if finance.company_commission > 0:
                    totalcompany += finance.company_commission
                if finance.bank_commission > 0:
                    totalbank += finance.bank_commission
                if finance.delivered_commission > 0:
                    totaldistributor += finance.delivered_commission
                
                alltransaction.append({
                    'id'                        : finance.pk,
                    'command'                   : finance.command.pk,
                    'company_commission'        : finance.company_commission,
                    'bank_commission'           : finance.bank_commission,
                    'distributor_commission'    : finance.delivered_commission,
                    'transaction_date'          : finance.created_date,
                    'bank_is_pay'               : finance.bank_is_pay,
                    'company_is_pay'            : finance.company_is_pay,
                    'delivered_is_pay'          : finance.delivered_is_pay
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/finance/payment.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

#all transaction
def homeTransactionMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            alltransaction = []
            totalpayment = 0
            transactioncomplete = 0
            transactionpending = 0
            transactionfailed = 0
            for item in Payments.objects.order_by('-created_date'):
                header_auth = {
                    "Accept"        : "application/json"
                }
                generatepayment = requests.get(MY_COOL_PAY_BASE_URL + MY_COOL_PAY_PUBLIC_KEY + '/checkStatus/' + item.transaction_ref, headers=header_auth)
                response_deel = generatepayment.json()
                if response_deel['status'] == 'success':
                    if response_deel['transaction_status'] == 'SUCCESS':
                        transactioncomplete += round(item.amount, 0)
                    if response_deel['transaction_status'] == 'PENDING':
                        transactionpending += round(item.amount, 0)
                    if response_deel['transaction_status'] == 'FAILED':
                        transactionfailed += round(item.amount, 0)
                    alltransaction.append({
                        'id'                        : item.pk,
                        'command'                   : item.command.pk,
                        'amount'                    : item.amount,
                        'description'               : item.description,
                        'transaction_date'          : item.created_date,
                        'transaction_status'        : response_deel['transaction_status'],
                    })

                    #update payment table
                    item.transactionStatus = response_deel['transaction_status']
                    item.save()
            totaltransaction = transactioncomplete + transactionpending + transactionfailed
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/finance/transaction.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

#####################################################################################
################################# MANAGES CUSTOMERS #################################
#####################################################################################
def customerHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allcustomer                 = []
            countallcustomer            = Persons.objects.filter(is_customer=True).count()
            activecustomer              = Persons.objects.filter(is_customer=True, is_active=True).count()
            unactivecustomer            = Persons.objects.filter(is_customer=False, is_active=False).count()
            for customer in Persons.objects.filter(is_customer=True):
                countryname = Country.objects.get(id=customer.country.pk)
                allcustomer.append({
                    'id'                    : customer.pk,
                    'first_name'            : customer.user.first_name,
                    'last_name'             : customer.user.last_name,
                    'sexe'                  : customer.sexe,
                    'phone'                 : customer.phone,
                    'email'                 : customer.user.email,
                    'address'               : customer.address,
                    'country'               : countryname,
                    'countryid'             : customer.country.pk,
                    'birthday_date'         : str(customer.birthday_date),
                    'city'                  : customer.city,
                    'pp'                    : customer.pp,
                    'is_active'             : customer.is_active,
                    'created_date'          : customer.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/customer/customerprofil.html', locals())
        return render(request, 'dashboard/errors/401.html')
    return redirect('core:auth-home')

#Customer Update Status
def customerStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            customer = Persons.objects.get(id=request.POST['id'])
            if customer.is_active:
                customer.is_active = False
            else:
                customer.is_active = True
            customer.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#################Finance Customer
def homeFinanceCustomerMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allfinancecustomer = []
            for customer in Persons.objects.all():
                cancelpayment       = 0
                successpayment      = 0
                countsuccesstrans   = 0
                countfailtrans      = 0
                traficglobal        = 0
                for commandcustomer in Commands.objects.filter(customer=customer):
                    traficglobal += 1
                    if commandcustomer.is_pay:
                        successpayment += commandcustomer.total_price
                        countsuccesstrans += 1
                    else:
                        cancelpayment += commandcustomer.total_price
                        countfailtrans += 1
                allfinancecustomer.append({
                    'id'                : customer.pk,
                    'pp'                : customer.pp,
                    'name'              : customer.user.get_full_name,
                    'phone'             : customer.phone,
                    'successpayment'    : successpayment,
                    'cancelpayment'     : cancelpayment,
                    'traficglobal'      : traficglobal,
                    'countsuccesstrans' : countsuccesstrans,
                    'countfailtrans'    : countfailtrans,
                    'is_active'         : customer.is_active,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/customer/customerfinance.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

def customerFinanceStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            customer = Persons.objects.get(id=request.POST['id'])
            if customer.is_active:
                customer.is_active = False
            else:
                customer.is_active = True
            customer.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#################################################################################################
#################################### MANAGES CHATBOOT AND AUTO MESSAGES #########################
#################################################################################################
def chatBootHomeMethod(request):
    if is_auth(request):
        if is_superuser(request):
            alldialog = Dialogs.objects.filter(opponent=request.user)   
            dialogs = []
            for dialog in alldialog:
                lastmessage = Messages.objects.filter(idchat=dialog.pk)
                dialogs.append({
                    'id'                : dialog.pk,
                    'owner_id'          : dialog.owner.pk,
                    'owner_name'        : dialog.owner.last_name,
                    'owner_email'       : dialog.owner.email,
                    'owner_online'      : dialog.owner_is_online,
                    'opponent_id'       : dialog.opponent.pk,
                    'opponent_name'     : dialog.opponent.last_name,
                    'opponent_email'    : dialog.opponent.email,
                    'opponent_online'   : dialog.opponent_is_online,
                    'is_active'         : dialog.is_active,
                    'msgcontent'        : lastmessage[0].content if lastmessage else str('Pas de message'),
                    'msgcontenttime'    : lastmessage[0].updated_date if lastmessage else ''
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/customer/chatboot.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

#############################GESTION DU CHAT AUTOMATIQUE
def AutoMessageHome(request):
    if is_auth(request):
        if is_superuser(request):
            allmessage                  = []
            countmessage                = 0
            sellers                     = Brands.objects.all()
            if is_superuser(request) or is_staff(request):
                automessages = AutoMessage.objects.all()
            if is_staff(request):
                seller          = Brands.objects.get(person=Persons.objects.get(user=request.user))
                automessages    = AutoMessage.objects.filter(seller=seller)
            for message in automessages:
                allmessage.append({
                    'id'                : message.pk,
                    'creator'            : message.creator.get_full_name,
                    'seller'            : message.seller.name,
                    'initial'           : message.call_message,
                    'response'          : message.resp_message,
                    'pp'                : message.seller.person.pp,
                    'is_active'         : message.is_active,
                    'created_date'      : message.created_date 
                })
                countmessage = len(allmessage)
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/support/auto-message.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

################################ADVERTIZING MANAGEMENT 
def advertizingHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allbanner           = BannerPubs.objects.all().count()
            allpub              = SponsoringProducts.objects.all().count()
            allbooking          = SponsoringBooking.objects.all().count()
            allsponsoringzone   = SponsoringManageBlock.objects.all().count()
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/advertizing/advertizing.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

###################MANAGE BANNER #########################
def bannerHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allbanner = []
            for banner in BannerPubs.objects.all():
                allbanner.append({
                    'id'            : banner.pk,
                    'title'         : banner.title,
                    'is_external'   : banner.is_external,
                    'link'          : banner.link,
                    'cover'         : banner.cover,
                    'is_active'     : banner.is_active
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/advertizing/banner.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createBannerMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = createBannerForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def bannerUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            banner = BannerPubs.objects.get(id=request.POST['id'])
            form = updateBannerForm(request.POST, request.FILES, instance=banner)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def bannerStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            banner = BannerPubs.objects.get(id=request.POST['id'])
            if banner.is_active:
                banner.is_active = False
            else:
                banner.is_active = True
            banner.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def bannerDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            banner = BannerPubs.objects.get(id=request.POST['id'])
            banner.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

###################MANAGE SPONSORING #########################
def sponsoringHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allprovider     = Providers.objects.filter(is_approved=True)
            allproduct      = Products.objects.filter(is_approved=True)
            allbooking      = SponsoringBooking.objects.filter(is_active=True)
            allsponsoring   = []
            for sponsoring in SponsoringProducts.objects.all():
                allsponsoring.append({
                    'id'            : sponsoring.pk,
                    'seller'        : sponsoring.seller,
                    'product'       : sponsoring.product,
                    'booking'       : sponsoring.booking,
                    'start_date'    : sponsoring.start_date,
                    'end_date'      : sponsoring.end_date,
                    'is_active'     : sponsoring.is_active
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/sponsoring/sponsoring.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createSponsoringMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = createSponsoringForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            sponsoring = SponsoringProducts.objects.get(id=request.POST['id'])
            form = updateSponsoringForm(request.POST, instance=sponsoring)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            sponsoring = SponsoringProducts.objects.get(id=request.POST['id'])
            if sponsoring.is_active:
                sponsoring.is_active = False
            else:
                sponsoring.is_active = True
            sponsoring.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            sponsoring = SponsoringProducts.objects.get(id=request.POST['id'])
            sponsoring.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringGetSellerProductMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            store = Persons.objects.get(id=request.POST['storeid'])
            products = Products.objects.filter(store=store, is_active=True)
            all_product = []
            for product in products:
                all_product.append({
                    'id':product.pk,
                    'name':product.name
                })
            return JsonResponse({'status':200, 'message':str('Opération réussie!'), 'results':all_product })
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

###################MANAGE SPONSORING BOOKING #########################
def sponsoringBookingHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allblock                = SponsoringManageBlock.objects.all()
            allsponsoringbooking    = []
            for booking in SponsoringBooking.objects.all():
                allsponsoringbooking.append({
                    'id'                    : booking.pk,
                    'name'                  : booking.name,
                    'code_zone'             : booking.code_zone,
                    'periode'               : booking.periode,
                    'sponsoring_price'      : booking.sponsoring_price,
                    'is_active'             : booking.is_active
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/sponsoring/booking.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createSponsoringBookingMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = createSponsoringBookingForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringBookingUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            booking = SponsoringBooking.objects.get(id=request.POST['id'])
            form = updateSponsoringBookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringBookingStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            booking = SponsoringBooking.objects.get(id=request.POST['id'])
            if booking.is_active:
                booking.is_active = False
            else:
                booking.is_active = True
            booking.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringBookingDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            booking = SponsoringBooking.objects.get(id=request.POST['id'])
            booking.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

###################MANAGE SPONSORING BLOCK #########################
def sponsoringZoneHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allsponsoringzone       = []
            for zone in SponsoringManageBlock.objects.all():
                allsponsoringzone.append({
                    'id'            : zone.pk,
                    'name'          : zone.name,
                    'code'          : zone.code,
                    'is_active'     : zone.is_active
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/sponsoring/sponsoringzone.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createSponsoringZoneMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = createSponsoringZoneForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringZoneUpdateMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            booking = SponsoringManageBlock.objects.get(id=request.POST['id'])
            form = updateSponsoringZoneForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringZoneStatusMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            zone = SponsoringManageBlock.objects.get(id=request.POST['id'])
            if zone.is_active:
                zone.is_active = False
            else:
                zone.is_active = True
            zone.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def sponsoringZoneDeleteMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            zone = SponsoringManageBlock.objects.get(id=request.POST['id'])
            zone.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})  

####################################################################################
################################ BLOG MANAGEMENT ###################################
####################################################################################
def blogHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allblog = []
            countlike       = 0
            countcomment    = 0
            for item in Blog.objects.all():
                countlike       += BlogLike.objects.filter(blog=item, is_active=True, is_like=True).count()
                countcomment    += BlogComment.objects.filter(blog=item, is_active=True, is_block=False).count()
                allblog.append({
                    'id'                : item.pk,
                    'title'             : item.title,
                    'label'             : item.label,
                    'author'            : item.author.get_full_name(), 
                    'description'       : item.description,
                    'cover'             : item.cover,
                    'is_approuved'      : item.is_approuved,
                    'approuved_by'      : item.approuved_by if item.approuved_by is not None else '',
                    'is_active'         : item.is_active,
                    'created_date'      : item.created_date,
                })
            countblog                   = Blog.objects.all().count()
            countapprouvedblog          = Blog.objects.filter(is_approuved=True).count()
            countapprouvedpendingblog   = Blog.objects.filter(is_approuved=False).count()
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/blog/blog.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('master:auth-home-user')

def createBlogMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateBlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save()
                if request.FILES.getlist('images'):
                    for item in request.FILES.getlist('images'):
                        image = BlogImage.objects.create(
                            cover = item
                        )
                        blog.images.add(image)
                if request.FILES.getlist('videos'):
                    for item in request.FILES.getlist('videos'):
                        video = BlogVideo.objects.create(
                            video = item
                        )
                        blog.videos.add(video)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateBlogMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            blog = Blog.objects.get(id=request.POST['id'])
            form = UpdateBlogForm(
                {
                    'title'             : request.POST['title'],
                    'label'             : request.POST['label'],
                    'description'       : request.POST['description'],
                    'cover'             : request.FILES['cover'] if 'cover' in request.FILES else blog.cover
                }, 
            instance=blog)
            if form.is_valid():
                newblog = form.save()
                if request.FILES.getlist('images'):
                    newblog.images.clear()
                    for item in request.FILES.getlist('images'):
                        image = BlogImage.objects.create(
                            cover = item
                        )
                        newblog.images.add(image)
                if request.FILES.getlist('videos'):
                    newblog.videos.clear()
                    for item in request.FILES.getlist('videos'):
                        video = BlogVideo.objects.create(
                            video = item
                        )
                        newblog.videos.add(video)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusBlogMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            blog = Blog.objects.get(id=request.POST['id'])
            if blog.is_active == True:
                blog.is_active = False
            else:
                blog.is_active = True
            blog.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def validateBlogMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            blog = Blog.objects.get(id=request.POST['id'])
            if blog.is_approuved == True:
                blog.is_approuved   = False
                blog.approuved_by   = None
            else:
                blog.is_approuved   = True
                blog.approuved_by   = request.user
            blog.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteBlogMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            blog = Blog.objects.get(id=request.POST['id'])
            blog.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    
#Manage Comment Blog
def blogCommentHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allcomment = []
            for item in BlogComment.objects.all():
                allcomment.append({
                    'id'                : item.id,
                    'author'            : item.person.user.get_full_name(),
                    'blog'              : item.blog.title,
                    'comment'           : item.comment,
                    'is_block'          : item.is_block,
                    'is_active'         : item.is_active,
                    'created_date'      : item.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/blog/blogcomment.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('master:auth-home-user')

def blogCommentValidationMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            comment = BlogComment.objects.get(id=request.POST['id'])
            if comment.is_block == True:
                comment.is_block   = False
            else:
                comment.is_block   = True
            comment.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteBlogCommentMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            comment = BlogComment.objects.get(id=request.POST['id'])
            comment.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

####################################################################################
################################ FAQ CATEGORY MANAGEMENT ###################################
####################################################################################
def faqCategoryHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allcategory = []
            for item in FAQCategory.objects.all():
                allcategory.append({
                    'id'            : item.pk,
                    'title'         : item.title,
                    'description'   : item.description, 
                    'is_active'     : item.is_active,
                    'created_date'  : item.created_date,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/faq/categoryfaq.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createFaqCategoryMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateFaqCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateFaqCategoryMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = FAQCategory.objects.get(id=request.POST['id'])
            form = UpdateFaqCategoryForm(
                {
                    'title'             : request.POST['title'],
                    'description'       : request.POST['description'],
                }, 
            instance=category)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusFaqCategoryMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = FAQCategory.objects.get(id=request.POST['id'])
            if category.is_active:
                category.is_active = False
            else:
                category.is_active = True
            category.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteFaqCategoryMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            category = FAQCategory.objects.get(id=request.POST['id'])
            category.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

####################################################################################
################################ FAQ MANAGEMENT ###################################
####################################################################################
def faqHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allfaq = []
            countreaction = 0
            for item in FAQ.objects.all():
                countreaction = item.numberlike + item.numberunlike
                allfaq.append({
                    'id'            : item.pk,
                    'title'         : item.title,
                    'label'         : item.label,
                    'category'      : item.category.title,
                    'categoryid'    : item.category.pk,
                    'subject'       : item.subject,
                    'content'       : item.content,
                    'slug'          : item.slug,
                    'created_date'  : item.created_date,
                    'numberlike'    : item.numberlike,
                    'numberunlike'  : item.numberunlike,
                    'is_active'     : item.is_active,
                    'is_approved'  : item.is_approved
                })
            countfaq                  = FAQ.objects.all().count()
            countapprovedfaq          = FAQ.objects.filter(is_approved=True).count()
            countapprovedpendingfaq   = FAQ.objects.filter(is_approved=False).count()
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/faq/faq.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createFaqMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateFaqForm(request.POST)
            if form.is_valid():
                faq = form.save()
                if 'file' in request.FILES:
                    faq.file = request.FILES['file']
                    faq.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateFaqMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            faq = FAQ.objects.get(id=request.POST['id'])
            form = UpdateFaqForm(
                {
                    'category'          : request.POST['category'],
                    'title'             : request.POST['title'],
                    'label'             : request.POST['label'],
                    'subject'           : request.POST['subject'],
                    'content'           : request.POST['content']
                }, 
            instance=faq)
            if form.is_valid():
                newfaq = form.save()
                if 'file' in request.FILES:
                    newfaq.file = request.FILES['file']
                    newfaq.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusFaqMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            faq = FAQ.objects.get(id=request.POST['id'])
            if faq.is_active:
                faq.is_active = False
            else:
                faq.is_active = True
            faq.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def validateFaqMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            faq = FAQ.objects.get(id=request.POST['id'])
            if faq.is_approved:
                faq.is_approved   = False
                faq.approved_by   = None
            else:
                faq.is_approved   = True
                faq.approved_by   = request.user
            faq.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteFaqMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            faq = FAQ.objects.get(id=request.POST['id'])
            faq.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

####################################################################################
################################ SUPPORT MANAGEMENT ###############################
####################################################################################

############################support Ticket Management ############################
#Home
def supportHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allticket = []
            for item in customerSupportTicket.objects.all():
                countmessage = 0
                for mess in ticketMessage.objects.filter(ticket=item):
                    countmessage += 1
                allticket.append({
                    'id'                    : item.pk,
                    'owner_name'            : item.owner.user.get_full_name(),
                    'owner_pp'              : item.owner.pp,
                    'resume'                : item.resume,
                    'command'               : 'Command Nº {}'.format(item.command.pk) if item.command is not None else '',
                    'service'               : item.service.title,
                    'description'           : item.description,
                    'countmessage'          : countmessage,
                    'progression_status'    : item.progression_status

                })
            countticket = len(allticket)
            countticketpending      = customerSupportTicket.objects.filter(is_resolv=False).count()
            countticketclose        = customerSupportTicket.objects.filter(is_resolv=True).count()
            countpendingcustomer    = customerSupportTicket.objects.filter(progression_status=1).count()
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/support/support.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

####################################Home Support Service########################################
def supportServiceHomeMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allsupportservice = []
            for item in customerSupportService.objects.all():
                allsupportservice.append({
                    'id'                        : item.pk,
                    'title'                     : item.title,
                    'description'               : item.description,
                    'is_active'                 : item.is_active,
                    'is_payment_required'       : item.is_payment_required,
                    'is_approved'              : item.is_approved,
                    'price'                     : item.price
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/support/servicesupport.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

#create support service
def createSupportServiceMethod(request):
    if is_superuser(request) or is_staff(request):
        form = CreateSupportServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        else:
            print(form.errors)
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#update support service
def updateSupportServiceMethod(request):
    if is_superuser(request) or is_staff(request):
        service = customerSupportService.objects.get(id=int(request.POST['id']))
        form = UpdateSupportServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        else:
            print(form.errors)
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#approuved Support Service
def validateSupportServiceMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            service = customerSupportService.objects.get(id=request.POST['id'])
            if service.is_approved:
                service.is_approved = False
            else:
                service.is_approved = True
            service.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#status support service 
def statusSupportServiceMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            service = customerSupportService.objects.get(id=request.POST['id'])
            if service.is_active:
                service.is_active = False
            else:
                service.is_active = True
            service.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#delete support service
def deleteSupportServiceMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            service = customerSupportService.objects.get(id=request.POST['id'])
            service.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

################################################################################
############################# MANAGE TICKET MESSAGE ############################
################################################################################
#Fromat Message
def formatMessageTicket(message):
    data = {
        'messageid'             : message.pk,
        'customer_name'         : message.owner.user.get_full_name(),
        'customer_pp'           : message.owner.pp.url if message.owner.pp else '',
        'operator_name'         : message.operator.user.get_full_name() if message.operator is not None else '',
        'operator_pp'           : message.operator.pp.url if message.operator is not None else '',
        'message'               : message.message,
        'rep_message'           : message.rep_message,
        'is_customer_message'   : message.is_customer_message,
        'is_operator_message'   : message.is_operator_message,
        'created_date'          : message.created_date,
        'updated_date'          : message.updated_date,
        'is_active'             : message.is_active
    }
    return data

#Fetch Message
def messageTicketSupportHome(request):
    if is_superuser(request) or is_staff(request):
        ticket = customerSupportTicket.objects.get(id=int(request.POST['ticket']))
        all_message = []
        for mes in ticketMessage.objects.filter(ticket=ticket):
            all_message.append(formatMessageTicket(mes))
        
        status = ''
        if ticket.progression_status == 1:
            status = 'En attente de votre reponse.'
        else:
            status = 'En attente du Support'
        ticketInfo = {
            'id'            : ticket.pk,
            'ticketnumber'  : 'TCK{}'.format(ticket.pk),
            'resume'        : ticket.resume,
            'status'        : status,
            'service'       : ticket.service.title
        }
        return JsonResponse({'status':200, 'messages':all_message, 'ticketInfo':ticketInfo})
    return JsonResponse({'status':500, 'message':'Veuillez vous identifiez pour effectuer cette action!'})

#Send Message
def sendMessageTicketSupport(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateMessageTicketForm(request.POST)
            if form.is_valid():
                newmessage = form.save()
                if 'attach' in request.FILES:
                    newmessage.attach = request.FILES['attach']
                newmessage.is_operator_message = True
                newmessage.operator = Persons.objects.get(user=request.user)
                newmessage.save()
                message = formatMessageTicket(newmessage)
                return JsonResponse({'status':200, 'message':'Message envoyé avec succès!', 'message':message})
            else:
                print(form.errors)
        return JsonResponse({'status':500, 'message':'Formulaire invalide!'})
    return JsonResponse({'status':500, 'message':'Veuillez vous identifiez pour effectuer cette action!'})

#Delete Message
def deleteMessageTicketSupport(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            message = ticketMessage.objects.get(id=int(request.POST['id']))
            message.delete()
            return JsonResponse({'status':200, 'message':'Message supprimer avec succès!'})
        return JsonResponse({'status':500, 'message':'Formulaire invalide!'})
    return JsonResponse({'status':500, 'message':'Veuillez vous identifiez pour effectuer cette action!'})

################################################################################
################################## MANAGE COMMNAD  #############################
################################################################################
##############Command Home
def homeCommandMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            numberallcommand        = Commands.objects.filter(is_active=True).count()
            numberbuycommand        = Commands.objects.filter(customer_has_pay=True).count()
            numberrejectedcommand   = Commands.objects.filter(is_rejected=True).count()
            numberdeletecommand     = Commands.objects.filter(desactivate_visibility_for_customer=True).count()
            delivered = None
            allcommand = []
            for item in Commands.objects.order_by('-created_date'):
                all_product = []
                if CommandBasketProduct.objects.filter(command=item):
                    for baskitem in CommandBasketProduct.objects.filter(command=item):
                        all_product.append({
                            'name'      : baskitem.product.name,
                            'cover'     : baskitem.product.cover,
                            'seller'    : baskitem.product.seller.user.get_full_name()
                        })
                if item.product:
                    all_product.append({
                        'name'      : item.product.name,
                        'cover'     : item.product.cover,
                        'seller'    : item.product.seller.user.get_full_name()
                    })

                if DeliveredCommands.objects.filter(command=item):
                    delivered = DeliveredCommands.objects.get(command=item)

                allcommand.append({
                    'id'                    : item.pk,
                    'customer'              : item.customer.user.get_full_name(),
                    'products'              : all_product,
                    'command_is_pay'        : item.customer_has_pay,
                    'total'                 : item.total_price,
                    'delivery_start'        : delivered.delivery_start if delivered is not None else '',
                    'delivered_end'         : delivered.delivered_end if delivered is not None else '',
                    'created_date'          : item.created_date
                })
            currency = currencyToggle(request) 
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/command/command.html', locals())
        return render(request, 'dashboard/errors/401.html') 
    return redirect('core:auth-home')

#############update status command payment
def statusCommandPaymentMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                command = Commands.objects.get(id=request.POST['id'])
                if command.customer_has_pay:
                    payment = Payments.objects.filter(command=command).first()
                    payment.is_pay = False 
                    payment.save()

                    #financial line
                    financialline = Finances.objects.get(command=command)

                    #delete seller commission line
                    sellercommission = FinanceSellerCommissionOwners.objects.filter(finance=financialline)
                    sellercommission.delete()

                    #delete financial line
                    financialline.delete()

                    #update product state and basket
                    if command.basket:
                        #update ich item payment status
                        for item in CommandBasketProduct.objects.filter(command=payment.command, customer_has_pay=True):
                            item.customer_has_pay = False
                            item.save()

                        #update item in basket 
                        basket = Baskets.objects.get(id=payment.command.basket.pk)
                        for item in ProductBaskets.objects.filter(basket=basket, is_pay=True):
                            item.visibility_for_customer    = True
                            item.is_pay                     = False
                            item.save()

                            #update product quantity
                            newsproductinfo = Products.objects.get(id=item.product.pk)
                            newsproductinfo.quantity = newsproductinfo.quantity + item.quantity
                            newsproductinfo.save()

                            #update basket info
                            basket.number_item += 1
                            basket.total_price += payment.amount
                            basket.save()
                    command.customer_has_pay = False
                else:
                    payment = Payments.objects.filter(command=command).first()
                    payment.is_pay = True 
                    payment.save()

                    #if command is sponsoring update financial statement
                    if payment.command.sponsoring:
                        #update the finalcial statement
                        Finances.objects.create(
                            command                 = payment.command,
                            total_price             = payment.amount,
                            delivered_commission    = 0,
                            company_commission      = payment.command.total_price,
                        )
                    
                    # if comamnd is basket item update financial statement
                    if payment.command.basket:
                        #commission company
                        company                 = Company.objects.first()
                        company_fees            = Decimal(company.commission_sales) * Decimal(payment.command.basket.total_price) / 100 

                        #commission distributor
                        deliveredinfo               = DeliveredCommands.objects.get(command=payment.command)
                        distributor                 = deliveredinfo.distributor
                        distributor_fees            = Decimal(distributor.frais_poid)

                        #update the finalcial statement
                        finance = Finances.objects.create(
                            command                 = payment.command,
                            total_price             = payment.amount,
                            delivered_commission    = distributor_fees,
                            company_commission      = company_fees,
                        )

                    # if command is direct product payment update statement
                    if payment.command.product:
                        #commission company
                        company                 = Company.objects.first()
                        company_fees            = Decimal(company.commission_sales) * Decimal(payment.command.total_price) / 100 

                        #commission distributor
                        deliveredinfo               = DeliveredCommands.objects.get(command=payment.command)
                        distributor                 = deliveredinfo.distributor
                        distributor_fees            = Decimal(distributor.frais_poid)

                        #update the finalcial statement
                        finance = Finances.objects.create(
                            command                 = payment.command,
                            total_price             = payment.amount,
                            delivered_commission    = distributor_fees,
                            company_commission      = company_fees,
                        )

                    #SEND SMS ALERT TO CUSTOMER
                    if command.customer.phone:
                        request_data = {
                            "messages":[
                                {
                                    "destinations":[
                                        {"to":"237{}".format(command.customer.phone)}
                                    ],
                                    "from":"Frip Me",
                                    "text":"Nous confirmons votre commande FRIP-CMD{} et validons votre paiement. Notre service de livraison vous contactera au plus tard dans 72H.\
                                            Merci d’envoyer une confirmation après réception de votre article.".format(command.pk)
                                }
                            ]
                        }

                        headers = {
                            "creatorization": "App 3c5790690e68c8c6e14a67cc57d12aa3-6f81a34d-bb76-42f4-b9ad-b7fddc49de6a",
                            "Content-Type": "application/json",
                            "Accept"      : "application/json"
                        }
                        json_data = json.dumps(request_data)
                        response = requests.post('https://m3ddx2.api.infobip.com/sms/2/text/advanced', data=json_data, headers=headers)
                        result = response.json()

                    #SEND SMS ALERT TO SELLER
                    if command.basket:
                        for item in ProductBaskets.objects.filter(basket=command.basket ,visibility_for_customer=True, is_pay=False):
                            if item.product.seller.phone:
                                request_data = {
                                    "messages":[
                                        { 
                                            "destinations":[
                                                {"to":"237{}".format(item.product.seller.phone)}
                                            ],
                                            "from":"Frip Me",
                                            "text":"Votre article a été commandé. Notre service de livraison vous contactera dans les 24h pour enlèvement.\
                                                    Vous recevrez votre paiement dès réception de l’article par l’acheteur."
                                        }
                                    ]
                                }

                                headers = {
                                    "creatorization": "App 3c5790690e68c8c6e14a67cc57d12aa3-6f81a34d-bb76-42f4-b9ad-b7fddc49de6a",
                                    "Content-Type": "application/json",
                                    "Accept"      : "application/json"
                                }
                                json_data = json.dumps(request_data)
                                response = requests.post('https://m3ddx2.api.infobip.com/sms/2/text/advanced', data=json_data, headers=headers)
                                result = response.json()
                    else:
                        request_data = {
                            "messages":[
                                { 
                                    "destinations":[
                                        {"to":"237{}".format(command.product.seller.phone)}
                                    ],
                                    "from":"Frip Me",
                                    "text":"Votre article a été commandé. Notre service de livraison vous contactera dans les 24h pour enlèvement.\
                                            Vous recevrez votre paiement dès réception de l’article par l’acheteur."
                                }
                            ]
                        }

                        headers = {
                            "creatorization": "App 3c5790690e68c8c6e14a67cc57d12aa3-6f81a34d-bb76-42f4-b9ad-b7fddc49de6a",
                            "Content-Type": "application/json",
                            "Accept"      : "application/json"
                        }
                        json_data = json.dumps(request_data)
                        response = requests.post('https://m3ddx2.api.infobip.com/sms/2/text/advanced', data=json_data, headers=headers)
                        result = response.json()

                    #SEND SMS ALERT TO DELIVERED
                    if distributor.person.phone:
                        if command.basket:
                            for item in ProductBaskets.objects.filter(basket=command.basket ,visibility_for_customer=True, is_pay=False):
                                if item.product.seller.phone:
                                    request_data = {
                                        "messages":[
                                            {
                                                "destinations":[
                                                    {"to":"237{}".format(distributor.person.phone)}
                                                ],
                                                "from":"Frip Me",
                                                "text":"Bien vouloir effectuer un enlèvement au numéro {} , et la livraison de cet article au numéro {} \
                                                        Nous prévenir si vous êtes indisponible.".format(item.product.seller.phone, command.customer.phone)
                                            }
                                        ]
                                    }

                                    headers = {
                                        "creatorization": "App 3c5790690e68c8c6e14a67cc57d12aa3-6f81a34d-bb76-42f4-b9ad-b7fddc49de6a",
                                        "Content-Type": "application/json",
                                        "Accept"      : "application/json"
                                    }
                                    json_data = json.dumps(request_data)
                                    response = requests.post('https://m3ddx2.api.infobip.com/sms/2/text/advanced', data=json_data, headers=headers)
                                    result = response.json()
                        else:
                            if command.product.seller.phone:
                                request_data = {
                                    "messages":[
                                        {
                                            "destinations":[
                                                {"to":"237{}".format(distributor.person.phone)}
                                            ],
                                            "from":"Frip Me",
                                            "text":"Bien vouloir effectuer un enlèvement au numéro {} , et la livraison de cet article au numéro {} \
                                                    Nous prévenir si vous êtes indisponible.".format(command.product.seller.phone, command.customer.phone)
                                        }
                                    ]
                                }

                                headers = {
                                    "creatorization": "App 3c5790690e68c8c6e14a67cc57d12aa3-6f81a34d-bb76-42f4-b9ad-b7fddc49de6a",
                                    "Content-Type": "application/json",
                                    "Accept"      : "application/json"
                                }
                                json_data = json.dumps(request_data)
                                response = requests.post('https://m3ddx2.api.infobip.com/sms/2/text/advanced', data=json_data, headers=headers)
                                result = response.json()

                    if command.basket:
                        for item in ProductBaskets.objects.filter(basket=payment.command.basket, is_pay=False):
                            FinanceSellerCommissionOwners.objects.create(
                                finance             = finance,
                                seller              = item.product.seller,
                                amount              = item.one_price
                            )

                        #update ich item payment status
                        for item in CommandBasketProduct.objects.filter(command=payment.command, customer_has_pay=False):
                            item.customer_has_pay = True
                            item.save()

                        #update item in basket 
                        basket = Baskets.objects.get(id=payment.command.basket.pk)
                        for item in ProductBaskets.objects.filter(basket=basket, is_pay=False):
                            item.visibility_for_customer    = False
                            item.is_pay                     = True
                            item.save()

                            #update product quantity
                            newsproductinfo = Products.objects.get(id=item.product.pk)
                            newsproductinfo.quantity = newsproductinfo.quantity - item.quantity
                            newsproductinfo.save()

                            #update basket info
                            if basket.number_item > 0:
                                basket.number_item -= 1
                            if basket.total_price > 0:
                                basket.total_price -= payment.amount
                            basket.save()
                    else:
                        #update product quantity
                        newsproductinfo = Products.objects.get(id=command.product.pk)
                        if newsproductinfo.quantity > 0:
                            newsproductinfo.quantity = newsproductinfo.quantity - command.quantity
                            newsproductinfo.save()

                    command.customer_has_pay = True
                command.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifié.')})

##############changer command distributor point
def changeCommanddistributorPointMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                distributor = Distributors.objects.get(id=int(request.POST['distributor']))
                command = Commands.objects.get(id=int(request.POST['id']))
                
                #commission distributor
                deliveredinfo               = DeliveredCommands.objects.get(command=command)
                distributor                 = deliveredinfo.distributor
                distributor_fees            = Decimal(distributor.frais_poid)

                #update the finalcial statement
                financialline = Finances.objects.get(command=command)
                financialline.delivered_commission = distributor_fees
                financialline.save()

                #request additionnal payment if previous amount is less than the current one

                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifié.')})

##############delete command
def deleteCommandMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            if request.method == 'POST':
                command = Commands.objects.filter(id=int(request.POST['id']))
                command.delete()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
        return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})
    return JsonResponse({'status':500, 'message':str('Veuillez vous identifié.')})

################################################################################
################################## MANAGE SECURITY  #############################
################################################################################

#Manage Menu
def homeMenuMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allmenu = []
            for item in Menus.objects.all():
                allmenu.append({
                    'id'            : item.pk,
                    'title'         : item.title,
                    'code'          : item.code,
                    'link'          : item.link,
                    'is_active'     : item.is_active,
                })
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/security/menu.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateMenuForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            menu = Menus.objects.get(id=request.POST['id'])
            form = UpdateMenuForm(
                {
                    'title'     : request.POST['title'],
                    'code'      : request.POST['code'],
                    'link'      : request.POST['link'],
                }, 
            instance=menu)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            menu = Menus.objects.get(id=request.POST['id'])
            if menu.is_active:
                menu.is_active = False
            else:
                menu.is_active = True
            menu.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            menu = Menus.objects.get(id=request.POST['id'])
            menu.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Manage Parent Menu
def homeParentMenuMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allparentmenu = []
            for item in ParentMenus.objects.all():
                allmenu = []
                for m in item.menus.all():
                    allmenu.append({
                        'id'            : m.pk,
                        'title'         : m.title,
                        'code'          : m.code,
                        'link'          : m.link,
                        'is_active'     : m.is_active,
                    })
                allparentmenu.append({
                    'id'            : item.pk,
                    'title'         : item.title,
                    'label'         : item.label,
                    'icon'          : item.icon,
                    'allmenu'       : allmenu,
                    'is_active'     : item.is_active,
                })
            allmenu = Menus.objects.filter(is_active=True)
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/security/parentmenu.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createParentMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateParentMenuForm(request.POST)
            if form.is_valid():
                parent = form.save(commit=True)
                for item in request.POST.getlist('menus'):
                    parent.menus.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateParentMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            parent = ParentMenus.objects.get(id=request.POST['id'])
            form = UpdateParentMenuForm(request.POST, instance=parent)
            if form.is_valid():
                parent = form.save(commit=True)
                if request.POST.getlist('menus'):
                    parent.menus.clear()
                    for item in request.POST.getlist('menus'):
                        parent.menus.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusParentMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            parent = ParentMenus.objects.get(id=request.POST['id'])
            if parent.is_active:
                parent.is_active = False
            else:
                parent.is_active = True
            parent.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteParentMenuMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            parent = ParentMenus.objects.get(id=request.POST['id'])
            parent.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Manage Menu rule
def homeMenuRuleMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allmenurule = []
            for item in MenuRules.objects.all():
                allmenurule.append({
                    'id'            : item.pk,
                    'label'         : item.label,
                    'menu'          : item.menu.title,
                    'menuid'        : item.menu.pk,
                    'can_read'      : item.can_read,
                    'can_create'    : item.can_create,
                    'can_update'    : item.can_update,
                    'can_delete'    : item.can_delete,
                    'is_active'     : item.is_active,
                })
            allmenu = Menus.objects.filter(is_active=True)
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/security/menurule.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createMenuRuleMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateMenuRuleForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateMenuRuleMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            rule = MenuRules.objects.get(id=request.POST['id'])
            form = UpdateMenuRuleForm(request.POST, instance=rule)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusMenuRuleMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            menurule = MenuRules.objects.get(id=request.POST['id'])
            if menurule.is_active:
                menurule.is_active = False
            else:
                menurule.is_active = True
            menurule.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteMenuRuleMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            menurule = MenuRules.objects.get(id=request.POST['id'])
            menurule.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Manage Profil
def homeProfilMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            allprofil = []
            for item in Profil.objects.all():
                allpermission = []
                for per in item.permissions.all():
                    allpermission.append({
                        'id'            : per.pk,
                        'label'         : per.label,
                        'menu'          : per.menu,
                        'can_read'      : per.can_read,
                        'can_create'    : per.can_create,
                        'can_update'    : per.can_update,
                        'can_delete'    : per.can_delete,
                        'is_active'     : per.is_active,
                    })
                allprofil.append({
                    'id'            : item.pk,
                    'title'         : item.title,
                    'description'   : item.description,
                    'is_active'     : item.is_active,
                    'permissions'   : allpermission
                })
            allmenurule = MenuRules.objects.filter(is_active=True)
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/security/profil.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateProfilForm(request.POST)
            if form.is_valid():
                profil = form.save(commit=True)
                for item in request.POST.getlist('permissions'):
                    profil.permissions.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            profil = Profil.objects.get(id=request.POST['id'])
            form = UpdateProfilForm(request.POST, instance=profil)
            if form.is_valid():
                profil = form.save(commit=True)
                if request.POST.getlist('permissions'):
                    profil.permissions.clear()
                    for item in request.POST.getlist('permissions'):
                        profil.permissions.add(item)
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            profil = Profil.objects.get(id=request.POST['id'])
            if profil.is_active:
                profil.is_active = False
            else:
                profil.is_active = True
            profil.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            profil = Profil.objects.get(id=request.POST['id'])
            profil.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

#Manage User Profil
def homeUserProfilMethod(request):
    if is_auth(request):
        if is_superuser(request) or is_staff(request):
            alluserprofil = []
            for item in UserProfil.objects.all():
                alluserprofil.append({
                    'id'            : item.pk,
                    'person'        : item.person.user.get_full_name(),
                    'personid'      : item.person.pk,
                    'profil'        : item.profil.title,
                    'profilid'      : item.profil.pk,
                    'description'   : item.description,
                    'is_active'     : item.is_active,
                })
            print(alluserprofil)
            allperson = Persons.objects.filter(is_active=True)
            allprofil = Profil.objects.filter(is_active=True)
            try:
                current_person  = Persons.objects.get(user=request.user)
                permissions     = userPermission(current_person)
            except Exception as error:
                pass
            return render(request, 'dashboard/security/userprofil.html', locals())
        return render(request, 'dashboard/errors/401.html', locals())
    return redirect('core:auth-home')

def createUserProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            form = CreateUserProfilForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            else:
                print(form.errors)
                return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})
    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def updateUserProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            userprofil = UserProfil.objects.get(id=request.POST['id'])
            form = UpdateUserProfilForm(request.POST, instance=userprofil)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':200, 'message':str('Opération réussie!')})
            return JsonResponse({'status':500, 'message':str('Une erreur cest produite!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def statusUserProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            userprofil = UserProfil.objects.get(id=request.POST['id'])
            if userprofil.is_active:
                userprofil.is_active = False
            else:
                userprofil.is_active = True
            userprofil.save()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})

def deleteUserProfilMethod(request):
    if is_superuser(request) or is_staff(request):
        if request.method == 'POST':
            userprofil = UserProfil.objects.get(id=request.POST['id'])
            userprofil.delete()
            return JsonResponse({'status':200, 'message':str('Opération réussie!')})
        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite dans le formulaire')})

    return JsonResponse({'status':500, 'message':str('Vous n\'avez pas le niveau de sécurité exiger.')})














