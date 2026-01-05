from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Persons),
admin.site.register(AccountActivationCode)


