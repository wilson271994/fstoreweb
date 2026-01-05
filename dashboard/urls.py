from django.urls import re_path
from .views import *
from core.views import *

app_name = "dashboard"

urlpatterns = [
    re_path(r'^$', HomeAnalytics, name='home'),
    re_path(r'^user-home$', UsersHomeMethod, name='users-page'),
    re_path(r'^user-creation$', CreateUser, name='user-creation'),
    re_path(r'^user-update$', UpdateUser, name='user-update'),
    re_path(r'^user-status$', userStatusMethod, name='user-status'),
    re_path(r'^user-delete$', userDeleteMethod, name='user-delete'),
    re_path(r'^user-password-reset$', userChangePassword, name='user-password-reset'),

    #Company Info
    re_path(r'^index-info-company$', indexAboutCompany, name='index-info-company'),
    re_path(r'^update-info-company$', updateInfoCompanyMethod, name='update-info-company'),
    
    re_path(r'^create-contact-company$', contactCompanyMethod, name='create-contact-company'),
    re_path(r'^delete-phone-company$', deleteContactComapnyMethod, name='delete-phone-company'),

    re_path(r'^create-email-company$', emailCompanyMethod, name='create-email-company'),
    re_path(r'^delete-email-company$', deleteEmailComapnyMethod, name='delete-email-company'),

    re_path(r'^create-social-company$', socialCompanyMethod, name='create-social-company'),
    re_path(r'^delete-social-company$', deleteSocialComapnyMethod, name='delete-social-company'),

    re_path(r'^create-value-company$', valueCompanyMethod, name='create-value-company'),
    re_path(r'^delete-value-company$', deleteValueComapnyMethod, name='delete-value-company'),

    #manage Company Address 
    re_path(r'^create-address-company$', createAddressCompanyMethod, name='create-address-company'),
    re_path(r'^update-address-company$', updateAddressCompanyMethod, name='update-address-company'),
    re_path(r'^default-address-company$', defaultAddressCompanyMethod, name='default-address-company'),
    re_path(r'^delete-address-company$', deleteAddressCompanyMethod, name='delete-address-company'),

    #Partner Company 
    re_path(r'^index-partner-company$', indexCompanyPartnerMethod, name='index-partner-company'),
    re_path(r'^create-partner-company$', createCompanyPartnerMethod, name='create-partner-company'),
    re_path(r'^update-partner-company$', updateCompanyPartnerMethod, name='update-partner-company'),
    re_path(r'^status-partner-company$', statusCompanyPartnerMethod, name='status-partner-company'),
    re_path(r'^validate-partner-company$', validateCompanyPartnerMethod, name='validate-partner-company'),
    re_path(r'^delete-partner-company$', deleteCompanyPartnerMethod, name='delete-partner-company'),
    
    ####Brand Route
    re_path(r'^brand$', brandHomeMethod, name='brand'),
    re_path(r'^create-brand$', createBrandMethod, name='create-brand'),
    re_path(r'^update-brand$', brandUpdateMethod, name='update-brand'),
    re_path(r'^validate-brand$', brandValidateMethod, name='validate-brand'),
    re_path(r'^status-brand$', brandStatusMethod, name='status-brand'),
    re_path(r'^delete-brand$', brandDeleteMethod, name='delete-brand'),
    
    ####Grant Category Route
    re_path(r'^grantcategory$', categoryGrantChildHomeMethod, name='grantchildcategory'),
    re_path(r'^create-grantchild-category$', createGrantChildCategoryMethod, name='create-grantchild-category'),
    re_path(r'^update-grantchild-category$', grantChildCategoryUpdateMethod, name='update-grantchild-category'),
    re_path(r'^status-grantchild-category$', grantChildCategoryStatusMethod, name='status-grantchild-category'),
    re_path(r'^delete-grantchild-category$', grantChildCategoryDeleteMethod, name='delete-grantchild-category'),
    
    ####Child Category Route
    re_path(r'^childcategory$', categoryChildHomeMethod, name='childcategory'),
    re_path(r'^create-child-category$', createChildCategoryMethod, name='create-child-category'),
    re_path(r'^update-child-category$', childCategoryUpdateMethod, name='update-child-category'),
    re_path(r'^status-child-category$', childCategoryStatusMethod, name='status-child-category'),
    re_path(r'^delete-child-category$', childCategoryDeleteMethod, name='delete-child-category'),
    
    ####Parent Category Route
    re_path(r'^parentcategory$', categoryParentHomeMethod, name='parentcategory'),
    re_path(r'^create-parent-category$', createParentCategoryMethod, name='create-parent-category'),
    re_path(r'^update-parent-category$', parentCategoryUpdateMethod, name='update-parent-category'),
    re_path(r'^status-parent-category$', parentCategoryStatusMethod, name='status-parent-category'),
    re_path(r'^delete-parent-category$', parentCategoryDeleteMethod, name='delete-parent-category'),
    
    ####Attributes Route
    re_path(r'^home-attribute$', attributeHomeMethod, name='home-attribute'),
    
    ##############Colors
    re_path(r'^home-color$', colorHomeMethod, name='home-color'),
    re_path(r'^create-color$', createColorMethod, name='create-color'),
    re_path(r'^update-color$', colorUpdateMethod, name='update-color'),
    re_path(r'^status-color$', colorStatusMethod, name='status-color'),
    re_path(r'^delete-color$', colorDeleteMethod, name='delete-color'),
    
    ##############Sizes
    re_path(r'^home-size$', sizeHomeMethod, name='home-size'),
    re_path(r'^create-size$', createSizeMethod, name='create-size'),
    re_path(r'^update-size$', sizeUpdateMethod, name='update-size'),
    re_path(r'^status-size$', sizeStatusMethod, name='status-size'),
    re_path(r'^delete-size$', sizeDeleteMethod, name='delete-size'),
    
    ##############Materials
    re_path(r'^home-material$', materialHomeMethod, name='home-material'),
    re_path(r'^create-material$', createMaterialMethod, name='create-material'),
    re_path(r'^update-material$', materialUpdateMethod, name='update-material'),
    re_path(r'^status-material$', materialStatusMethod, name='status-material'),
    re_path(r'^delete-material$', materialDeleteMethod, name='delete-material'),
    
    ####Provider Route
    re_path(r'^provider$', providerHomeMethod, name='provider'),
    re_path(r'^create-provider$', createProviderMethod, name='create-provider'),
    re_path(r'^update-provider$', providerUpdateMethod, name='update-provider'),
    re_path(r'^validate-provider$', providerValidateMethod, name='validate-provider'),
    re_path(r'^status-provider$', providerStatusMethod, name='status-provider'),
    re_path(r'^delete-provider$', providerDeleteMethod, name='delete-provider'),
    
    ##############Products
    re_path(r'^home-product$', productHomeMethod, name='home-product'),
    re_path(r'^create-product$', createProductMethod, name='create-product'),
    re_path(r'^update-product$', productUpdateMethod, name='update-product'),
    re_path(r'^status-product$', productStatusMethod, name='status-product'),
    re_path(r'^validate-product$', validateProductMethod, name='validate-product'),
    re_path(r'^delete-product$', productDeleteMethod, name='delete-product'),
    re_path(r'^get-child-category$', childCategoryMethod, name='get-child-category'),
    re_path(r'^get-grant-category$', grantCategoryMethod, name='get-grant-category'),
    re_path(r'^create-presentation$', createPresentationMethod, name='create-presentation'),
    re_path(r'^update-presentation$', updatePresentationMethod, name='update-presentation'),
    re_path(r'^create-attribut$', createAttributMethod, name='create-attribut'),
    re_path(r'^update-attribut$', updateAttributMethod, name='update-attribut'),
    re_path(r'^add-flash-product$', addFlashProductMethod, name='add-flash-product'),
    re_path(r'^delete-product-flash$', deleteFlashProductMethod, name='delete-product-flash'),
    
    ####Distributor route
    re_path(r'^distribution-zone$', deliveredZoneHomeMethod, name='distribution-zone'),
    re_path(r'^create-zone$', deliveredCreate, name='create-zone'),
    re_path(r'^update-zone$', deliveredUpdate, name='update-zone'),
    re_path(r'^status-zone$', deliveredStatus, name='status-zone'),
    re_path(r'^validate-zone$', deliveredValidate, name='validate-zone'),
    re_path(r'^delete-zone$', deliveredDelete, name='delete-zone'),
    
    ####Trafic route
    re_path(r'^trafic$', traficHomeMethod, name='trafic'),
    re_path(r'^trafic-start$', traficDeliveredStart, name='trafic-start'),
    re_path(r'^trafic-end$', traficDeliveredEnd, name='trafic-end'),
    
    ####Billing route
    re_path(r'^invoices$', invoiceHomeMethod, name='invoices'),
    re_path(r'^template-invoice/(?P<command_id>[0-9]+)$', invoiceTemplateMethod, name='template-invoice'),

    ####Transaction And Paymentroute
    re_path(r'^payment-home$', homePaymentMethod, name='payment-home'),
    re_path(r'^transaction-home$', homeTransactionMethod, name='transaction-home'),
    
    ####Finance Provider route
    re_path(r'^finance-provider$', homeFinanceProviderMethod, name='finance-provider'),
    re_path(r'^finance-provider-status$', statusFinanceProviderMethod, name='finance-provider-status'),
    
    ####Finance Product route
    re_path(r'^finance-product$', homeFinanceProductMethod, name='finance-product'),
    re_path(r'^finance-product-status$', productFinanceStatus, name='finance-product-status'),
    
    ####Finance Distributor route
    re_path(r'^finance-distributor$', homeFinanceDistributorMethod, name='finance-distributor'),
    re_path(r'^finance-distributor-status$', distributorFinanceStatus, name='finance-distributor-status'),
    
    ####Customer Finance route
    re_path(r'^customer-finance$', homeFinanceCustomerMethod, name='customer-finance'),
    re_path(r'^customer-finance-status$', customerFinanceStatusMethod, name='customer-finance-status'),
    
    ####Customer Infos route
    re_path(r'^customer-list$', customerHomeMethod, name='customer-list'),
    re_path(r'^customer-status$', customerStatusMethod, name='customer-status'),
    
    ####ChatBoot route
    re_path(r'^chatboot-home$', chatBootHomeMethod, name='chatboot-home'), 

    
    ####################URL FOR DEVISE ###############
    re_path(r'^currency-home$',currencyHomeMethod, name='currency-home'),
    re_path(r'^currency-creation$',createCurrencyMethod, name='currency-creation'),
    re_path(r'^currency-update$',updateCurrencyMethod, name='currency-update'),
    re_path(r'^currency-status$',currencyStatusMethod, name='currency-status'),
    re_path(r'^currency-active$',currencyActiveMethod, name='currency-active'),
    re_path(r'^currency-delete$',currencyDeleteMethod, name='currency-delete'),
    
    ##########################ADVERTIZING ROUTE###########
    re_path(r'^advertizing-home$',advertizingHomeMethod, name='advertizing-home'),
    
    ####### Banner #######################
    re_path(r'^banner-home$',bannerHomeMethod, name='banner-home'),
    re_path(r'^create-banner$',createBannerMethod, name='create-banner'),
    re_path(r'^update-banner$',bannerUpdateMethod, name='update-banner'),
    re_path(r'^status-banner$',bannerStatusMethod, name='status-banner'),
    re_path(r'^delete-banner$',bannerDeleteMethod, name='delete-banner'),
    
    #####################Sponsoring Route
    re_path(r'^sponsoring-home$',sponsoringHomeMethod, name='sponsoring-home'),
    re_path(r'^create-sponsoring$',createSponsoringMethod, name='create-sponsoring'),
    re_path(r'^update-sponsoring$',sponsoringUpdateMethod, name='update-sponsoring'),
    re_path(r'^status-sponsoring$',sponsoringStatusMethod, name='status-sponsoring'),
    re_path(r'^delete-sponsoring$',sponsoringDeleteMethod, name='delete-sponsoring'),
    re_path(r'^sponsoring-product-seller$',sponsoringGetSellerProductMethod, name='sponsoring-product-seller'),
    
    #####################Sponsoring Route
    re_path(r'^sponsoringbooking-home$',sponsoringBookingHomeMethod, name='sponsoringbooking-home'),
    re_path(r'^create-sponsoringbooking$',createSponsoringBookingMethod, name='create-sponsoringbooking'),
    re_path(r'^update-sponsoringbooking$',sponsoringBookingUpdateMethod, name='update-sponsoringbooking'),
    re_path(r'^status-sponsoringbooking$',sponsoringBookingStatusMethod, name='status-sponsoringbooking'),
    re_path(r'^delete-sponsoringbooking$',sponsoringBookingDeleteMethod, name='delete-sponsoringbooking'),
    
    #####################Sponsoring Zone Route
    re_path(r'^sponsoringzone-home$',sponsoringZoneHomeMethod, name='sponsoringzone-home'),
    re_path(r'^create-sponsoringzone$',createSponsoringZoneMethod, name='create-sponsoringzone'),
    re_path(r'^update-sponsoringzone$',sponsoringZoneUpdateMethod, name='update-sponsoringzone'),
    re_path(r'^status-sponsoringzone$',sponsoringZoneStatusMethod, name='status-sponsoringzone'),
    re_path(r'^delete-sponsoringzone$',sponsoringZoneDeleteMethod, name='delete-sponsoringzone'),
    
    ##########################Manage Blog Route
    re_path(r'^blog-home$',blogHomeMethod, name='blog-home'),
    re_path(r'^blog-creation$',createBlogMethod, name='blog-creation'),
    re_path(r'^blog-update$',updateBlogMethod, name='blog-update'),
    re_path(r'^blog-status$',statusBlogMethod, name='blog-status'),
    re_path(r'^blog-validate$',validateBlogMethod, name='blog-validate'),
    re_path(r'^blog-delete$',deleteBlogMethod, name='blog-delete'),
    
    #########################Manage Blog Comment
    re_path(r'^comment-blog$',blogCommentHomeMethod, name='comment-blog'),
    re_path(r'^blog-comment-validation$',blogCommentValidationMethod, name='blog-comment-validation'),
    re_path(r'^blog-comment-delete$',deleteBlogCommentMethod, name='blog-comment-delete'),

    ##########################Manage FAQ Route
    re_path(r'^faq-home$',faqHomeMethod, name='faq-home'),
    re_path(r'^faq-creation$',createFaqMethod, name='faq-creation'),
    re_path(r'^faq-update$',updateFaqMethod, name='faq-update'),
    re_path(r'^faq-status$',statusFaqMethod, name='faq-status'),
    re_path(r'^faq-validate$',validateFaqMethod, name='faq-validate'),
    re_path(r'^faq-delete$',deleteFaqMethod, name='faq-delete'),

    #category FAQ Route
    re_path(r'^faq-category-home$',faqCategoryHomeMethod, name='faq-category-home'),
    re_path(r'^faq-category-creation$',createFaqCategoryMethod, name='faq-category-creation'),
    re_path(r'^faq-category-update$',updateFaqCategoryMethod, name='faq-category-update'),
    re_path(r'^faq-category-status$',statusFaqCategoryMethod, name='faq-category-status'),
    re_path(r'^faq-category-delete$',deleteFaqCategoryMethod, name='faq-category-delete'),

    ##########################Manage Support Route
    re_path(r'^ticket-support-home$',supportHomeMethod, name='ticket-support-home'),
    re_path(r'^create-support-service$',createSupportServiceMethod, name='create-support-service'),
    re_path(r'^update-support-service$',updateSupportServiceMethod, name='update-support-service'),
    re_path(r'^validate-support-service$', validateSupportServiceMethod, name='validate-support-service'),
    re_path(r'^status-support-service$', statusSupportServiceMethod, name='status-support-service'),
    re_path(r'^delete-support-service$', deleteSupportServiceMethod, name='delete-support-service'),

    re_path(r'^service-support-home$',supportServiceHomeMethod, name='service-support-home'),
    re_path(r'^create-support-service$',createSupportServiceMethod, name='create-support-service'),
    re_path(r'^update-support-service$',updateSupportServiceMethod, name='update-support-service'),
    re_path(r'^validate-support-service$', validateSupportServiceMethod, name='validate-support-service'),
    re_path(r'^status-support-service$', statusSupportServiceMethod, name='status-support-service'),
    re_path(r'^delete-support-service$', deleteSupportServiceMethod, name='delete-support-service'),

    ##########################################Manage Ticket Route
    re_path(r'^message-ticket-support$', messageTicketSupportHome, name='message-ticket-support'),
    re_path(r'^create-message-ticket-support$', sendMessageTicketSupport, name='create-message-ticket-support'),
    re_path(r'^delete-message-ticket-support$', deleteMessageTicketSupport, name='delete-message-ticket-support'),

    ##########################################Manage Command Route
    re_path(r'^command-home$', homeCommandMethod, name='command-home'),
    re_path(r'^update-status-command-payment$', statusCommandPaymentMethod, name='update-status-command-payment'),
    re_path(r'^delete-command$', deleteCommandMethod, name='delete-command'),
    
    ##########################Manage Menu Route
    re_path(r'^home-menu$',homeMenuMethod, name='home-menu'),
    re_path(r'^create-menu$',createMenuMethod, name='create-menu'),
    re_path(r'^update-menu$',updateMenuMethod, name='update-menu'),
    re_path(r'^status-menu$',statusMenuMethod, name='status-menu'),
    re_path(r'^delete-status$',deleteMenuMethod, name='delete-menu'),

    ##########################Manage Parent Menu Route
    re_path(r'^home-parent-menu$',homeParentMenuMethod, name='home-parent-menu'), 
    re_path(r'^create-parent-menu$',createParentMenuMethod, name='create-parent-menu'),
    re_path(r'^update-parent-menu$',updateParentMenuMethod, name='update-parent-menu'),
    re_path(r'^status-parent-menu$',statusParentMenuMethod, name='status-parent-menu'),
    re_path(r'^delete-parent-menu$',deleteParentMenuMethod, name='delete-parent-menu'),

    ##########################Manage Menu Rule Route
    re_path(r'^home-menu-rule$',homeMenuRuleMethod, name='home-menu-rule'),
    re_path(r'^create-menu-rule$',createMenuRuleMethod, name='create-menu-rule'),
    re_path(r'^update-menu-rule$',updateMenuRuleMethod, name='update-menu-rule'),
    re_path(r'^status-menu-rule$',statusMenuRuleMethod, name='status-menu-rule'),
    re_path(r'^delete-menu-rule$',deleteMenuRuleMethod, name='delete-menu-rule'),
    
    ##########################Manage Profil
    re_path(r'^home-profil$',homeProfilMethod, name='home-profil'),
    re_path(r'^create-profil$',createProfilMethod, name='create-profil'),
    re_path(r'^update-profil$',updateProfilMethod, name='update-profil'),
    re_path(r'^status-profil$',statusProfilMethod, name='status-profil'),
    re_path(r'^delete-profil$',deleteProfilMethod, name='delete-profil'),

    ##########################Manage User Profil
    re_path(r'^home-user-profil$',homeUserProfilMethod, name='home-user-profil'),
    re_path(r'^create-user-profil$',createUserProfilMethod, name='create-user-profil'),
    re_path(r'^update-user-profil$',updateUserProfilMethod, name='update-user-profil'),
    re_path(r'^status-user-profil$',statusUserProfilMethod, name='status-user-profil'),
    re_path(r'^delete-user-profil$',deleteUserProfilMethod, name='delete-user-profil'),
    
]
