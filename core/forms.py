from django import forms

from core.models import *
from django.forms import ModelChoiceField, ModelForm

#from allauth.account.forms import SignupForm
from fstore.settings import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from cities_light.models import City, Country

# country module import
from django_countries.fields import CountryField

class SignupUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

class LoginUsernameForm(forms.Form):
    username = forms.CharField(max_length=250, label=_("Votre nom d'utilisateur"))
    password = forms.CharField(max_length=250, label=_("Votre mot de passe"))

class LoginEmailForm(forms.Form):
    email = forms.CharField(max_length=250, label=_("Votre nom d'utilisateur ou Adresse Email"))
    password = forms.CharField(max_length=250, label=_("Votre mot de passe"))

class SignupPersonForm(ModelForm):
    class Meta:
        model = Persons
        fields = [
            'phone',
            'country',
            'city',
            'sexe',
            'user'
        ]

class UpdatePersonForm(ModelForm):
    class Meta:
        model = Persons
        fields = [
            'phone',
            'country',
            'city',
            'sexe',
            'address',
            'codepostal',
            'birthday_date',
            'googlemap'
        ]

#Manage Menu
class CreateMenuForm(ModelForm):
    class Meta:
        model = Menus
        fields = [
            'title',
            'code',
            'link',
            'create_by'
        ]
class UpdateMenuForm(ModelForm):
    class Meta:
        model = Menus
        fields = [
            'title',
            'code',
            'link',
        ]


#Manage Parent Menu
class CreateParentMenuForm(ModelForm):
    class Meta:
        model = ParentMenus
        fields = [
            'title',
            'label',
            'icon',
            'create_by'
        ]
class UpdateParentMenuForm(ModelForm):
    class Meta:
        model = ParentMenus
        fields = [
            'title',
            'label',
            'icon',
        ]


#Manage Menu Rule
class CreateMenuRuleForm(ModelForm):
    class Meta:
        model = MenuRules
        fields = [
            'label',
            'menu',
            'can_read',
            'can_create',
            'can_update',
            'can_delete',
            'create_by'
        ]
class UpdateMenuRuleForm(ModelForm):
    class Meta:
        model = MenuRules
        fields = [
            'label',
            'menu',
            'can_read',
            'can_create',
            'can_update',
            'can_delete',
        ]

#Manage Profil
class CreateProfilForm(ModelForm):
    class Meta:
        model = Profil
        fields = [
            'title',
            'description',
            'create_by'
        ]
class UpdateProfilForm(ModelForm):
    class Meta:
        model = Profil
        fields = [
            'title',
            'description'
        ]

#Manage User Profil
class CreateUserProfilForm(ModelForm):
    class Meta:
        model = UserProfil
        fields = [
            'person',
            'profil',
            'description',
            'create_by'
        ]
class UpdateUserProfilForm(ModelForm):
    class Meta:
        model = UserProfil
        fields = [
            'person',
            'profil',
            'description',
        ]





