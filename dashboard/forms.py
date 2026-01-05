from django.forms import ModelForm, ModelChoiceField, DateInput,ChoiceField,Select
from ckeditor.widgets import CKEditorWidget

from .models import *

#Grant Child Cat
class CreateGrantChildCategoryForm(ModelForm):
    class Meta:
        model = categoriesGrantChild
        fields = [
            'name',
            'creator',
        ]
#Child Cat    
class CreateChildCategoryForm(ModelForm):
    class Meta:
        model = categoriesChild
        fields = [
                    'name',
                    'creator',
                ]

class UpdateChildCategoryForm(ModelForm):
    class Meta:
        model = categoriesChild
        fields = [
                    'name'
                ]
        
#Parent Cat
class CreateParentCategoryForm(ModelForm):
    class Meta:
        model = parentCategory
        fields = [
                    'name',
                    'creator',
                    'cover'
                ]

class UpdateParentCategoryForm(ModelForm):
    class Meta:
        model = parentCategory
        fields = [
                    'name',
                    'cover'
                ]
        

##################brand Forms
class CreatebrandForm(ModelForm):
    class Meta:
        model = Brands
        fields = [
                'name',
                'creator',
                'logo'
            ]
class UpdatebrandForm(ModelForm):
    class Meta:
        model = Brands
        fields = [
                    'name',
                ]

##################Provider Forms
class CreateProviderForm(ModelForm):
    class Meta:
        model = Providers
        fields = [
                'name',
                'creator',
                'logo'
            ]
class UpdateProviderForm(ModelForm):
    class Meta:
        model = Providers
        fields = [
                    'name',
                ]

##################Color Forms
class CreateColorForm(ModelForm):
    class Meta:
        model = DefaultsColors
        fields = [
                    'creator',
                    'name',
                    'code',
                ]
class UpdateColorForm(ModelForm):
    class Meta:
        model = DefaultsColors
        fields = [
                    'name',
                    'code',
                ]

##################Size Forms
class CreateSizeForm(ModelForm):
    class Meta:
        model = DefaultSize
        fields = [
                    'creator',
                    'name'
                ]
class UpdateSizeForm(ModelForm):
    class Meta:
        model = DefaultSize
        fields = [
                    'name'
                ]
        
##################Material Forms
class CreateMaterialForm(ModelForm):
    class Meta:
        model = DefaultsMaterial
        fields = [
                    'creator',
                    'name',
                    'description'
                ]
class UpdateMaterialForm(ModelForm):
    class Meta:
        model = DefaultsMaterial
        fields = [
                    'name',
                    'description'
                ]

#Product Form
class CreateProductForm(ModelForm):
    category = ModelChoiceField(queryset=categoriesGrantChild.objects.all())
    class Meta:
        model = Products
        fields = [
            'creator',
            'provider',
            'name',
            'description',
            'quantity',
            'price',
            'discount',
            'category'
        ]
        widgets = {
            'description':CKEditorWidget(),
        }
        
class UpdateProductForm(ModelForm):
    class Meta:
        model = Products
        fields = [
            'name',
            'description',
            'quantity',
            'price',
            'discount',
        ]
        widgets = {
            'description':CKEditorWidget(),
        }
        
#Manage Caracteristique Form
class CreateCaractProductForm(ModelForm):
    class Meta:
        model = ProductCaracteristque
        fields = [
            'creator',
            'product'
        ]

#Product Flash
class AddFlashProductForm(ModelForm):
    class Meta:
        model = PromotionsProducts
        fields = [
            'creator',
            'product',
            'date_start',
            'date_end',
            'promo_price'
        ]
    
#MANAGE CURRENCY 
class CreateCurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = [
            'creator',
            'currency_origin_country',
            'currency_origin_code',
            'currency_destination_country',
            'currency_destination_code',
            'exchange_rate'
        ]
        
class UpdateCurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = [
            'currency_origin_country',
            'currency_origin_code',
            'currency_destination_country',
            'currency_destination_code',
            'exchange_rate'
        ]
        
