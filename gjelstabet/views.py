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
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from xml.dom import minidom

PERPAGE=50
USERID = 'gjelstabet'
PSWD = '8678y7u7'
FEED_URL = 'http://xml2.txodds.com/feed/odds/xml.php'
AVGFEED_URL = 'http://xml2.txodds.com/feed/average/xml.php'
BOOKMAKER_URL= 'http://xml2.txodds.com/feed/books.php?active=1'
ODDTYPES_URL= 'http://xml2.txodds.com/feed/odds_types.php'
SPORTS_URL = 'http://xml2.txodds.com/feed/sports.php'

def fetchurl(type):
    if type == "oddtypes":
        urlto = ODDTYPES_URL
    else:
        urlto = FEED_URL
    values = {"ident":USERID,"passwd":PSWD}
    resp = requests.get(urlto, params=values)
    return resp
    

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

class FeaturesPageClass(TemplateView):
    def get(self, request, *args, **kwargs):        
        content = {'page_title': "EDGEBET :: Features"}
        return render_template(request, "portfolio_item.html", content)

class ContactPageClass(TemplateView):
    def get(self, request, *args, **kwargs):        
        content = {'page_title': "EDGEBET :: Features"}
        return render_template(request, "page_contacts.html", content)


class RegistrationViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        if 'pid' in request.GET and request.GET['pid'] != "":
            prices = Pricing.objects.get(id=request.GET['pid'])
            content = {'title': "User Registration",'prices':prices,
                       'regform':RegistrationForm,'pid':request.GET['pid']}
            return render_template(request, "page_signup.html", content)
        else:
            return HttpResponseRedirect('/prices')

class RegistrationActionClass(TemplateView):
    def post(self, request, *args, **kwargs):
        pid = request.POST['pid']
        try:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                profileform = form.save(request)
                content = {'page_title': "Success",}
                return render_template(request, "success.html", content)
            else:
                form_errors = form.errors
                content = {'page_title': "User Registration",
                           'regform':RegistrationForm, 'pid':pid}
                return render_template(request, "success.html", content)
        except Exception, e:
            logging.info('LoginfoMessage now:: %s',e)
            return HttpResponse(e)
            #return HttpResponseRedirect('/signup?pid='+pid+'&err=Form Field Errors')

class CustomerLoginClass(TemplateView):
    def post(self, request, *args, **kwargs):
        logout(request)
        customer_list=""
        form = LoginForm(request.POST)
        if form.is_valid():
            logging.info('Form Is clean')
            username = request.POST['username']
            password = request.POST['password']
            #logging.info('Remember Me not here %s %s',username,password)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active and (not user.is_superuser and not user.is_staff):
                    if request.POST.has_key('remember'):
                        logging.info('Remember Me increased to 5 days')
                        request.session.set_expiry(1209600)
                    else:
                        logging.info('Remember Me not here')
                    login(request, user)

                    return HttpResponseRedirect('/myaccount')
                else:
                    request.session['ErrorMessage'] = "account does not exist"
                    return HttpResponseRedirect('/login')
                success = True
                logging.info('LoginfoMessage:: %s',username)
                return HttpResponseRedirect(target_page)
            else:
                request.session['ErrorMessage'] = "Invalid Username or Password."
                return HttpResponseRedirect('/login')
        else:
            request.session['ErrorMessage'] = "Invalid Form data."
            return HttpResponseRedirect('/login')

class PricesViewClass(TemplateView):
    def get(self, request, *args, **kwargs):
        prices = Pricing.objects.filter(status=1)
        content = {'title': "Prices",'prices':prices}
        return render_template(request, "page_prices.html", content)

class MyaccountViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        
        logging.info('User Started::  %s', request.user.id)
        countries=ShippingCountries.objects.all().filter(enabled=1)
        userprofiles= UserProfile.objects.get(user_id = request.user.id)
        content = {'page_title': "Edit Profile",'regform':RegistrationForm,
                   'countries':countries,'userprofiles':userprofiles}
        return render_template(request, "user_templates/index.html", content)
    def post(self, request, *args, **kwargs):
        pass


class OddtypesViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        sidevalues=""
        oddnum = ""
        resp = requests.get(ODDTYPES_URL)
        xmldoc = minidom.parseString(resp.text)
        itemlist = xmldoc.getElementsByTagName('type')
        for s in itemlist:
            #print s.getElementsByTagName("name")[0].childNodes[0].data
            oddnum = str(s.getElementsByTagName("ot")[0].childNodes[0].data)
            sidevalues += '<li><a data-toggle="tab" href="javascript:;" onClick="datastream('+oddnum+');">'
            sidevalues += '<i class="fa fa-eye"></i> '+str(s.getElementsByTagName("name")[0].childNodes[0].data)+'</a></li>'
        content = {'page_title': "Odd Types",'sidevalues':sidevalues}
        return render_template(request, "odd_types.html", content)

class FeedsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        sidevalues=""
        values = {"ident":USERID,"passwd":PSWD,
                  'ot':request.GET['ot']}
        resp = requests.get(FEED_URL, params=values)
        
        xmldoc = minidom.parseString(resp.text.encode('utf-8'))
        itemlist = xmldoc.getElementsByTagName('match')
        matchname = ""
        last = 0
        for s in itemlist:
            matchname = str(s.getElementsByTagName("group")[0].childNodes[0].data).encode('utf8')
            countries =s.getElementsByTagName("hteam")[0].childNodes[0].data.encode('utf-8').decode('utf-8')+' vs '
            
            countries += s.getElementsByTagName("ateam")[0].childNodes[0].data.encode('utf-8').decode('utf-8')
            sidevalues += '<tr><th align=left colspan=9> '+matchname+' <span style="float:right"> '+countries+'</span></th></tr>'
            for n in s.getElementsByTagName("bookmaker"):
                sidevalues += '<tr><td class="active">'+n.getAttribute('name')+'</td>'
               
                for k in n.getElementsByTagName("odds"):
                    sidevalues += '<td>&nbsp;</td>'
                    sidevalues += '<td class="success">'+k.getElementsByTagName("o1")[0].childNodes[0].data+'</td>'
                    sidevalues += '<td class="warning">'+k.getElementsByTagName("o2")[0].childNodes[0].data+'</td>'
                    sidevalues += '<td class="danger">'+k.getElementsByTagName("o3")[0].childNodes[0].data+'</td>'
                    
                    #for j in k.getElementsByTagName("o1"):
                        #sidevalues += '<td class="success">'+j.childNodes[0].data+'</td>'
                        #sidevalues += '<td class="success">'+j.childNodes[1].data+'</td>'
                        #sidevalues += '<td class="success">'+j.childNodes[2].data+'</td>'
                sidevalues += '</tr>'
        content = {'page_title': "Odd Types",'sidevalues':sidevalues.encode('utf8')}
        return render_template(request, "oddstable.html", content)

class SportFeedsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        sidevalues=""
        values = {"ident":USERID,"passwd":PSWD,
                  'spid':request.GET['spid']}
        resp = requests.get(FEED_URL, params=values)
        
        xmldoc = minidom.parseString(resp.text.encode('utf-8'))
        itemlist = xmldoc.getElementsByTagName('match')
        matchname = ""
        last = 0
        for s in itemlist:
            matchname = str(s.getElementsByTagName("group")[0].childNodes[0].data).encode('utf8')
            #countries = str(s.getElementsByTagName("hteam")[0].childNodes[0].data)+' vs '+str(s.getElementsByTagName("ateam")[0].childNodes[0].data)
            countries =s.getElementsByTagName("hteam")[0].childNodes[0].data.encode('utf-8').decode('utf-8')+' vs '
            countries += s.getElementsByTagName("ateam")[0].childNodes[0].data.encode('utf-8').decode('utf-8')
            sidevalues += '<tr><th align=left colspan=9> '+matchname+' <span style="float:right"> '+countries+'</span></th></tr>'
            for n in s.getElementsByTagName("bookmaker"):
                sidevalues += '<tr><td class="active">'+n.getAttribute('name')+'</td>'
                for k in n.getElementsByTagName("odds"):
                    sidevalues += '<td>&nbsp;</td>'
                    sidevalues += '<td class="success">'+k.getElementsByTagName("o1")[0].childNodes[0].data+'</td>'
                    sidevalues += '<td class="warning">'+k.getElementsByTagName("o2")[0].childNodes[0].data+'</td>'
                    sidevalues += '<td class="danger">'+k.getElementsByTagName("o3")[0].childNodes[0].data+'</td>'
                sidevalues += '</tr>'
        content = {'page_title': "Odd Types",'sidevalues':sidevalues.encode('utf8')}
        return render_template(request, "oddstable.html", content)

class SporttypesViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        sidevalues=""
        oddnum = ""
        resp = requests.get(SPORTS_URL)
        xmldoc = minidom.parseString(resp.text)
        itemlist = xmldoc.getElementsByTagName('sport')
        for s in itemlist:
            #print s.getElementsByTagName("name")[0].childNodes[0].data
            oddnum = str(s.getElementsByTagName("id")[0].childNodes[0].data)
            sidevalues += '<li><a data-toggle="tab" href="javascript:;" onClick="datastream('+oddnum+');">'
            sidevalues += '<i class="fa fa-eye"></i> '+str(s.getElementsByTagName("name")[0].childNodes[0].data)+'</a></li>'
        content = {'page_title': "Odd Types",'sidevalues':sidevalues}
        return render_template(request, "sport_types.html", content)

class BookmakertypesViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        sidevalues=""
        oddnum = ""
        resp = requests.get(BOOKMAKER_URL)
        xmldoc = minidom.parseString(resp.text)
        itemlist = xmldoc.getElementsByTagName('bookmaker')
        for s in itemlist:
            oddnum = str(s.getAttribute('name'))
            booknum = str(s.getAttribute('id'))
            sidevalues += '<li><a data-toggle="tab" href="javascript:;" onClick="datastream('+booknum+');">'
            sidevalues += '<i class="fa fa-eye"></i> '+str(oddnum)+'</a></li>'
        content = {'page_title': "Odd Types",'sidevalues':sidevalues}
        return render_template(request, "bookmaker_types.html", content)

class BookmakerFeedsViewClass(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        sidevalues=""
        values = {"ident":USERID,"passwd":PSWD,
                  'bid':request.GET['bid']}
        resp = requests.get(FEED_URL, params=values)
        
        xmldoc = minidom.parseString(resp.text.encode('utf-8'))
        itemlist = xmldoc.getElementsByTagName('match')
        matchname = ""
        last = 0
        for s in itemlist:
            matchname = str(s.getElementsByTagName("group")[0].childNodes[0].data).encode('utf8')
            #countries = str(s.getElementsByTagName("hteam")[0].childNodes[0].data)+' vs '+str(s.getElementsByTagName("ateam")[0].childNodes[0].data)
            countries =s.getElementsByTagName("hteam")[0].childNodes[0].data.encode('utf-8').decode('utf-8')+' vs '
            countries += s.getElementsByTagName("ateam")[0].childNodes[0].data.encode('utf-8').decode('utf-8')
            sidevalues += '<tr><th align=left colspan=9> '+matchname+' <span style="float:right"> '+countries+'</span></th></tr>'
            for n in s.getElementsByTagName("bookmaker"):
                sidevalues += '<tr><td class="active">'+n.getAttribute('name')+'</td>'
                for k in n.getElementsByTagName("odds"):
                    sidevalues += '<td>&nbsp;</td>'
                    sidevalues += '<td class="success">'+k.getElementsByTagName("o1")[0].childNodes[0].data+'</td>'
                    sidevalues += '<td class="warning">'+k.getElementsByTagName("o2")[0].childNodes[0].data+'</td>'
                    sidevalues += '<td class="danger">'+k.getElementsByTagName("o3")[0].childNodes[0].data+'</td>'
                sidevalues += '</tr>'
        content = {'page_title': "Odd Types",'sidevalues':sidevalues.encode('utf8')}
        return render_template(request, "oddstable.html", content)


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
