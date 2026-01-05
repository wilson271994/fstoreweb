from django.urls import re_path
from . import views

app_name = 'api'

urlpatterns = [
    re_path(r'^auth$', views.LoginApiView.as_view()),
    re_path(r'^signup$', views.SinupApiView.as_view()),
    re_path(r'^activate-account$', views.ActivateAccount.as_view()),    
    re_path(r'^logout$', views.LogOut.as_view()), 
    re_path(r'^site-info$', views.SiteInfoApiView.as_view()),

    #User management Data
    re_path(r'^user-data$', views.UserDataApiView.as_view()),

    #Product Management
    re_path(r'^product-list$', views.allProduct.as_view()),
    re_path(r'^search-product$', views.searchProduct.as_view()),
    re_path(r'^products-category$', views.productsCategory.as_view()),
    re_path(r'^comment-product$', views.commentProduct.as_view()),

    #Basket management
    re_path(r'^toggle-basket$', views.toggleBasket.as_view()), 
    re_path(r'^toggle-qteproduct-basket$', views.toggleQteProdBasket.as_view()), 
    re_path(r'^remove-item-basket$', views.removeProdBasket.as_view()), 
    re_path(r'^wipe-basket$', views.wipeBasket.as_view()), 

    #command 
    re_path(r'^create-command$', views.createCommand.as_view()), 
    re_path(r'^delete-command$', views.deleteCommand.as_view()), 
    
    #payment 
    re_path(r'^auth-payment$', views.requestAuthPayment.as_view()), 
    re_path(r'^request-payment-fee$', views.requestPaymentFee.as_view()), 
    re_path(r'^request-payitemid$', views.requestPayItemID.as_view()), 
    re_path(r'^request-quoteid$', views.requestQuoteID.as_view()), 
    re_path(r'^post-payment-collection$', views.postCollection.as_view()), 
    re_path(r'^request-payment-status$', views.requestPaymentStatus.as_view()), 

]   