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
from ckeditor_uploader.fields import RichTextUploadingField
from core.models import Persons
from cities_light.models import City, Country

# Create your models here.

class UUIDFileStorageCOVER(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('cover', uuid4().hex + ext)
    
class UUIDFileStorageBILL(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('bill', uuid4().hex + ext)
    
class UUIDFileStorageIMAGE(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('image', uuid4().hex + ext)

class UUIDFileStorageVIDEO(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('video', uuid4().hex + ext)
    
class UUIDFileStoragePRESENTATION(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('presentation', uuid4().hex + ext) 

class UUIDFileStorageFILE(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('file', uuid4().hex + ext) 
    
class UUIDFileStorageLOGO(FileSystemStorage):
    def get_available_name(self, name, max_length=None): 
        _, ext = splitext(name)
        return os.path.join('logo', uuid4().hex + ext) 

class CompanyConditions(models.Model):
    title               = models.TextField(verbose_name=_('Titre de la Condition'))
    description         = RichTextField(verbose_name=_('Contenu de la condition'))
    is_approved         = models.BooleanField(default=False, verbose_name=_('Partner Approuvé ou pas'))
    approved_by         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=('ConditionAdminAppouved'), null=True)
    is_active           = models.BooleanField(default=True, verbose_name=_('Actif ou pas'))
    create_by           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_date        = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
class CompanyPolicies(models.Model):
    title = models.TextField(verbose_name=_('Titre de la politique'))
    description = RichTextField(verbose_name=_('Contenu de la politique'))
    is_approved = models.BooleanField(default=False, verbose_name=_('Partner Approuvé ou pas'))
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=('PolicyAdminAppouved'), null=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Actif ou pas'))
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class CompanyPhones(models.Model):
    phone = models.TextField(verbose_name=_('Telepehone de lentreprise'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.phone)
    
class CompanyEmails(models.Model):
    email = models.TextField(verbose_name=_('Email de lentreprise'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.email)

class CompanySocial(models.Model):
    name = models.TextField(verbose_name=_('nom du reseau social'))
    faicon = models.TextField(verbose_name=_('indicatif de licon du reseau social'))
    link = models.URLField(verbose_name=_('lien du reseau social'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.name)

class CompanyValues(models.Model):
    label = models.TextField(verbose_name=_('Libeller de lentreprise'))
    value = models.TextField(verbose_name=_('Valeur'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.label)
    
class CompanyPresentation(models.Model):
    label = models.TextField(verbose_name=_('Libeller de lentreprise'))
    description = RichTextField(verbose_name=_('Description de lentreprise'))
    video = models.FileField(upload_to='company-video', storage=UUIDFileStoragePRESENTATION(), verbose_name=_('Presentation'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.label)
    
class CompanyAddress(models.Model):
    continent = models.TextField(verbose_name=_('continent'))
    country = models.TextField(verbose_name=_('country'))
    city = models.TextField(verbose_name=_('city'))
    address = models.TextField(verbose_name=_('address'))
    postal = models.IntegerField(verbose_name=_('Boite postal'))
    is_default = models.BooleanField(default=False, verbose_name=_('Adresse par default'))
    is_active = models.BooleanField(default=True, verbose_name=_('Adresse actif ou pas'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{} {} {}".format(self.continent, self.country, self.city)

class CompanyPartner(models.Model):
    name = models.TextField(verbose_name=_('nom du partenaire'))
    description = RichTextField(verbose_name=_('Description sur le partenaire'), null=True)
    link = models.URLField(verbose_name=_('lien de la plateforme du partenaire'))
    logo = models.FileField(upload_to='company-partner-logo', storage=UUIDFileStorageLOGO(), verbose_name=_('Logo du partenaire'), null=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False, verbose_name=_('Partner Approuvé ou pas'))
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=('PartnerAdminAppouved'), null=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Partner actif ou pas'))
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.name)
    
class CompanyDeliveryZone(models.Model):
    title           = models.TextField(verbose_name=_('Nom du lieu'))
    description     = RichTextField(verbose_name=_('Description du lieu'), null=True)
    googlemap       = models.TextField(verbose_name=_('map Zone'), null=True)
    price           = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Commission sur les ventes", default=0)
    create_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_approved     = models.BooleanField(default=False, verbose_name=_('Certification Approuvé ou pas'))
    approved_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=('CompanyDeliveryZoneAdminAppouved'), null=True)
    is_active       = models.BooleanField(default=True, verbose_name=_('Partner actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.title)

class Company(models.Model):
    name                = models.TextField(verbose_name=_('Nom de lentreprise'))
    vision              = models.TextField(verbose_name=_('Vision de lentreprise'))
    mission             = models.TextField(verbose_name=_('mission de lentreprise'))
    description         = RichTextField(verbose_name=_('Description de lentreprise'), null=True)
    presentations       = models.ManyToManyField(CompanyPresentation, verbose_name=_('List des presentation de lentreprise'))
    mission             = models.TextField(verbose_name=_('mission de lentreprise'), null=True)
    logo                = models.FileField(upload_to='company-logo', storage=UUIDFileStorageLOGO(), verbose_name=_('Logo de lentreprise'), null=True)
    phones              = models.ManyToManyField(CompanyPhones, verbose_name=_('telephone de lentreprise'))
    emails              = models.ManyToManyField(CompanyEmails, verbose_name=_('email de lentreprise'))
    socials             = models.ManyToManyField(CompanySocial, verbose_name=_('reseau social de lentreprise'))
    values              = models.ManyToManyField(CompanyValues, verbose_name=_('Valeur de lentreprise'))
    partners            = models.ManyToManyField(CompanyPartner, verbose_name=_('Partenaire de lentreprise'))
    addresses           = models.ManyToManyField(CompanyAddress, verbose_name=_('Adresses de lentreprise'))
    create_by           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    slug                = AutoSlugField(populate_from=['name'])
    created_date        = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.name)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
# Model des Monaies
class Currency(models.Model):
    creator                         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    currency_origin_country         = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Pays origin")
    currency_origin_code            = models.CharField(null=True, max_length=256, verbose_name="Code de la devise d\'origine")
    currency_destination_country    = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Pays de destination", related_name=_('Destination'))
    currency_destination_code       = models.CharField(null=True, max_length=256, verbose_name="Nom de la devise à obtenir")
    exchange_rate                   = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Taux echange", default=0)
    is_default                      = models.BooleanField(default=False, editable=True, verbose_name="Par default ou pas")
    is_active                       = models.BooleanField(default=True, editable=True, verbose_name="Visible ou pas")
    created_date                    = models.DateTimeField(default=now, editable=False)
    updated_date                    = models.DateTimeField(default=now, editable=True)
    
    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{} {}".format(self.currency_origin_country.name, self.currency_destination_country.name)
    
# Model des Taxes
class Taxes(models.Model):
    creator         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    name            = models.CharField(null=True, max_length=256, verbose_name="Intituler de la taxe")
    country         = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Pays")
    vat             = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Pourcentage de la taxe")
    is_default      = models.BooleanField(default=False, editable=True, verbose_name="Par default ou pas")
    is_active       = models.BooleanField(default=True, editable=True, verbose_name="Visible ou pas")
    created_date    = models.DateTimeField(default=now, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True)
    
    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.country)
    
# categories grant childreen
class categoriesGrantChild(models.Model):
    creator         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    name            = models.CharField(blank=False, max_length=256, verbose_name=_('Catégorie Petite Fille'))
    is_active       = models.BooleanField(default=True, editable=True, verbose_name=_('Actif ou pas'))
    created_date    = models.DateTimeField(default=now, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)
    
# categories childreen
class categoriesChild(models.Model):
    creator             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    grantchilds         = models.ManyToManyField(categoriesGrantChild, verbose_name=_('Liaison avec la catégorie Ptite Fille'))
    name                = models.CharField(max_length=256, verbose_name=_('Nom de la Catégorie Fille'))
    is_active           = models.BooleanField(default=True, editable=True, verbose_name=_('Actif ou pas'))
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)

# categories of products (parents category)
class parentCategory(models.Model):
    creator             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    childs              = models.ManyToManyField(categoriesChild)
    name                = models.CharField(blank=False, max_length=256, verbose_name=_('Nom de la catégorie parente'))
    cover               = models.FileField(upload_to="category_image/cover/", verbose_name=_('Photo de couveture de la categorie parente'))
    is_active           = models.BooleanField(default=True, editable=True, verbose_name=_('Actif ou pas'))
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)

#Brands Model
class Brands(models.Model):
    creator             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    categories          = models.ManyToManyField(parentCategory, verbose_name="Les Categories lié à la marque")
    name                = models.CharField(null=True, max_length=256, verbose_name="Nom de la marque")
    logo                = models.FileField(upload_to="marque/logo/", verbose_name="Logo de la marque", null=True)
    is_approved         = models.BooleanField(default=False, editable=True, verbose_name=_('Valider ou pas')) 
    approved_by         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="BrandApprouvedByAdmin", null=True)
    is_active           = models.BooleanField(default=True, editable=True, verbose_name="La marque s'affiche dans le shopping ou pas")
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)
    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)
    
#Providers Models
class Providers(models.Model):
    creator             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    name                = models.CharField(null=True, max_length=256, verbose_name="Nom de la marque")
    logo                = models.FileField(upload_to="provider/logo/", verbose_name="Logo de la marque", null=True)
    is_approved         = models.BooleanField(default=False, editable=True, verbose_name=_('Valider ou pas')) 
    approved_by         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ProviderApprouvedByAdmin", null=True)
    is_active           = models.BooleanField(default=True, editable=True, verbose_name="La marque s'affiche dans le shopping ou pas")
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)
    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)
    
# Product images
class ProductImages(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    label = models.CharField(max_length=256, verbose_name=_("Label Image"), null=True)
    image = models.FileField(upload_to="product/images/", verbose_name=_("car Images"), storage=UUIDFileStorageIMAGE)
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_("Image Active ou pas"))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)
    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.label)
    
# product videos
class ProductVideos(models.Model):
    creator         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    label           = models.CharField(max_length=256, verbose_name="Label Image", null=True)
    video           = models.FileField(upload_to="product/videos/", verbose_name="car Videos", storage=UUIDFileStorageVIDEO)
    is_active       = models.BooleanField(default=True, editable=True, verbose_name="Video active ou pas")
    created_date    = models.DateTimeField(default=now, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True)
    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.label)

