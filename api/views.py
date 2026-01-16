from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User
from jose import jwt
import json
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from rest_framework.generics import ListAPIView
from django.contrib.auth import logout
from allauth.account.models import EmailAddress
from datetime import datetime as datetime1
import datetime as datetime2
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
import logging
from django.core import serializers as core_serialisers
from braces.views import CsrfExemptMixin
from django.db.models import F
from rest_framework.views import APIView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from core.models import *
from django.db import IntegrityError
from dashboard.models import *
from core.models import AccountActivationCode
from django_filters.rest_framework import DjangoFilterBackend
from cities_light.models import City, Country, Region
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid
import requests
from dashboard.models import *
from dashboard.forms import *

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import random
from django.utils.http import urlsafe_base64_encode
import time
from django.utils.crypto import get_random_string

def loadUsr(token):
    user_data = jwt.decode(token, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
    usr = User.objects.get(username=user_data["user"])
    return usr

################################################################
######################### FORMAT DATA ##########################
################################################################
#Format company 
def company_info():
    company = Company.objects.first()
    all_presentation    = []
    all_phone           = []
    all_email           = []
    all_social          = []
    all_address         = []
    all_values          = []
    all_deliveredzone   = []
    all_partner         = []
    try:
        for item in company.presentations.all():
            all_presentation.append({
                'label'         : item.label,
                'description'   : item.description,
                'video'         : item.video.url
            })

        for item in company.phones.all():
            all_phone.append({
                'phone' : item.phone
            })
        for item in company.emails.all():
            all_email.append({
                'email' : item.email
            })
        for item in company.socials.all():
            all_social.append({
                'name'      : item.name,
                'faicon'    : item.faicon,
                'link'      : item.link 
            })
        for item in company.addresses.all():
            all_address.append({
                'continent'         : item.continent,
                'country'           : item.country,
                'city'              : item.city,
                'address'           : item.address
            })
        for item in company.values.all():
            all_values.append({
                'label'             : item.label,
                'value'             : item.value
            })
        for item in CompanyDeliveryZone.objects.filter(is_approved=True):
            all_deliveredzone.append({
                'title'                 : item.title,
                'description'           : item.description,
                'googlemap'             : item.googlemap,
                'price'                 : item.price
            })
        for item in company.partners.all():
            all_partner.append({
                'name'             : item.name,
                'description'      : item.description,
                'link'             : item.link,
                'logo'             : item.logo.url
            })
    except Exception as error:
        pass
        print (error)
        
    data = {
        'name'                      : company.name,
        'vision'                    : company.vision,
        'mission'                   : company.mission,
        'description'               : company.description,
        'presentations'             : all_presentation,
        'mission'                   : company.mission,   
        'logo'                      : company.logo.url,
        'phones'                    : all_phone,
        'emails'                    : all_email,
        'socials'                   : all_social,
        'values'                    : all_values,
        'partners'                  : all_partner,
        'addresses'                 : all_address,
        'slug'                      : company.slug, 
    }
    return data

#Format country 
def one_country(country):
    all_city           = []
    for item in City.objects.filter(country=country):
        all_city.append({
            'id'        : item.pk,
            'name'      : item.name,
        })
        
    data = {
        'id'            : country.pk,
        'name'          : country.name,
        'cities'        : all_city
    }
    return data

#Person format
def one_person(person):
    data = { 
        'id_person'                     : person.id, 
        'first_name'                    : person.user.first_name,
        'last_name'                     : person.user.last_name,
        'name'                          : person.user.get_full_name(),
        'country'                       : person.country.name if person.country else '',
        'countryid'                     : person.country.id if person.country else '',
        'city'                          : person.city.name if person.city else '',
        'cityid'                        : person.city.id if person.city else '',
        'phone'                         : person.phone,
        'email'                         : person.user.email,
        'currency'                      : person.currency,
        'address'                       : person.address,
        'codepostal'                    : person.codepostal,
        'birthday_date'                 : str(person.birthday_date),
        'pp'                            : person.pp.url if person.pp  else '',
        'is_active'                     : person.is_active,
        'is_verified'                   : person.is_verified,
        'is_staff'                      : person.is_staff,
        'is_customer'                   : person.is_customer,
        'googleauthenticator'           : person.googleauthenticator,
        'twofactor'                     : person.twofactor,
        'googlemapservice'              : person.googlemapservice,
        'pushconfirmnotification'       : person.pushconfirmnotification,
        'smsconfirmnotification'        : person.smsconfirmnotification,
        'emailconfirmnotification'      : person.emailconfirmnotification,
        'pushremindnotification'        : person.pushremindnotification,
        'smsremindnotification'         : person.smsremindnotification,
        'emailremindnotification'       : person.emailremindnotification,
        'pushpricealertnotification'    : person.pushpricealertnotification,
        'smspricealertnotification'     : person.smspricealertnotification,
        'emailpricealertnotification'   : person.emailpricealertnotification,
        'pushdiscountnotification'      : person.pushdiscountnotification,
        'smsdiscountnotification'       : person.smsdiscountnotification,
        'emaildiscountnotification'     : person.emaildiscountnotification,
        'created_date'                  : person.created_date,
    } 
    return data

#Banner format
def one_banner(banner):
    data = {
        'id'            : banner.pk,
        'title'         : banner.title,
        'cover'         : banner.cover.url,
        'link'          : banner.link,
        'is_external'   : banner.is_external,
        'is_approved'   : banner.is_approved
    }
    return data

#Format category
def one_category(category):
    data = {
        'id'    : category.pk,
        'name'  : category.name,
        'cover' : category.cover.url
    }
    return data

#Format brand
def one_brand(brand):
    data = {
        'id'   : brand.pk,
        'name' : brand.name,
        'logo' : brand.logo.url
    }
    return data

def on_product(product):
    provider = {
        'name'    : product.provider.name,
        'logo'    : product.provider.logo.url
    }
    
    #get all images 
    all_image = []
    for item in product.images.all():
        all_image.append({
            'id'    : item.pk,
            'label' : item.label,
            'image' : item.image.url
        })
        
    #get all videos 
    all_video = []
    for item in product.videos.all():
        all_video.append({
            'id'    : item.pk,
            'label' : item.label,
            'video' : item.video.url
        })
        
    ATTRIBUTS = dict()
    if ProductCaracteristque.objects.filter(product=product):
        attribut = ProductCaracteristque.objects.get(product=product)
        all_size = []
        for item in attribut.size.all():
            all_size.append({
                'id'    : item.pk,
                'name'  : item.name
            })
        ATTRIBUTS['sizes'] = all_size
        
        all_color = []
        for item in attribut.color.all():
            all_color.append({
                'id'    : item.pk,
                'name'  : item.name,
                'code'  : item.code
            })
        ATTRIBUTS['colors'] = all_color
            
        all_material = []
        for item in attribut.material.all():
            all_material.append({
                'id'            : item.pk,
                'name'          : item.name,
                'description'   : item.description
            })
        ATTRIBUTS['materials'] = all_material
        
    all_comment = []
    rate_average = 0
    iter_rate = 0
    sum_rate = 0
    for item in CommentProducts.objects.filter(product=product):
        all_comment.append(one_comment_product(item))
        for itemrate in RatingProducts.objects.filter(product=item.product):
            iter_rate += 1
            sum_rate += itemrate.rate
    
    if iter_rate > 0:
        rate_average = round((sum_rate / 5) / iter_rate)
    
    data = {
        'id'                    : product.pk,
        'provider'              : provider,
        'name'                  : product.name,
        'description'           : product.description,
        'presentation'          : product.presentation,
        'price'                 : Decimal(product.price),
        'discount'              : Decimal(product.discount),
        'quantity'              : product.quantity,
        'brand'                 : one_brand(product.brand),
        'category'              : product.category.pk,
        'categoryname'          : product.category.name,
        'slug'                  : product.slug,
        'images'                : all_image,
        'videos'                : all_video,
        'weigth'                : product.weigth,
        'height'                : product.height,
        'width'                 : product.width,
        'depth'                 : product.depth,
        'commission_provider'   : Decimal(product.commission_provider),
        'commission_company'    : Decimal(product.commission_company),
        'is_approved'           : product.is_approved,
        'attributes'            : ATTRIBUTS,
        'comments'              : all_comment,
        'count_rate'            : iter_rate,
        'rate_average'          : rate_average
    }
    return data

#Format comment product
def one_comment_product(comment):
    data = {
        'customer'      : one_person(comment.customer),
        'comment'       : comment.comment,
        'reply_comment' : comment.reply_comment,
        'created_date'    : comment.created_date
    }
    return data

#Format basket
def one_basket(basket):
    products = []
    for item in ProductBaskets.objects.filter(basket=basket):
        products.append({
            'id'            : item.pk,
            'product'       : on_product(item.product),
            'quantity'      : item.quantity,
            'one_price'     : item.one_price,
            'is_pay'        : item.is_pay
        })
        
    data = {
        'id'                    : basket.pk,
        'products'              : products,
        'number_item'           : basket.number_item,
        'total_price'           : Decimal(basket.total_price),
        'vat_price'             : Decimal(basket.vat_price),
        'is_checkout'           : basket.is_checkout
    }
    return data

#format provider
def one_provider(provider):
    data = {
        'name'              : provider.name,
        'logo'              : provider.logo.url,
        'is_approved'       : provider.is_approved
    }
    return data

#format booking sponsoring
def one_booking(booking):
    data = {
        'code_zone'         : booking.code_zone,
        'name'              : booking.name,
        'periode'           : booking.periode,
        'sponsoring_price'  : booking.sponsoring_price
    }
    return data

#Format sponsoring
def one_sponsoring(sponsor):
    data = {
        'provider'      : one_provider(sponsor.provider),
        'product'       : on_product(sponsor.product),
        'booking'       : one_booking(sponsor.booking),
        'banner'        : one_banner(sponsor.banner) if sponsor.banner is not None else None,
        'start_date'    : sponsor.start_date,
        'end_date'      : sponsor.end_date,
        'is_approved'   : sponsor.is_approved
    }
    return data

#Format command
def one_command(command):
    data = {
        'basket'                            : one_basket(command.basket),
        'product'                           : on_product(command.product) if command.product is not None else None,
        'sponsoring'                        : one_sponsoring(command.sponsoring) if command.sponsoring is not None else None,
        'item_number'                       : command.item_number,
        'details'                           : command.details,
        'total_price'                       : Decimal(command.total_price),
        'vat_price'                         : Decimal(command.vat_price),
        'is_shop_pickup'                    : command.is_shop_pickup,
        'is_delivery'                       : command.is_delivery,
        'delivery'                          : command.delivery.pk,
        'is_delivery_start'                 : command.is_delivery_start,
        'delivery_start_datetime'           : command.delivery_start_datetime,
        'is_delivery_end'                   : command.is_delivery_end,
        'delivery_end_datetime'             : command.delivery_end_datetime,
        'quantity'                          : command.quantity,
        'is_pay'                            : command.is_pay,
        'is_hide'                           : command.is_hide,
        'is_approved'                       : command.is_approved,
        'is_rejected'                       : command.is_rejected
    }
    return data

#Format service support
def one_service_support(service):
    data = {
        'title'                 : service.title,
        'description'           : service.description,
        'is_payment_required'   : service.is_payment_required,
        'price'                 : Decimal(service.price),
        'is_approved'           : service.is_approved
    }
    return data

#Format one ticket messages
def one_ticket_message(message):
    data = {
        'owner'                 : one_person(message.owner),
        'operator'              : one_person(message.operator) if message.operator is not None else None,
        'message'               : message.message,
        'attach'                : message.attach.url if message.attach else '',
        'rep_message'           : message.rep_message,
        'is_customer_message'   : message.is_customer_message,
        'is_operator_message'   : message.is_operator_message
    }
    return data

#Format ticket
def one_ticket(ticket):
    all_message = []
    for item in ticketMessage.objects.filter(ticket=ticket):
        all_message.append(one_ticket_message(item))
        
    data = {
        'id'                : ticket.pk,
        'owner'             : one_person(ticket.owner),
        'service'           : one_service_support(ticket.service),
        'command'           : one_command(ticket.command),
        'resume'            : ticket.resume,
        'description'       : ticket.description,
        'progression_status': ticket.progression_status,
        'is_resolv'         : ticket.is_resolv,
        'messages'          : all_message,
    }
    return data

########################### END FORMAT #########################

class SiteInfoApiView(CsrfExemptMixin, generic.View):
    def get(self, request, *args, **wargs):
        SITE_INFO = dict()
        allbanner = []
        for item in BannerPubs.objects.filter(is_approved=True, is_active=True).order_by('-created_date'):
            allbanner.append(one_banner(item))
        SITE_INFO['banners'] = allbanner

        categories = []
        for item in parentCategory.objects.filter(is_active=True).order_by('-created_date'):
            categories.append(one_category(item))
        SITE_INFO['categories'] = categories

        allbrand = []
        for item in Brands.objects.filter(is_active=True).order_by('-created_date'):
            allbrand.append(one_brand(item))
        SITE_INFO['brands'] = allbrand
        
        allcountry = []
        for item in Country.objects.all():
            allcountry.append(one_country(item))
        SITE_INFO['countries'] = allcountry

        SITE_INFO['company'] = company_info()
        return JsonResponse({"status":200, "message":"Opération réussie!" ,'result':SITE_INFO})   

class LoginApiView(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf8"))
        user = authenticate(username=body["username"], password=body["password"])
        log_message_api_auth = ''
        exexute_date = datetime1.now()
        if user:
            user_is_activate = EmailAddress.objects.filter(user=user, verified=True)
            if user_is_activate:
                RESULT = dict()
                PERSON = Persons.objects.get(user=user)
                RESULT['user'] = one_person(PERSON)
                
                #generate token
                expiry = datetime2.date.today() + datetime2.timedelta(days=999)
                expiry = str(expiry.day) + "/" + str(expiry.month) + "/" + str(expiry.year)
                token = jwt.encode({'user': user.username, 'expiry': expiry}, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithm='HS256')
                RESULT['token'] = token
                
                #login instance
                login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')
                
                return JsonResponse({"status":200, "result": RESULT})
            else:
                log_message_api_auth = str('Erreur d\'authentification le Compte {} est inactif {}').format(
                    user,
                    exexute_date) 
                log = open('fstore_log.txt', 'a' , encoding='utf-8')
                log.write(log_message_api_auth)
                log.write('\n')
                log.close()
                return JsonResponse({"status": 500, "message":"Votre compte est inactif."})
        else:
            log_message_api_auth = str('Erreur d\'  c. {} à essayer de ce connecter avec des identifiants incorrects {}').format(
                    body["username"],
                    exexute_date)
            log = open('fstore_log.txt', 'a' , encoding='utf-8')
            log.write(log_message_api_auth)
            log.write('\n')
            log.close()
            return JsonResponse({"status":500, "message": 'Utilisateur ou mot de passe incorrects'})
        
class SinupApiView(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf8"))
        PERSON = None
        if User.objects.filter(email=body["email"]):
            return JsonResponse({"status":500, "message": "Email déjà utilisé par un autre utilisateur."})
        else:
            pass

        if User.objects.filter(username=body["username"]):
            return JsonResponse({'status':500, 'message':str('Désoler ce nom d\'utilisateur est déjà utiliser essayez un autre.')})
        else:
            pass

        if body['password1'] == body['password2']:
            pass
        else:
            return JsonResponse({'status':500, 'message':str('Les mots de passe sont différents')})

        #create new user
        USER = User.objects.create(username=body["email"], password=body["password1"])
        USER.first_name = body["first_name"]
        USER.last_name = body["last_name"]
        USER.username = body["username"]
        USER.email = body["email"] 
        USER.save()
        
        #create email address
        EmailAddress.objects.create(email=USER.email,user=USER)
        
        #create person
        PERSON = Persons.objects.create(
            phone=body['phone'],
            user=USER
        )
        
        PERSON.is_customer = True

        if body['referral'] != '':
            PERSON.referral = User.objects.get(username=body['referral'])
        PERSON.save()
        
        fixed_digits = 6
        activation_code = random.randrange(111111, 999999, fixed_digits)
        activation_code_generate = AccountActivationCode.objects.create(
            person = PERSON,
            code = activation_code
        )

        try:  
            #Send Activation Code By EMAIL
            context = {
                "receiver_name"     : USER.get_full_name(),
                "code"              : activation_code_generate.code,
                "date"              : datetime.now().strftime("%d-%m-%Y %H:%M")
            }

            receiver_email = USER.email
            template_name = "core/mail/account_activation_email.html"
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
        return JsonResponse({'status':200, 'message': str('Compte crée avec succès! Veuillez saisir le code reçu par mail pour l\'activer.')})
        
class ActivateAccount(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf8"))
        print(body, 'ddd')
        activate_code = None
        PERSON  = None
        USER    = None
        RESULT  = dict()
        current_user = User.objects.get(email=body['email'])
        current_person = Persons.objects.get(user=current_user)
        
        try:
            activate_code = AccountActivationCode.objects.get(person=current_person, code=body['code'])
        except Exception as error:
            print(error)
            
        if activate_code:
            user = activate_code.person.user
            user.is_active = True
            user.save()

            EMAIL = EmailAddress.objects.get(user_id=user.pk)
            EMAIL.verified = True
            EMAIL.primary = True
            EMAIL.save()

            PERSON = Persons.objects.get(user=user)
            PERSON.is_online=True
            PERSON.save()

            RESULT['user'] = one_person(PERSON)

            expiry = datetime2.date.today() + datetime2.timedelta(days=999)
            expiry = str(expiry.day) + "/" + str(expiry.month) + "/" + str(expiry.year)
            token = jwt.encode({'user': user.username, 'expiry': expiry}, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithm='HS256')
            activate_code.delete()
            
            RESULT['token'] = token
            
            return JsonResponse({"status":200, "result": RESULT})
        else:
            return JsonResponse({"status":500, "message":"Le code que vous avez saisi est incorrect"})

class updatePassword(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        usr = loadUsr(data["token"])
        if usr:
            usr.set_password(data["password"])
            usr.save()
            return JsonResponse({"status":200, "message":"Mot de passe modifier avec succès."})
        return JsonResponse({"status":403, "message":"Veuillez vous authentifier"})
            
class LogOut(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        usr = loadUsr(data["token"])
        if usr:
            current_person = Persons.objects.get(user=usr)
            current_person.is_online = False
            current_person.save()
            logout(request)
            return JsonResponse({"status": 200, "message":"Déconnexion réussie!"})
        return JsonResponse({"status":403, "message":"Veuillez vous authentifier"})
        

####################### MANAGE USER DATA
class UserDataApiView(CsrfExemptMixin, generic.View):
    def get(self, request, *args, **wargs):
        token = self.request.GET.get('token')
        user_data = jwt.decode(token, 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            RESULT = dict()
            PERSON = Persons.objects.get(user=USER)
            
            try:
                active_basket = Baskets.objects.get(customer=PERSON, is_checkout=False)
                RESULT['basket'] = one_basket(active_basket)
            except Exception as e:
                RESULT['basket'] = []

            all_command = []
            for item in Commands.objects.filter(customer=PERSON):
                all_command.append(one_command(item))
            RESULT['commands'] = all_command
            
            all_favorit = []
            for item in FavoriteProducts.objects.filter(customer=PERSON):
                all_favorit.append(on_product(item.product))
            RESULT['favorits'] = all_favorit
            
            all_affiliate = []
            for item in Persons.objects.filter(referral=PERSON.user, is_verified=True):
                all_affiliate.append(one_person(item))
            RESULT['affiliates'] = all_affiliate

            all_ticket = []
            for item in customerSupportTicket.objects.filter(owner=PERSON, is_active=True)[:30]:
                all_ticket.append(one_ticket(item))
            RESULT['tickets'] = all_ticket

            return JsonResponse({"status":200, "message":"Opération réussie!" ,'result':RESULT})   
        return JsonResponse({"status": 403, "message" : "Vous n'êtes pas autorisé à effectuer cette action"})

# ######################MANAGE PRODUCT
class allProduct(CsrfExemptMixin, generic.View):
    def get(self, request, *args, **wargs):
        token = request.GET.get('token')
        usr = loadUsr(token)
        if usr:
            allproduct = []
            for item in Products.objects.filter(is_approved=True):
                allproduct.append(on_product(item))
                
            initial_per_page = 20
            
            paginator = Paginator(allproduct, initial_per_page)
            
            page = request.GET.get('page')
            try:
                paginate_data = paginator.page(page)
            except PageNotAnInteger:
                paginate_data = paginator.page(1)
            except EmptyPage:
                paginate_data = paginator.page(Paginator.num_pages)
            is_paginated = False
            if len(allproduct) > int(str(initial_per_page)):
                is_paginated = True 
            paginate_data = paginate_data
            is_paginated = is_paginated
            
            return JsonResponse({'status':200, 
                                    'result'                : paginate_data.object_list, 
                                    'is_paginated'          : is_paginated,
                                    'page'                  : paginate_data.number,
                                    'total_pages'           : paginator.num_pages,
                                    'total_items'           : paginator.count,
                                    'has_next'              : paginate_data.has_next(),
                                    'has_previous'          : paginate_data.has_previous(),
                                })
        else:
            return JsonResponse({"erreur": "Une erreur cest produite veuillez contacter l'administrateur"})
        
class searchProduct(CsrfExemptMixin, generic.View):
    def get(self, request, *args, **wargs):
        token = request.GET.get('token')
        q = request.GET.get('key')
        usr = loadUsr(token)
        if usr:
            liste = Products.objects.filter(is_approved=True)
            try:
                if Products.objects.filter(is_approved=True, name__icontains=q) and len(q) > 1:
                    liste = liste | Products.objects.order_by('-id').filter(is_approved=True, name__icontains=q)
                if Products.objects.filter(is_approved=True, description__icontains=q) and len(q) > 1:
                    liste = liste | Products.objects.order_by('-id').filter(is_approved=True, description__icontains=q)
                if Products.objects.filter(is_approved=True, category__name__icontains=q) and len(q) > 1:
                    liste = liste | Products.objects.order_by('-id').filter(is_approved=True, category__name__icontains=q)
                allproduct = []
                for item in liste:
                    allproduct.append(on_product(item))
                return JsonResponse({'status':200, 'result':allproduct})
            except Exception as error:
                print(error, 'error')
                return JsonResponse({'status':400, 'message':'Aucun resultats pour cette recherche'})
        else:
            return JsonResponse({'status':500, 'message':'Utilisateur non authentifier'})

# ######################MANAGE PRODUCTS CATEGORY
class productsCategory(CsrfExemptMixin, generic.View):
    def get(self, request, *args, **wargs):
        token = request.GET.get('token')
        category = request.GET.get('category')
        usr = loadUsr(token)
        if usr:
            allproduct = []
            currentcat = None
            if categoriesGrantChild.objects.filter(id=int(category)):
                category = categoriesGrantChild.objects.get(id=int(category))
                for item in Products.objects.filter(is_approved=True, category=category):
                    allproduct.append(on_product(item))
                currentcat = category
                    
            elif parentCategory.objects.filter(id=int(category)):
                category = parentCategory.objects.get(id=int(category))
                for child in category.childs.all():
                    grantcs = child.grantchilds.all()
                    for item in Products.objects.filter(is_approved=True, category_in=[grantcs]):
                        allproduct.append(on_product(item))
                currentcat = category
                
            initial_per_page = 20
            
            paginator = Paginator(allproduct, initial_per_page)
            
            page = request.GET.get('page')
            try:
                paginate_data = paginator.page(page)
            except PageNotAnInteger:
                paginate_data = paginator.page(1)
            except EmptyPage:
                paginate_data = paginator.page(Paginator.num_pages)
            is_paginated = False
            if len(allproduct) > int(str(initial_per_page)):
                is_paginated = True 
            paginate_data = paginate_data
            is_paginated = is_paginated
            
            RESULT = {
                'products'              : paginate_data.object_list, 
                'is_paginated'          : is_paginated,
                'page'                  : paginate_data.number,
                'total_pages'           : paginator.num_pages,
                'total_items'           : paginator.count,
                'has_next'              : paginate_data.has_next(),
                'has_previous'          : paginate_data.has_previous(),
            }
            return JsonResponse({'status':200, 'result' : RESULT})
        else:
            return JsonResponse({"erreur": "Une erreur cest produite veuillez contacter l'administrateur"})

#Comment product
class commentProduct(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            PERSON = Persons.objects.get(user=USER)
            PRODUCT = Products.objects.get(pk=data["product"])
            comment = CommentProducts.objects.create(
                customer    = PERSON,
                product     = PRODUCT,
                comment     = data["comment"]
            )
            
            #create rating
            RatingProducts.objects.create(
                customer    = PERSON,
                product     = PRODUCT,
                rate        = data["rate"]
            )
            
            newcomment = one_comment_product(comment)
            return JsonResponse({'status':200, 'result':newcomment, 'message':str('Opération réussie!')})
        else:
            return JsonResponse({"error":"Une erreur c'est produite dans le formulaire"})

##################################################################
##########################Manage BASKET###########################
##################################################################
class toggleBasket(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            PERSON = Persons.objects.get(user=USER)
            product = Products.objects.get(pk=data["product"])
            
            RESULT                  = dict()
            basket                  = None
            
            color                   = None
            material                = None
            size                    = None
            
            quantity                = data['quantity']
            price                   = product.price
            
            status                  = 200
            message                 = ''
            
            try:
                color = DefaultsColors.objects.get(id=data['color']) if data['color'] else None
                material = DefaultsMaterial.objects.get(id=data['material']) if data['material'] else None
                size = DefaultSize.objects.get(id=data['size']) if data['size'] else None
            except Exception as e:
                print(e)

            if Baskets.objects.filter(customer=PERSON, is_checkout=False):
                basket = Baskets.objects.get(customer=PERSON, is_checkout=False)
                if ProductBaskets.objects.filter(basket=basket, product=product):
                    
                    #remove the current item from backet
                    current_basket_product = ProductBaskets.objects.get(basket=basket, product=product)
                    
                    #update number of item
                    if basket.total_price > 0:
                        basket.total_price = Decimal(basket.total_price) - (Decimal(current_basket_product.one_price) * current_basket_product.quantity)
                    if basket.number_item > 0:
                        basket.number_item = basket.number_item - 1
                        
                    basket.save()

                    #Delete the item
                    current_basket_product.delete()
                    
                    status  = 200
                    message = str('Article retiré du panier avec succès!')
                else:
                    #create the new item in the basket
                    ProductBaskets.objects.create(
                        basket              = basket,
                        product             = product,
                        quantity            = quantity,
                        one_price           = price,
                        color               = color,
                        size                = size,
                        material            = material
                    )

                    #update Basket Info
                    basket.total_price = Decimal(basket.total_price) + (Decimal(price) * Decimal(quantity))
                    basket.number_item = basket.number_item + 1
                    basket.save()

                    status  = 200
                    message = str('Article ajouté au panier avec succès!')
            else:
                #Create the new basket
                basket = Baskets.objects.create(
                    customer            = PERSON,
                    number_item         = 0,
                    total_price         = 0,
                )
                
                ProductBaskets.objects.create(
                    basket              = basket,
                    product             = product,
                    quantity            = quantity,
                    one_price           = price,
                    color               = color,
                    size                = size,
                    material            = material
                )
                    
                #update Basket Info
                if basket.total_price > 0:
                    basket.total_price = Decimal(basket.total_price) + (Decimal(price) * quantity)
                basket.number_item = basket.number_item + 1
                basket.save()
                
                status  = 200
                message = str('Article ajouté au panier avec succès!')

            DATA = one_basket(basket)
            return JsonResponse({'status':200, 'message':message, 'result':DATA})
        else:
            return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})

#Change quantity item basket
class toggleQteProdBasket(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            basket = Baskets.objects.get(pk=data["basket"])
            productbasket = ProductBaskets.objects.get(id=int(data['prodbasket']))
            productbasket.quantity = data['quantity']
            productbasket.save()
            
            #update basket quantity
            total_price = 0
            for item in ProductBaskets.objects.filter(basket=basket):
                total_price = Decimal(total_price) + (Decimal(item.one_price) * Decimal(item.quantity))
            basket.total_price = total_price
            basket.save()

            DATA = one_basket(basket)
            return JsonResponse({'status':200, 'message':'La quantité a été mise à jour.', 'result':DATA})
        else:
            return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})
        
#Remove item basket
class removeProdBasket(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            basket = Baskets.objects.get(pk=data["basket"])
            
            #update basket quantity
            productbasket = ProductBaskets.objects.get(id=int(data['prodbasket']))

            #update basket
            total_price = Decimal(basket.total_price) - (Decimal(productbasket.one_price) * Decimal(productbasket.quantity))
            basket.total_price = total_price
            basket.number_item = basket.number_item - 1
            basket.save()
            
            productbasket.delete()

            DATA = one_basket(basket)
            return JsonResponse({'status':200, 'message':'Article retirer avec succès.', 'result':DATA})
        else:
            return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})

# Clean Basket
class wipeBasket(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            PERSON = Persons.objects.get(user=USER)
            
            basket = Baskets.objects.get(id=data['basket'], customer=PERSON)
            
            if ProductBaskets.objects.filter(basket=basket):
                #Delete ich item
                for item in ProductBaskets.objects.filter(basket=basket):
                    item.delete()
                
            #update number of item
            basket.total_price = 0
            basket.number_item = 0
            basket.save()

            DATA = one_basket(basket)
            return JsonResponse({'status':200, 'message':'Panier vider avec succès!', 'result':DATA})
        else:
            return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})

#Create command
class createCommand(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            PERSON          = Persons.objects.get(user=USER)
            is_shop_pickup  = data['is_shop_pickup']
            description     = data['description']
            quantity        = data['quantity']
            color           = None
            size            = None
            material        = None
            basket          = None
            product         = None
            shop_pickup     = False
            delivery        = None
            
            if is_shop_pickup == 'true':
                shop_pickup = True
            
            if data['product']:
                product     = Products.objects.get(id=int(data['product']))
                color       = DefaultsColors.objects.get(id=data['color'])
                size        = DefaultSize.objects.get(id=data['size'])
                material    = DefaultsMaterial.objects.get(id=data['material'])
                
            if data['basket']:
                basket = Baskets.objects.get(id=int(data['basket']))
                
            if not shop_pickup:
                delivery = CompanyDeliveryZone.objects.get(id=int(data['deliveredzone']))
            
            command = Commands.objects.create(
                customer                            = PERSON,
                basket                              = basket,
                product                             = product,
                item_number                         = basket.number_item if basket is not None else 1,
                details                             = description,
                total_price                         = basket.total_price if basket is not None else product.price,
                is_shop_pickup                      = shop_pickup,
                is_delivery                         = False if shop_pickup else True,
                delivery                            = delivery,
                quantity                            = quantity if product is not None else None,
                color                               = color,
                size                                = size,
                material                            = material
            )

            if basket is not None:
                basket.is_checkout = True
            basket.save()
            
            RESULT = one_command(command)
            return JsonResponse({'status':200, 'message':'Commande envoyée avec succès. Vous recevrez un message pour la confirmation de la validation.', 'result' : RESULT})
        else:
            return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})

#delete command
class deleteCommand(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            PERSON = Persons.objects.get(user=USER)
            command = Commands.objects.get(id=user_data['command'], customer=PERSON)
            if command.is_pay:
                command.is_hide = True
                command.save()
            else:
                command.delete()
            return JsonResponse({'status':200, 'message':'Commande supprimée avec succès!'})
        else:
            return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})        


##################################################################
########################## MANAGE PAIEMENT #######################
##################################################################
#Auth Api Payment
class requestAuthPayment(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            PERSON = Persons.objects.get(user=USER)
            
            #Process Auth
            authformdata = {
                'username'    : AFPAY_API_ACCOUNT_USERNAME,
                'password'    : AFPAY_API_ACCOUNT_PASSWORD
            }
            response_auth = requests.post("https://poly-h.net/api-auth/auth", data=authformdata)
            if response_auth.status_code == 200:
                auth_data = response_auth.json()
                if auth_data['token']:
                    return JsonResponse({'status':200, 'message':'Authentification réussie.', 'token':auth_data['token']})
                return JsonResponse({'status':500, 'message':str('Impossible de s\'authentifier')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite, veuillez contacter l\'administrateur!')})
        return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})        

