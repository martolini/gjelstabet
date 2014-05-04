# -*- encoding: utf-8 -*-
from django.http import *
from forms import UploadForm
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import unittest
from forms import *
from models import *
from django.db.models import Count, Min, Sum, Max, Avg, Q
from django.db import connection
import random, logging, datetime, json, functools
from datetime import datetime, timedelta
from functools import wraps
from django.core.context_processors import csrf
import urllib2
import urllib
import httplib
from xml.dom import minidom
from datetime import datetime as dt
import time
from django.core.urlresolvers import resolve
from decimal import Decimal
import os
PERPAGE=50

def to_decimal(float_price):
    return Decimal('%.2f' % float_price)

def now_str():
    """Return hh:mm:ss string representation of the current time."""
    t = dt.now().time()
    return t.strftime("%H:%M:%S")

def GetRecaptcha(request):
    value = random.randrange(10000, 99999, 1)
    request.session['ReCaptcha'] = value
    return "https://chart.googleapis.com/chart?chst=d_text_outline&chld=FFCC33|16|h|FF0000|b|%s"%value

def checkuserlogin_dispatch(f):
    def wrap(request, *args, **kwargs):
        if 'IsLogin' in request.session and request.session['IsLogin'] and request.session['Customer'].email !="":
            customer_list = customers.objects.filter(email = request.session['Customer'].email,
                                                     pass_field = request.session['Customer'].pass_field,custenabled=1)
            if customer_list:
                request.session['IsLogin'] = True
                request.session['Customer'] = customer_list[0]
                success = True
            else:
                return HttpResponseRedirect('/logout')
            logging.info('Fetch Started::  %s', customer_list[0])
        else:
            return HttpResponseRedirect('/logout')
        return f(request, *args, **kwargs)
    return wrap

class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

@csrf_exempt
def render_template(request, template, data=None):
    errs =""
    if request.method == 'GET' and 'err' in request.GET:
        data.update({'errs':request.GET['err']})
    
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

class HomePageClass(TemplateView):
    def get(self, request, *args, **kwargs):
                   
        content = {'page_title': "Welcome"}
        return render_template(request, "index.html", content)
   
class RegistrationViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'title': "User Registration",
                   'regform':RegistrationForm,}
        return render_template(request, "registration1.html", content)

class QuickListClass(TemplateView):
    def get(self, request, *args, **kwargs):
        cat = request.GET['cat'] if 'cat' in request.GET else 15
        content = {'title': "Quick List",'cat': cat,}
         
        return render_template(request, "quick_list.htm", content)

class ViewCategoryClass(TemplateView):
    def get(self, request, *args, **kwargs):
        cat = request.GET['id'] if 'id' in request.GET else 3
        category = Category.objects.get(id=cat)
        categoryid, category_name, parent_id = BreadParentCategory(cat)
        content = {'title': "Quick List",'catparent':category_name,
                   'cat': category,}
         
        return render_template(request, "category.htm", content)

class MyaccountViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        
        logging.info('User Started::  %s', request.user.id)
        countries=ShippingCountries.objects.all().filter(enabled=1)
        userprofiles= UserProfile.objects.get(user_id = request.user.id)
        content = {'page_title': "Edit Profile",'regform':RegistrationForm,
                   'countries':countries,'userprofiles':userprofiles}
        return render_template(request, "myaccount.html", content)
    def post(self, request, *args, **kwargs):
        pass

class ChangePwdViewClass(LoginRequiredMixin, TemplateView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Profile - Password Change"}

        error_message = ""
        if "ErrorMessage" in request.session:
          
          error_message = request.session["ErrorMessage"]
          del request.session["ErrorMessage"]
        customer = request.session['Customer']
        prefill_data = {'username':request.user.email}
        form = ChangePwdForm(prefill_data)
        content = {'page_title': "Summary",'customer':request.session['Customer'],'form':form}
        
        return render_template(request, "ChangePWD.html", content)

class ResetPwdViewClass(TemplateView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if 'id' in request.GET and  request.GET['id']!="":
            usercnt = UserProfile.objects.filter(reset_code = request.GET['id'], reset_status='1').count()
            logging.info('User reset::  %s', usercnt)
            if usercnt>=1:
                content = {'page_title': "Reset Password",'form':ChangePwdForm,'id':request.GET['id']}
                return render_template(request, "resetPWD.html", content)
            else:
                return HttpResponse('/login?err=Successfully Updated the Record')
        else:
            return HttpResponseRedirect('/login?err=Successfully Updated the Record')
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        error_msg=""
        success=""
        logging.info('Reset Code::  %s', request.POST['id'])
        usercnt = UserProfile.objects.filter(reset_code = request.POST['id'], reset_status='1' ).count()
        if usercnt:
            
            userdetails = UserProfile.objects.get(reset_code = request.POST['id'])
            userdetails.reset_code=''
            userdetails.reset_status=2
            userdetails.save()
            u = User.objects.get(id=userdetails.user_id)
            u.set_password(request.POST['cnew_password'])
            u.save()
            success = True
            error_msg = False
        else:
            (success, error_msg) = (False, 1)
        content = {'page_title': "Forgot Password",
                   'error_msg':error_msg,
                   'success':success}
        return render_template(request, "resetPWD.html", content)    
        

import random, string
class ForgetPasswordClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "View Media List",}
        return render_template(request, "forgetpwd.html", content)
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        error_msg=""
        success=""
        logging.info('User Started::  %s', request.POST['email'])
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            usercnt = User.objects.filter(email = request.POST['email']).count()
            if usercnt:
                ucode = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(64)])
                logging.info('Reset Code::  %s', ucode)
                userdetails = User.objects.get(email = request.POST['email'])
                userprofile=UserProfile.objects.get(user_id=userdetails.id)
                userprofile.reset_code=str(ucode)
                userprofile.reset_status=1
                userprofile.save()
                mail.send_mail(sender=" Support <accounts@example.com>",
                               to=userdetails.first_name+" "+userdetails.last_name+"<"+userdetails.email+">",
                               subject="Password Reset",
                               body="""
                               You're receiving this e-mail because you requested a password reset for your user account at our site.
                                Please go to the following page and choose a new password:
                                <a href='http://example.com/rset?id="""+ucode+"""'> click here to reset password</a>
                                Thanks for using our site!
                            
                                Your  Team
                               """)
                success = True
                error_msg = False
            else:
               (success, error_msg) = (False, 1)
        content = {'page_title': "Forgot Password",
                   'error_msg':error_msg,
                   'success':success}
        return render_template(request, "forgetpwd.html", content)