#Products Models
class Products(models.Model):
    creator             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    provider            = models.ForeignKey(Providers, on_delete=models.CASCADE, verbose_name="Infos sur le fournisseur")
    name                = RichTextField(verbose_name=_('Intituler du produit'))
    description         = RichTextField(verbose_name=_('Description du produit'))
    presentation        = RichTextUploadingField(verbose_name=_('Contenu de la presentation du produit'))
    price               = models.DecimalField(decimal_places=2, max_digits=17, verbose_name="prix hors tax", null=True)
    discount            = models.DecimalField(decimal_places=2, max_digits=17, verbose_name="Montant a reduire", default=0)
    quantity            = models.IntegerField(null=True, verbose_name="quantite")
    brand               = models.ForeignKey(Brands, on_delete=models.CASCADE, verbose_name=_('La marque du produit'), null=True)
    category            = models.ForeignKey(categoriesGrantChild, on_delete=models.CASCADE, verbose_name=_('La catégorie du produit'), null=True)
    slug                = AutoSlugField(populate_from=['name'])
    images              = models.ManyToManyField(ProductImages, verbose_name=_('Images du produit'))
    videos              = models.ManyToManyField(ProductVideos, verbose_name=_('Videos du produit'))
    weigth              = models.CharField(max_length=250, verbose_name=_('poids'), null=True)
    height              = models.CharField(max_length=250, verbose_name=_('hauteur'), null=True)
    width               = models.CharField(max_length=250, verbose_name=_('largeur'), null=True)
    depth               = models.CharField(max_length=250, verbose_name=_('profondeur'), null=True)
    commission_provider = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_("Pourcentage de la commission du fournisseur"), default=0)
    commission_company  = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_("Pourcentage de la commission de lentreprise"), default=0)
    is_approved         = models.BooleanField(default=False, editable=True, verbose_name=_('Valider ou pas')) 
    approved_by         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="productApprouvedByAdmin", null=True)
    is_taxable          = models.BooleanField(default=False, editable=True, verbose_name=_('Produit taxable ou pas')) 
    delete_by_owner     = models.BooleanField(default=False, editable=True, verbose_name=_('Produit supprimer parle proprio ou pas')) 
    is_active           = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)

    def exist(self):
        if Products.objects.filter(slug=self.slug).exists():
            return True
        else:
            return False
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Gestion des tailles
class DefaultSize(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    name = models.CharField(null=True, max_length=255, verbose_name=_('Valeur de la taille'))
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)

