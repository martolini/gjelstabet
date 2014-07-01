from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

#Deprecated in 1.6 Django
#from django.conf.urls.defaults import *

from django.conf.urls import patterns, url, include
from django.contrib import admin
from views import *
from gjelstabet.auth_views import *
#from admin.admin_actions import *
#from admin.views import *
from django.contrib.auth.views import password_reset

handler500 = 'djangotoolbox.errorviews.server_error'
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', HomePageClass.as_view(),name='Home'),
    url(r'^accounts/login/$',LoginPageClass.as_view(),name='login'),
    url(r'^login', LoginPageClass.as_view(),name='LoginPage'),
    url(r'^logout', LogoutClass.as_view(),name='Logout'),
    #url(r'^custlogin', 'auth_views.CustomerLoginClass', name='custlogin'),
    url(r'^custlogin', CustomerLoginClass.as_view(), name='custlogin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^myaccount', MyaccountViewClass.as_view(), name='myaccount'),
    url(r'^signup', RegistrationViewClass.as_view(), name='registration'),
    url(r'^registeruser', RegistrationActionClass.as_view(), name='registeruser'),
    #url(r'^forgetpassword', ForgetPasswordClass.as_view(), name='forgetpassword'),
    url(r'^reset', ForgetPasswordClass.as_view(), name='forgetpassword'),
    #url(r'^sendpassword', ForgetPasswordActionClass.as_view(), name='sendpassword'),
    url(r'^features', FeaturesPageClass.as_view(), name='features'),
    url(r'^contactus', ContactPageClass.as_view(), name='contactus'),
    url(r'^prices', PricesViewClass.as_view(), name='prices'),
	url(r'^oddtypes', OddtypesViewClass.as_view(), name='oddstypes'),
    url(r'^booktypes', BookmakertypesViewClass.as_view(), name='booktypes'),
    url(r'^sporttypes', SporttypesViewClass.as_view(), name='sporttypes'),
    url(r'^feeds', FeedsViewClass.as_view(), name='getfeeds'),
    url(r'^sportfeeds', SportFeedsViewClass.as_view(), name='sportfeeds'),
    url(r'^bookfeeds', BookmakerFeedsViewClass.as_view(), name='bookfeeds'),
)+ static(settings.local.MEDIA_URL, document_root=settings.local.MEDIA_ROOT)