#Request for payment fees
class requestPaymentFee(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            token       = data['paymenttoken']
            amount      = data['amount']
            serviceid   = data['serviceid']
            
            #Process Auth
            comformdata = {
                'token'         : token,
                'service_id'    : serviceid,
                'app_id'        : AFPAY_API_PUBLIC_KEY,
                'amount'        : amount
            }
            response_reqcom = requests.post(f'{AFPAY_BASE_URL}afpay-gateway-commission', data=comformdata)
            if response_reqcom.status_code == 200: 
                commission_req_data = response_reqcom.json()
                if commission_req_data['status'] == 200:
                    result = commission_req_data['result']
                    return JsonResponse({'status':200, 'message':'Authentification réussie.', 'result':result})
                return JsonResponse({'status':500, 'message':str('Impossible de s\'authentifier')})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite, veuillez contacter l\'administrateur!')})
        return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})  

#PayItemID Api Payment
class requestPayItemID(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            #initial variable
            token               = data['paymenttoken']
            serviceid           = data['servicecode'] 
        
            BEARER_TOKEN = urlsafe_base64_encode(str(f'{AFPAY_API_PUBLIC_KEY}:{AFPAY_API_KEY_SECRET}').encode('utf-8'))
            cashoutparams = {
                'token'         : token,
                'service_id'    : serviceid,
                'app_id'        : AFPAY_API_PUBLIC_KEY
            }
            cashoutheaders = {
                'Authorization' : f'Bearer {BEARER_TOKEN}'
            }
            response_cashout = requests.get(f'{AFPAY_BASE_URL}afpay-gateway-cashout', params=cashoutparams, headers=cashoutheaders)
            if response_cashout.status_code == 200:
                cashout_data = response_cashout.json()
                result = {
                    'payItemId'     : cashout_data['result'][0]['payItemId'],
                    'serviceid'     : cashout_data['result'][0]['serviceid']
                }
                return JsonResponse({'status':200, 'message':'Payement initier avec succès', 'result':result})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite, veuillez contacter l\'administrateur!')})
        return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})  

