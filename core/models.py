from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.timezone import now
from os.path import splitext
from uuid import uuid4
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from django_extensions.db.fields import AutoSlugField
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from fstore.settings import *
from cities_light.models import City, Country

# Create your models here.

class UUIDFileStoragePP(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('pp', uuid4().hex + ext)

class UUIDFileStorageCOVER(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('cover', uuid4().hex + ext)

class UUIDFileStorageIDRECTOVERSO(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('identificationID', uuid4(  ).hex + ext)

class Persons(models.Model):
    user                            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    referral                        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=_('Reference'), null=True)
    googlemap                       = models.CharField(max_length=1024, verbose_name=_('Lien google map du lieu physique'), null=True) 
    type_identification             = models.IntegerField(default=1, verbose_name=_('Type de la pièce d\'identité'), null=True)
    identification                  = models.FileField(upload_to='cni_recto_verso', storage=UUIDFileStorageIDRECTOVERSO(),  verbose_name=_("Pièce d'identification"), null=True)
    identificationID                = models.CharField(max_length=1024, verbose_name=_('Numéro de la pièce identité'), null=True )
    phone                           = models.CharField(verbose_name=_('Numero de telephone'), max_length=255, null=True)
    whatsapp_phone                  = models.CharField(verbose_name=_('Numero de telephone Whatsapp'), max_length=255, null=True)
    country                         = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'), null=True) 
    city                            = models.ForeignKey(City, on_delete=models.CASCADE,  verbose_name=_('City'), null=True)
    address                         = models.CharField(max_length=254, verbose_name=_('Adresse')) 
    codepostal                      = models.CharField(max_length=254, verbose_name=_('Boite Postal'), null=True) 
    birthday_date                   = models.DateField(verbose_name=_('Date de naissance'), null=True)
    sexe                            = models.CharField(max_length=254, verbose_name=_('Sexe'), null=True)
    language                        = models.CharField(max_length=20, verbose_name=_('Adresse'), default='french') 
    currency                        = models.CharField(max_length=10, verbose_name=_('Monnaie'), default='XAF') 
    rate                            = models.IntegerField(verbose_name=_('Mention de lutilisateur'), default=0)
    pp                              = models.FileField(upload_to='pp', storage=UUIDFileStoragePP(), verbose_name=_('Image de profile'), null=True)
    cover                           = models.FileField(upload_to='cover', storage=UUIDFileStorageCOVER(), verbose_name=_('Image de couverture du profile'), null=True)
    is_staff                        = models.BooleanField(default=False, editable=True,  verbose_name=_('Staff ou Pas'))
    is_customer                     = models.BooleanField(default=False, editable=True,  verbose_name=_('Client ou Pas'))
    is_verified                     = models.BooleanField(default=False, editable=True,  verbose_name=_('Compte Verifier ou pas'))
    googleauthenticator             = models.BooleanField(default=False, editable=True,  verbose_name=_('Google Authenticator Actif ou pas'))
    twofactor                       = models.BooleanField(default=False, editable=True,  verbose_name=_('Authentification a deux facteurs Actif ou pas'))
    googlemapservice                = models.BooleanField(default=False, editable=True,  verbose_name=_('Service Google Map Actif ou pas'))
    pushconfirmnotification         = models.BooleanField(default=False, editable=True,  verbose_name=_('Push Notification pour confirmation Actif ou pas'))
    smsconfirmnotification          = models.BooleanField(default=False, editable=True,  verbose_name=_('Sms Notification pour confirmation Actif ou pas'))
    emailconfirmnotification        = models.BooleanField(default=False, editable=True,  verbose_name=_('Email Notification pour confirmation Actif ou pas'))
    pushremindnotification          = models.BooleanField(default=False, editable=True,  verbose_name=_('Push Notification des rappels Actif ou pas'))
    smsremindnotification           = models.BooleanField(default=False, editable=True,  verbose_name=_('Sms Notification des rappels Actif ou pas'))
    emailremindnotification         = models.BooleanField(default=False, editable=True,  verbose_name=_('Email Notification des rappels Actif ou pas'))
    pushpricealertnotification      = models.BooleanField(default=False, editable=True,  verbose_name=_('Push Notification des prix d\'alert Actif ou pas'))
    smspricealertnotification       = models.BooleanField(default=False, editable=True,  verbose_name=_('Sms Notification des prix d\'alert Actif ou pas'))
    emailpricealertnotification     = models.BooleanField(default=False, editable=True,  verbose_name=_('Email Notification des prix d\'alert Actif ou pas'))
    pushdiscountnotification        = models.BooleanField(default=False, editable=True,  verbose_name=_('Push Notification des offres Actif ou pas'))
    smsdiscountnotification         = models.BooleanField(default=False, editable=True,  verbose_name=_('Sms Notification des offres Actif ou pas'))
    emaildiscountnotification       = models.BooleanField(default=False, editable=True,  verbose_name=_('Email Notification des offres Actif ou pas'))
    is_active                       = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'), help_text=_('Defini la visibilite'))
    is_online                       = models.BooleanField(default=False, editable=True,  verbose_name=_('En ligne'), help_text=_('Defini si l\'utilsateur est en ligne'))
    created_date                    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date                    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")
    last_updated_password_date      = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour du mot de passe")

    def __str__(self):
        return "{}".format(self.user.get_full_name())
    
#model code activation
class AccountActivationCode(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('Information de lutilisateur'))
    code = models.IntegerField(verbose_name=_('Code de validation'))
    is_expired = models.BooleanField(default=False, verbose_name=_("Code Expirer ou pas"))
    is_active = models.BooleanField(default=True, verbose_name=_("Client actif ou pas"))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name=_("Date de mise a jour"))

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return "{}".format(self.person)   

#model user Session
class Sessions(models.Model):
    person                  = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('Information de lutilisateur'))
    login_time              = models.DateTimeField(default=now, editable=False, verbose_name="Date et heur de connexion")
    logout_time             = models.DateTimeField(default=now, editable=False, verbose_name="Date et heur de Deconnexion")
    location                = models.TextField(verbose_name=_('Localisation')) 
    devise                  = models.TextField(verbose_name=_('Appareil utiliser')) 
    ip_address              = models.TextField(verbose_name=_('Adresse IP utiliser')) 
    mac_address             = models.TextField(verbose_name=_('Adresse MAC de l\'appareil utiliser')) 
    is_active               = models.BooleanField(default=True, verbose_name=_("Session active ou pas"))
    created_date            = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return "{}".format(self.person) 