# default color class
class DefaultsColors(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    name = models.CharField(blank=False, max_length=255, verbose_name=_('choix de couleur'))
    code = models.CharField(blank=False, max_length=255, verbose_name=_('code de couleur'), null=True)
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)

# default color class
class DefaultsMaterial(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    name = models.CharField(blank=False, max_length=255, verbose_name=_('Nom de la matiere'))
    description = RichTextField(verbose_name=_('Description du materiau'), null=True)
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.name)

# Product Caracteristique
class ProductCaracteristque(models.Model):
    creator         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur")
    product         = models.ForeignKey( Products, on_delete=models.CASCADE, verbose_name=_('Product concerné'))
    color           = models.ManyToManyField(DefaultsColors, verbose_name=_('choix des couleurs du produit'))
    size            = models.ManyToManyField(DefaultSize, verbose_name=_('choix tailles du produits'))
    material        = models.ManyToManyField(DefaultsMaterial,  verbose_name="choix des matières du produit")
    is_active       = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date    = models.DateTimeField(default=now, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.product)

#enregistrement des produits en promotions
class PromotionsProducts(models.Model):
    creator         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    product         = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('information sur le produit'))
    date_start      = models.DateTimeField(verbose_name=_('Date de debut de la promotion'))
    date_end        = models.DateTimeField(verbose_name=_('Date de debut de la promotion'))
    promo_price     = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('Prix promotionnel'), default=0)   
    is_active       = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date    = models.DateTimeField(default=now, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.product)