#GetQuote Api Payment
class requestQuoteID(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            #initial variable
            token               = request.POST['paymenttoken']
            serviceid           = request.POST['serviceid']
            payItemId           = request.POST['payItemId']
            amount              = request.POST['amount']
        
            BEARER_TOKEN = urlsafe_base64_encode(str(f'{AFPAY_API_PUBLIC_KEY}:{AFPAY_API_KEY_SECRET}').encode('utf-8'))
            getquoteformdata = {
                'token'         : token,
                'service_id'    : serviceid,
                'app_id'        : AFPAY_API_PUBLIC_KEY,
                'payItemId'     : payItemId,
                'amount'        : amount
            }
            getquoteheaders = {
                'Authorization' : f'Bearer {BEARER_TOKEN}'
            }
            response_getquote = requests.post(f'{AFPAY_BASE_URL}afpay-gateway-request-quote', data=getquoteformdata, headers=getquoteheaders)
            if response_getquote.status_code == 200:
                getquote_data = response_getquote.json() 
                if getquote_data['status'] == 200:
                    result = {
                        'quoteId'   : getquote_data['result']['quoteId'],
                        'serviceid' : serviceid
                    }
                    return JsonResponse({'status':200, 'message':'Payement initier avec succès', 'result':result})
                return JsonResponse({'status':500, 'message':getquote_data['message']})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite, veuillez contacter l\'administrateur!')})
        return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})  