############################################################Models de gestions des menus########################################################
class Menus(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Intitulé du role'))
    code =  models.IntegerField(verbose_name=_('Code du menu'), null=True)
    link =  models.CharField(max_length=255, verbose_name=_('Lien du menu'), null=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Createur du menu'), null=True)
    is_active = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'), help_text=_('Defini la visibilite'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return "{}".format(self.title) 

class ParentMenus(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Intitulé du menu parent'))
    label = models.TextField(verbose_name=_('Label du menu parent'), null=True)
    icon = models.CharField(max_length=25, verbose_name=_('Icon du menu parent'), null=True)
    menus = models.ManyToManyField(Menus, verbose_name=_('Menu Enfant lier'))
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Createur du menu'), null=True)
    is_active = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'), help_text=_('Defini la visibilite'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return "{}".format(self.title) 
    
class MenuRules(models.Model):
    label = models.CharField(max_length=255, verbose_name=_('Libeller du role'), null=True)
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE, verbose_name=_('Menu Concerner'), null=True)
    can_read = models.BooleanField(default=False, editable=True,  verbose_name=_('Peut Lire'))
    can_create = models.BooleanField(default=False, editable=True,  verbose_name=_('Peut Créer'))
    can_update = models.BooleanField(default=False, editable=True,  verbose_name=_('Peut Mettre a jour'))
    can_delete = models.BooleanField(default=False, editable=True,  verbose_name=_('Peut Supprimer'))
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Createur du menu'), null=True)
    is_active = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'), help_text=_('Defini la visibilite'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return "{}".format(self.menu) 
 
class Profil(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Intitulé du role'))
    permissions = models.ManyToManyField(MenuRules, verbose_name=_('Menu lier au role'))
    description = RichTextField(verbose_name=_('Description du role'))
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Createur du role'), null=True)
    is_active = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'), help_text=_('Defini la visibilite'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return "{}".format(self.title) 
    
class UserProfil(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('Personne ayant acces au center'))
    profil = models.ForeignKey(Profil,on_delete=models.CASCADE, verbose_name=_('Profil Attribuer a lutilisateur'), null=True)
    description = RichTextField(verbose_name=_('Commentaire'))
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Personne ayant attribuer'), null=True)
    is_active = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'), help_text=_('Defini la visibilite'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return "{}".format(self.person.user.get_full_name()) 