#################################################################################################################
###########################################GESTION DES SPONSORING DES PRODUITS###################################
#################################################################################################################
######manage Block Sponsoring
class SponsoringManageBlock(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    name = models.CharField(max_length=256, verbose_name="nom du block")
    code = models.CharField(max_length=50, verbose_name="Code du block")
    is_active = models.BooleanField(default=True, verbose_name=_('Rendre le block visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.name)

#forfait de sponsoring
class SponsoringBooking(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    code_zone = models.ForeignKey(SponsoringManageBlock, on_delete=models.CASCADE, verbose_name="Info sur la zone", null=True)
    name = models.CharField(max_length=512, verbose_name=_('Intituler du forfait'))
    periode = models.CharField(max_length=512, verbose_name=_('duree du sponsoring en heur'))
    sponsoring_price = models.DecimalField(decimal_places=2, max_digits=17, null=True, verbose_name=_('Prix du sponsoring'))
    is_active = models.BooleanField(default=False, editable=True, verbose_name=_('Sponsoring visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.name)
    
###################################Banniere principale ####################"
class BannerPubs(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    title = models.CharField(max_length=512, verbose_name="titre")
    cover = models.FileField(blank=False, upload_to="product_image/banner/", verbose_name="Banniere accueil")
    link = models.CharField(max_length=512, verbose_name="lien de redirection")
    is_external = models.BooleanField(default=False, editable=True, verbose_name="Lien externe")
    is_approved = models.BooleanField(default=False, editable=True, verbose_name=_('Valider ou pas')) 
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bannerPubApprouvedByAdmin", null=True)
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('Visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.title)
    
#enregistrement des produits sponsoriser sur espace pub ou sur la banniere principale
class SponsoringProducts(models.Model): 
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Infos sur l'auteur", null=True)
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE,verbose_name=_('information sur le magasin'), null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('information sur le produit'))
    booking = models.ForeignKey(SponsoringBooking, on_delete=models.CASCADE, verbose_name=_('Forfait choisie pour le produit'), null=True)
    banner = models.ForeignKey(BannerPubs, on_delete=models.CASCADE, verbose_name=_('Sponsoring de la banniere'), null=True)
    start_date = models.DateTimeField(verbose_name=_('Date de début du sponsoring'), null=True)
    end_date = models.DateTimeField(verbose_name=_('Date de fin du sponsoring'), null=True)
    is_approved = models.BooleanField(default=False, editable=True, verbose_name=_('Valider ou pas')) 
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sponsoringApprouvedByAdmin", null=True)
    is_active = models.BooleanField(default=False, editable=True, verbose_name=_('Sponsoring visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.product)

#######################################################################################################
############################################CUSTOMER ACTION############################################
#######################################################################################################
#User Favorite Data
class FavoriteProducts(models.Model): 
    customer = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('Clients concerné'))
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('information sur le produit'))
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('Favoris visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.product)
    
    def count_favorite(self, product):
        count = FavoriteProducts.objects.filter(customer=self.customer, product=product, is_active=True).count()
        return count
    
#User Rating Data
class RatingProducts(models.Model): 
    customer = models.ForeignKey(Persons,  on_delete=models.CASCADE, verbose_name=_('Client concerné'))
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('information sur le produit'))
    rate = models.IntegerField(verbose_name=_('Mention du client sur le produit'))
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('Favoris visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.product)
    
    def count_rate(product):
        count = RatingProducts.objects.filter(product=product, is_active=True).count()
        return count

#User Comment Data
class CommentProducts(models.Model): 
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('information sur le produit'))
    customer = models.ForeignKey(Persons,  on_delete=models.CASCADE, verbose_name=_('Client concerné'))
    comment = models.TextField(max_length=5000, verbose_name=_('Commentaire'))
    reply_comment = models.TextField(max_length=5000, verbose_name=_('Commentaire'))
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('Commentaire visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.product)
    
#User Like Comment
class LikeCommentProducts(models.Model): 
    customer = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('Client qui like'))
    comment = models.ForeignKey(CommentProducts,  on_delete=models.CASCADE, verbose_name=_('Commentaire concerné'))
    like = models.IntegerField(default=0, verbose_name=_('Valeur du like 0 ou 1'))
    is_active = models.BooleanField(default=True, editable=True, verbose_name=_('Like visible ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']

    def __str__(self):
        return "{}".format(self.customer.user.get_full_name())
    
    def count_like(comment):
        count = LikeCommentProducts.objects.filter(comment=comment).count()
        return count
    
#################################################################################################################
###################################################FINANCE AND COMMAND###########################################
#################################################################################################################
#create panier
class Baskets(models.Model):
    customer                = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('information sur l\'achéteur'), null=True)
    products                = models.ManyToManyField(Products, through='ProductBaskets', related_name=_('ProductListBasket'), verbose_name=_('Liste de produit du panier'))
    number_item             = models.IntegerField(verbose_name=_('Nombre d\'article dans le panier'))
    total_price             = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('prix total de la commande'), default=0)
    vat_price               = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('prix total de la commande avec taxe'), default=0)
    is_checkout             = models.BooleanField(default=False, editable=True, verbose_name=_('panier payer ou pas')) 
    is_active               = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date            = models.DateTimeField(default=now, editable=False)
    updated_date            = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.customer)
    
#Product Basket List
class ProductBaskets(models.Model):
    basket                      = models.ForeignKey(Baskets, on_delete=models.CASCADE, verbose_name=_('Panier Correspondant'))
    product                     = models.ForeignKey(Products, on_delete=models.CASCADE, related_name=_('OneProductBasket'))
    quantity                    = models.IntegerField(verbose_name=_('Nombre de pieces commander'))
    one_price                   = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('prix total'), default=0)
    is_pay                      = models.BooleanField(default=False, editable=True,verbose_name="Article acheter par le l\'acheteur ou pas")
    color                       = models.ForeignKey(DefaultsColors, on_delete=models.CASCADE, verbose_name=_('choix de la couleur du produit'), null=True)
    size                        = models.ForeignKey(DefaultSize, on_delete=models.CASCADE, verbose_name=_('choix de la taille du produit'), null=True)
    material                    = models.ForeignKey(DefaultsMaterial, on_delete=models.CASCADE, verbose_name=_("choix de la matiere du produit"), null=True)
    is_active                   = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date                = models.DateTimeField(default=now, editable=False)
    updated_date                = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['created_date']
    def __str__(self):
        return "{}".format(self.product.name)
    
class Commands(models.Model): 
    customer                            = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('information sur l\'achéteur'))
    basket                              = models.ForeignKey(Baskets, on_delete=models.CASCADE, verbose_name=_('Panier'), null=True)
    product                             = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('Produit achater directement sans passez par le panier'), null=True)
    sponsoring                          = models.ForeignKey(SponsoringProducts, on_delete=models.CASCADE, verbose_name=_('Sponsoring'), null=True)
    item_number                         = models.IntegerField(verbose_name=_('Nombre de pieces commander'))
    details                             = RichTextField(verbose_name=_('Detail de la commande'))
    total_price                         = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('prix total de la commande'), default=0)
    vat_price                           = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('prix total de la commande avec taxe'), default=0)
    is_shop_pickup                      = models.BooleanField(default=False, editable=True, verbose_name="Le client viendra lui prendre a la boutique ou pas (Pas de livraison)")
    is_delivery                         = models.BooleanField(default=False, editable=True, verbose_name="Commande a livrer ou pas")
    delivery                            = models.ForeignKey(CompanyDeliveryZone, on_delete=models.CASCADE, verbose_name=_('Point de livraison'), null=True)
    is_delivery_start                   = models.BooleanField(default=False, editable=True, verbose_name="Commande a livrer ou pas")
    delivery_start_datetime             = models.DateTimeField(verbose_name=_('Heure de debut'), null=True)
    is_delivery_end                     = models.BooleanField(default=False, editable=True, verbose_name="Commande livrer ou pas")
    delivery_end_datetime               = models.DateTimeField(verbose_name=_('Heure de fin'), null=True)
    quantity                            = models.IntegerField(verbose_name=_('Quantité de l\'article payer directement'), null=True)
    is_pay                              = models.BooleanField(default=False, editable=True, verbose_name="Commande valider ou pas")
    is_hide                             = models.BooleanField(default=False, editable=True, verbose_name="Commande visible pour le client ou pas")
    is_approved                         = models.BooleanField(default=False, editable=True, verbose_name=_('Commande Valider ou pas')) 
    approved_by                         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="CommandApprouvedByAdmin", null=True)
    is_rejected                         = models.BooleanField(default=False, editable=True, verbose_name="Commande Rejetter ou pas")
    color                               = models.ForeignKey(DefaultsColors, on_delete=models.CASCADE, verbose_name=_('choix de la couleur du produit'), null=True)
    size                                = models.ForeignKey(DefaultSize, on_delete=models.CASCADE, verbose_name=_('choix de la taille du produit'), null=True)
    material                            = models.ForeignKey(DefaultsMaterial, on_delete=models.CASCADE, verbose_name="choix de la matiere du produit", null=True)
    is_active                           = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date                        = models.DateTimeField(default=now, editable=False)
    updated_date                        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.customer)