#Trid generator
def trid_generator():
    """
    Generates a unique 8-digit alphanumeric code.
    """
    # Generate an 8-character random string
    code = get_random_string(length=8)
    return code

#Collection Api Payment
class postCollection(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            #initial variable
            token                   = request.POST['paymenttoken']
            quoteId                 = request.POST['quoteId']
            description             = request.POST['description']
            amount                  = request.POST['amount']
            currency                = request.POST['currency']
            customer_phone_number   = request.POST['customer_phone_number']
            customerEmailaddress    = request.POST['customer_email']
            customer_name           = request.POST['customer_name']
            serviceid               = request.POST['serviceid']
            command                 = Commands.objects.get(id=int(request.POST['command']))
            customer                = Persons.objects.get(user=request.user)
            trid                    = trid_generator()
            BEARER_TOKEN = urlsafe_base64_encode(str(f'{AFPAY_API_PUBLIC_KEY}:{AFPAY_API_KEY_SECRET}').encode('utf-8'))
            collectionpostdata = {
                'token'                 : token,
                'service_id'            : serviceid,
                'app_id'                : AFPAY_API_PUBLIC_KEY,
                'quoteId'               : quoteId,
                'customerPhonenumber'   : customer_phone_number,
                'customerEmailaddress'  : customerEmailaddress,
                'customerName'          : customer_name,
                'customerAddress'       : customer.address if customer.address != '' else customer.city.name,
                'description'           : description,
                'trid'                  : trid,
                'initial_amount'        : amount
                
            }
            collectionheaders = {
                'Authorization' : f'Bearer {BEARER_TOKEN}'
            }
            response_collection = requests.post(f'{AFPAY_BASE_URL}afpay-gateway-request-collection', data=collectionpostdata, headers=collectionheaders)
            if response_collection.status_code == 200:
                data_collection = response_collection.json()
                if data_collection['status'] == 200:
                    
                    channel = None
                    if serviceid == 30056:
                        channel = 'Orange Money'
                    if serviceid == 20056:
                        channel = 'MTN Mobile Money'
                        
                    #create the command
                    try:
                        Payments.objects.create(
                            customer                = customer,
                            command                 = command,    
                            transaction_ref         = data_collection['transaction_ref'],
                            currency                = currency,
                            transactionStatus       = 'PENDING',
                            mobile_operator_code    = channel,
                            mobileWalletNumber      = customer_phone_number,
                            MobileWcustomerName     = customer_name,
                            description             = 'Paiement de la commande FSTORE-CMD{} par le client {}'.format(command.pk, customer.user.get_full_name()),
                            amount                  = amount,
                        )
                        
                        result = {
                            'transaction_ref'   : data_collection['transaction_ref'],
                            'serviceid'         : serviceid
                        }
                        return JsonResponse({'status':200, 'message':'En attente de validation.', 'result':result})
                    except Exception as error:
                        print(error)
                        return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite, veuillez contacter l\'administrateur!')})
                return JsonResponse({'status':500, 'message':str('Impossible d\'effectuer le paiement'), 'result':response_collection.json()})
            return JsonResponse({'status':500, 'message':str('Une erreur c\'est produite, actualisez la page et reéssayez.')})
        return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')}) 