########################## FORM FOR BANNER
class createBannerForm(ModelForm):
    class Meta:
        model = BannerPubs
        fields = [
            'creator',
            'title',
            'cover',
            'link',
            'is_external',
        ]

class updateBannerForm(ModelForm):
    class Meta:
        model = BannerPubs
        fields = [
            'title',
            'cover',
            'link',
            'is_external',
        ]


###############################FORM FOR SPONSORING
class createSponsoringForm(ModelForm):
    class Meta:
        model = SponsoringProducts
        fields = [
            'creator',
            'provider',
            'product',
            'booking',
            'start_date',
            'end_date',
        ]

class updateSponsoringForm(ModelForm):
    class Meta:
        model = SponsoringProducts
        fields = [
            'provider',
            'product',
            'booking',
            'start_date',
            'end_date',
        ]

###############################FORM FOR SPONSORING BOOKING
class createSponsoringBookingForm(ModelForm):
    class Meta:
        model = SponsoringBooking
        fields = [
            'creator',
            'name',
            'code_zone',
            'periode',
            'sponsoring_price',
        ]

class updateSponsoringBookingForm(ModelForm):
    class Meta:
        model = SponsoringBooking
        fields = [
            'name',
            'code_zone',
            'periode',
            'sponsoring_price',
        ]
        
###############################FORM FOR SPONSORING ZONE
class createSponsoringZoneForm(ModelForm):
    class Meta:
        model = SponsoringManageBlock
        fields = [
            'creator',
            'name',
            'code'
        ]

class updateSponsoringZoneForm(ModelForm):
    class Meta:
        model = SponsoringManageBlock
        fields = [
            'name',
            'code'
        ]

# Manage Support Service
class CreateSupportServiceForm(ModelForm):
    class Meta:
        model = customerSupportService
        fields = [
            'creator',
            'title',
            'description',
            'is_payment_required',
            'price'
        ]


class UpdateSupportServiceForm(ModelForm):
    class Meta:
        model = customerSupportService
        fields = [
            'title',
            'description',
            'is_payment_required',
            'price'
        ]

# Manage Support Ticket
class CreateSupportTicketForm(ModelForm):
    class Meta:
        model = customerSupportTicket
        fields = [
            'owner',
            'service',
            'command',
            'resume',
            'description'
        ]

class UpdateSupportTicketForm(ModelForm):
    class Meta:
        model = customerSupportTicket
        fields = [
            'service',
            'command',
            'resume',
            'description'
        ]
        
#################################################################
###################### FORM MANAGE FAQ ##########################
##################################################################
class CreateFaqForm(ModelForm):
    class Meta:
        model = FAQ
        fields = [
            'creator',
            'category',
            'title',
            'label',
            'subject',
            'content',
        ]

class UpdateFaqForm(ModelForm):
    class Meta:
        model = FAQ
        fields = [
            'category',
            'title',
            'label',
            'subject',
            'content',
        ]


#Manage Categorie FAQ
class CreateFaqCategoryForm(ModelForm):
    class Meta:
        model = FAQCategory
        fields = [
            'creator',
            'title',
            'description',
        ]

class UpdateFaqCategoryForm(ModelForm):
    class Meta:
        model = FAQCategory
        fields = [
            'title',
            'description',
        ]


##################################################################
###################### FORM MANAGE BLOG ##########################
##################################################################
class CreateBlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = [
            'author',
            'title',
            'label',
            'description',
            'cover',
        ]

class UpdateBlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title',
            'label',
            'description',
            'cover',
        ]


##################### Blog Comment
class CreateBlogCommentForm(ModelForm):
    class Meta:
        model = BlogComment
        fields = [
            'person',
            'blog',
            'comment',
        ]        


#####################Create Delivered Zone
class CreateDeliveredZoneForm(ModelForm):
    class Meta:
        model = CompanyDeliveryZone
        fields = [
            'title',
            'description',
            'price',
            'googlemap'
        ]      

#####################Update Delivered Zone
class UpdateDeliveredZoneForm(ModelForm):
    class Meta:
        model = CompanyDeliveryZone
        fields = [
            'title',
            'description',
            'price',
            'googlemap'
        ]     