class Payments(models.Model):
    customer                    = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('information sur lutilisateur'))
    command                     = models.ForeignKey(Commands, on_delete=models.CASCADE, verbose_name=_("Command"))
    transaction_ref             = models.CharField(max_length=100, verbose_name=_("Reference de la transaction"), null=True)
    currency                    = models.CharField(max_length=100, verbose_name=_("Monais utiliser"))
    transactionStatus           = models.CharField(max_length=100, verbose_name=_("Status de la transaction"))
    mobileWalletNumber          = models.CharField(max_length=100, verbose_name=_("Telephone utiliser"), null=True)
    MobileWcustomerName         = models.CharField(max_length=100, verbose_name=_("Nom du proprio du Wallet"), null=True)
    bankAccountNumber           = models.CharField(max_length=100, verbose_name=_("Numero de carte bancaire utiliser"), null=True)
    mobile_operator_code        = models.CharField(max_length=512, verbose_name="Code de loperateur", null=True)
    fee                         = models.DecimalField(max_digits=9, decimal_places=3, verbose_name=_('Montant total'), default=0.0)
    is_pay                      = models.BooleanField(default=False, verbose_name=_('Payement effectuer ou pas'))
    is_declined                 = models.BooleanField(default=False, verbose_name=_('Payement annuler ou pas')) 
    description                 = models.TextField(verbose_name=_("description"))
    amount                      = models.DecimalField(max_digits=9, decimal_places=3, verbose_name=_('Montant total'))
    is_active                   = models.BooleanField(default=True, verbose_name=_('Commande actif ou pas'))
    created_date                = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date                = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.customer)
    
