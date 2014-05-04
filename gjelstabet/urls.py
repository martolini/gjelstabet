from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

#Deprecated in 1.6 Django
#from django.conf.urls.defaults import *

from django.conf.urls import patterns, url, include
from django.contrib import admin
from views import *
from auth_views import *
#from admin.admin_actions import *
#from admin.views import *
from django.contrib.auth.views import password_reset

handler500 = 'djangotoolbox.errorviews.server_error'
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', HomePageClass.as_view(),name='Home'),
    url(r'^accounts/login/$','auth_views.loginpage',name='login'),
    url(r'^login', LoginPageClass.as_view(),name='LoginPage'),
    (r'^logout/$', 'auth_views.logout_view'),
    url(r'^custlogin', 'auth_views.CustomerLoginClass', name='custlogin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^myaccount', MyaccountViewClass.as_view(), name='myaccount'),
    #url(r'^registration', RegistrationViewClass.as_view(), name='registration'),
    #url(r'^registeruser', RegistrationActionClass.as_view(), name='registeruser'),
    #url(r'^forgetpassword', ForgetPasswordClass.as_view(), name='forgetpassword'),
    url(r'^reset', ForgetPasswordClass.as_view(), name='forgetpassword'),
    #url(r'^sendpassword', ForgetPasswordActionClass.as_view(), name='sendpassword'),
)+ static(settings.local.MEDIA_URL, document_root=settings.local.MEDIA_ROOT)