# Request Payment Status 
class requestPaymentStatus(CsrfExemptMixin, generic.View):
    def post(self, request, *args, **wargs):
        data = json.loads(request.body.decode("utf8"))
        user_data = jwt.decode(data["token"], 'Eg{x%^_~&Jxv%D**jZBPvMMXv/brp0', algorithms='HS256')
        USER = User.objects.get(username=user_data["user"])
        if USER:
            transaction_ref             = request.POST['transaction_ref']
            serviceid                   = request.POST['servicecode']
            token                       = request.POST['paymenttoken']
            person                      = Persons.objects.get(user=request.user)
            payment                     = Payments.objects.get(customer=person, transaction_ref=transaction_ref)
            response_message            = ''
            status_code                 = 200 
            
            BEARER_TOKEN = urlsafe_base64_encode(str(f'{AFPAY_API_PUBLIC_KEY}:{AFPAY_API_KEY_SECRET}').encode('utf-8'))
            statusparams = {
                'token'         : token,
                'service_id'    : serviceid,
                'app_id'        : AFPAY_API_PUBLIC_KEY,
                'ptn'           : transaction_ref
            }
            statusheaders = {
                'Authorization' : f'Bearer {BEARER_TOKEN}'
            }
            
            response_status = requests.get(f'{AFPAY_BASE_URL}afpay-gateway-transaction-status', params=statusparams, headers=statusheaders)
            if response_status.status_code == 200:
                status_data = response_status.json()
                if status_data['transactionStatus'] == 'SUCCESS':
                    payment.is_pay                  = True 
                    payment.transactionStatus       = status_data['transactionStatus']
                    payment.fee                     = status_data['transaction_fees']
                    payment.save()
                
                    status_code         = 200
                    trans_fees          = status_data['transaction_fees']

                    company_fees        = 0
                    provider_commission = 0
                    if payment.command.basket:
                        for item in ProductBaskets.objects.filter(basket=payment.command.basket):
                            company_fees        = Decimal(company_fees) + (Decimal(item.product.commission_company) * Decimal(item.one_price) / 100)
                            provider_commission = Decimal(provider_commission) + (Decimal(item.product.commission_provider) * Decimal(item.one_price) / 100)
                    else:
                        company_fees        = Decimal(payment.command.product.commission_company) * Decimal(payment.command.total_price) / 100 
                        provider_commission = Decimal(payment.command.product.commission_provider) * Decimal(payment.command.total_price) / 100

                    #update the finalcial statement
                    Finances.objects.create(
                        command                 = payment.command,
                        total_price             = payment.amount,
                        bank_commission         = trans_fees,
                        delivered_commission    = payment.command.delivery.price if payment.command.is_delivery else 0,
                        company_commission      = company_fees,
                        provider_commission     = provider_commission,
                    )
                    
                    #update command payment status
                    command                     = Commands.objects.get(id=payment.command.pk)
                    command.is_pay              = True
                    command.save()

                    response_message = 'Votre commande a été validé nous vous enverrons une notification aussitôt. Merci!'
                    return JsonResponse({'status':status_code, 'message':response_message})
                elif status_data['status'] == 403:
                    return JsonResponse({'status':403, 'message':'En attente de validation...'})
                else:
                    return JsonResponse({'status':500, 'message':status_data['message']})
            return JsonResponse({'status':500, 'message':'Impossible de verifier le status de la transaction, contactez l\'administrateur'})
        return JsonResponse({'status':500, 'message':str('Vous n\'êtes pas autoriser à effectuer cette action. Veuillez vous authentifié')})  