class Finances(models.Model): 
    command                 = models.ForeignKey(Commands, on_delete=models.CASCADE, verbose_name=_('information sur la command'))
    total_price             = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('prix total de la commande'), default=0)
    bank_commission         = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('Frais Bancaire'), default=0)
    delivered_commission    = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('Montant à transmettre au Livreur'), default=0)
    provider_commission     = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('Montant à transmettre au Fournisseur'), default=0)
    company_commission      = models.DecimalField(decimal_places=2, max_digits=17, verbose_name=_('Montant à transmettre a lentreprise'), default=0)
    bank_is_pay             = models.BooleanField(default=False, editable=True, verbose_name="Le vendeur a ete payer ou pas")
    delivered_is_pay        = models.BooleanField(default=False, editable=True, verbose_name="Le livreur a ete payer ou pas")
    provider_is_pay         = models.BooleanField(default=False, editable=True, verbose_name="Fournisseur a ete payer ou pas")
    company_is_pay          = models.BooleanField(default=False, editable=True, verbose_name="Lentreprise a ete payer ou pas")
    is_active               = models.BooleanField(default=True, editable=True, verbose_name=_('visible ou pas')) 
    created_date            = models.DateTimeField(default=now, editable=False)
    updated_date            = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.command.details)

# Gestion des factures
class billCommand(models.Model):
    command             = models.ForeignKey(Commands, on_delete=models.CASCADE, verbose_name=_('commande origine de la facture'), null=True)
    bill                = models.FileField( upload_to="factures/", verbose_name=_('Facture Command'), storage=UUIDFileStorageBILL)
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
    def __str__(self):
        return "{}".format(self.command.customer)
    

###########################################################################################################
#############################################GESTION DES LITIGES###########################################
###########################################################################################################
# Gestion des litiges
class customersComplaints(models.Model):
    customer = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('information sur l\'acheteur'), related_name=_('CuatomerInfo'), null=True)
    command = models.ForeignKey(Commands, on_delete=models.CASCADE, verbose_name=_('commande origine du litige'), null=True)
    title = models.CharField(max_length=1024, verbose_name=_('titre du message'))
    message = RichTextField(null=True, verbose_name=_('Message'), help_text=('Message contenu du litige'))
    rep_message = RichTextField(null=True, verbose_name=_('Message Repondu'), help_text=_('Message contenu du litige'))
    is_resolv = models.BooleanField(default=False, editable=True, verbose_name=_('litige traiter ou pas'))
    created_date = models.DateTimeField(default=now, editable=False)
    updated_date = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['updated_date']
        
    def __str__(self):
        return "{} {}".format(self.title, self.customer)
    


###########################################################################################################
#############################################GESTION DU CUSTOMER SERVICE ##################################
###########################################################################################################
#Service du support
class customerSupportService(models.Model):
    creator              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Auteur'))
    title               = models.CharField(max_length=1024, verbose_name=_('titre du message'))
    description         = RichTextField(verbose_name=_('Description'), help_text=('Description'))
    is_payment_required = models.BooleanField(default=False, verbose_name=_('Payment requis pour ce service ou pas'))
    price               = models.DecimalField(decimal_places=2, max_digits=9, verbose_name=_('Frais du service'), default=0)
    is_approved        = models.BooleanField(default=False, verbose_name=_('Service Valider ou pas'))
    approved_by        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supportServiceApprouvedByAdmin", null=True)
    is_active           = models.BooleanField(default=True, verbose_name=_('Service actif ou pas'))
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['created_date']
    def __str__(self): 
        return "{}".format(self.title)
    
# Gestion des litiges
class customerSupportTicket(models.Model):
    creator              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Auteur'))
    owner               = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('information sur l\'utilisateur'))
    service             = models.ForeignKey(customerSupportService, on_delete=models.CASCADE, verbose_name=_('Service Choisie par le client'))
    command             = models.ForeignKey(Commands, on_delete=models.CASCADE, verbose_name=_('commande origine du litige'), null=True)
    resume              = models.TextField(verbose_name=_('resumer du probleme'), null=True)
    description         = RichTextField(null=True, verbose_name=_('Description'), help_text=('Description du litige'))
    progression_status  = models.IntegerField(default=0, verbose_name=_('Niveau de progression de la resolution du ticket'))
    is_resolv           = models.BooleanField(default=False, editable=True, verbose_name=_('litige traiter ou pas'))
    is_active           = models.BooleanField(default=True, verbose_name=_('Tiket actif ou pas'))
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['created_date']
    def __str__(self):
        return "{} {}".format(self.resume, self.owner.user.get_full_name())
    
#Tiket Discussions
class ticketMessage(models.Model):
    creator             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Auteur'))
    ticket              = models.ForeignKey(customerSupportTicket, on_delete=models.CASCADE, verbose_name=_('Information sur le Ticket'))
    owner               = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('information sur l\'utilisateur'))
    operator            = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('information lagent du litige'), related_name=_('Operateur'), null=True)
    message             = RichTextField(null=True, verbose_name=_('Message'), help_text=('Message contenu du litige'))
    attach              = models.FileField(upload_to="ticket/attach/", verbose_name="Fichier en attach au message", null=True)
    rep_message         = RichTextField(null=True, verbose_name=_('Message Repondu'), help_text=_('Message contenu du litige'))
    is_customer_message = models.BooleanField(default=False, editable=False, verbose_name=_('message du client'))
    is_operator_message = models.BooleanField(default=False, editable=False, verbose_name=_('message de loperateur'))
    is_active           = models.BooleanField(default=True, verbose_name=_('Message actif ou pas'))
    created_date        = models.DateTimeField(default=now, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True)

    class Meta:
        ordering = ['created_date']
    def __str__(self):
        return "{} {}".format(self.owner.user.get_full_name(), self.ticket.resume)
    
####################################################################
############################## MESSENGER ###########################
####################################################################
###Dialog Model
class Dialogs(models.Model):
    owner               = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Owner'))
    opponent            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Opponent'), related_name=_('Opponent'))
    block_by            = models.CharField(verbose_name=_("bloqué par"),blank=True ,max_length=255, null=True)
    owner_is_online     = models.BooleanField(verbose_name=_("owner_is_online"), default=True)
    opponent_is_online  = models.BooleanField(verbose_name=_("opponent_is_online"), default=True)
    is_active           = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'))
    created_date        = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date        = models.DateTimeField(default=now, editable=True, verbose_name=_("Date de mise a jour"))
    
    def __str__(self):
        return "{}".format(self.owner.username) 
    
#Messenges Model
class Messages(models.Model):
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_messages', on_delete=models.CASCADE, verbose_name=_("Auteur"))
    content             = models.TextField(verbose_name=_("Message_Text"))
    receiver            = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE, verbose_name=_("Destinataire"))
    idchat              = models.ForeignKey(Dialogs,on_delete=models.CASCADE, verbose_name=_("Id du Dialog"))
    read                = models.BooleanField(verbose_name=_("Lecture"), default=False)
    file                = models.FileField(upload_to='filechat', storage=UUIDFileStorageFILE(), null=True)
    supp_author         = models.BooleanField(verbose_name=_("supp_par_Aut"), default=False)
    supp_receiver       = models.BooleanField(verbose_name=_("supp_par_Dest"), default=False)
    answer              = models.TextField(verbose_name=_("Message_Repondu"), blank=True)
    answer_msg_author   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Response_MessageAuthor', on_delete=models.CASCADE, verbose_name=_("AuteurResponse"), null=True)
    is_active           = models.BooleanField(default=True, editable=True,  verbose_name=_('Actif'))
    key                 = models.IntegerField(default=1, verbose_name=_("Type de message... 1 text, 2 image, 3 video"))
    created_date        = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Date"))
    updated_date        = models.DateTimeField(auto_now=True, editable=True, verbose_name=_("Date de mise à jour"))

    def __str__(self):
        return "{}".format(self.author.username) 

####################################################################
################################## FAQ #############################
####################################################################
#FAQ Category Model
class FAQCategory(models.Model):
    creator         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Auteur'))
    title           = models.TextField(verbose_name=_('Titre de la Catégorie'))
    description     = RichTextField(verbose_name=_('Description'), null=True)
    is_active       = models.BooleanField(default=True, verbose_name=_('FAQ actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.title)

#Model FAQ
class FAQ(models.Model):
    creator         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Auteur'))
    category        = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, verbose_name=_('Category du FAQ'))
    title           = models.TextField(verbose_name=_('titre du FAQ'))
    label           = models.TextField(verbose_name=_('Label du FAQ'), null=True)
    subject         = RichTextField(verbose_name=_('Question'))
    content         = RichTextField(verbose_name=_('Reponse'))
    numberlike      = models.IntegerField(default=0, verbose_name=_('Nombre de jaime'))
    numberunlike    = models.IntegerField(default=0, verbose_name=_('Nombre de non jaime'))
    is_approved     = models.BooleanField(default=False, verbose_name=_('FAQ Approuvé ou pas'))
    approved_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=('FAQAdminAppouved'), null=True)
    slug            = AutoSlugField(populate_from=['title'])
    file            = models.FileField(upload_to="faq/document/", verbose_name=_('Fichier'), storage=UUIDFileStorageFILE(), null=True)
    is_active       = models.BooleanField(default=True, verbose_name=_('FAQ actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        

####################################################################
################################## BLOG #############################
####################################################################

class BlogImage(models.Model):
    cover           = models.FileField(upload_to="blog/image/", verbose_name=_('image de du blog'), storage=UUIDFileStorageCOVER())
    is_active       = models.BooleanField(default=True, verbose_name=_('Blog actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

class BlogVideo(models.Model):
    video           = models.FileField(upload_to="blog/video/", verbose_name=_('Video de du blog'), storage=UUIDFileStorageVIDEO())
    is_active       = models.BooleanField(default=True, verbose_name=_('Blog actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

class Blog(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title           = models.TextField(verbose_name=_('Titre du Blog'))
    label           = models.TextField(verbose_name=_('Label du Blog'), null=True)
    description     = RichTextField(verbose_name=_('Description du blog'), null=True)
    is_approuved    = models.BooleanField(default=False, verbose_name=_('Blog Approuvé ou pas'))
    approuved_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=('BlogAdminAppouved'), null=True)
    slug            = AutoSlugField(populate_from=['title'])
    cover           = models.FileField(upload_to="blog/cover/", verbose_name=_('Couverture de du blog'), storage=UUIDFileStorageCOVER())
    images          = models.ManyToManyField(BlogImage, verbose_name=_('Image du Blog'))
    videos          = models.ManyToManyField(BlogVideo, verbose_name=_('Video du Blog'))
    is_active       = models.BooleanField(default=True, verbose_name=_('Blog actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{}".format(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class BlogComment(models.Model):
    person          = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('Information sur celui qui a commenté'))
    blog            = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name=_('Blog Concerné'))
    comment         = RichTextField(verbose_name=_('Commentaire du blog'))
    is_block        = models.BooleanField(default=False, verbose_name=_('Commentaire bloquer ou pas'))
    is_active       = models.BooleanField(default=True, verbose_name=_('FAQ actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{} a effectué le commentaire suivant : {}".format(self.person.user.get_full_name(), self.comment)

class BlogLike(models.Model):
    person          = models.ForeignKey(Persons, on_delete=models.CASCADE, verbose_name=_('Information sur celui qui a commenté'))
    blog            = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name=_('Blog Concerné'))
    is_like         = models.BooleanField(default=True, verbose_name=_('Like ou pas'))
    is_active       = models.BooleanField(default=True, verbose_name=_('Blog Like actif ou pas'))
    created_date    = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date    = models.DateTimeField(default=now, editable=True, verbose_name="Date de mise a jour")

    def __str__(self):
        return "{} a effectué le commentaire suivant : {}".format(self.person.user.get_full_name(), self.is_like)
