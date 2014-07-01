from django.contrib.auth import *
from django.contrib.auth.models import User
from django.http import *
from gjelstabet.forms import LoginForm
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
import logging, random, hashlib, datetime
from gjelstabet.models import *
from django.core.context_processors import csrf

@csrf_exempt
def render_template(request, template, data=None):
    errs =""
    if request.method == 'GET' and 'err' in request.GET:
        data.update({'errs':request.GET['err']})
    
    response = render_to_response(template, data,
                              context_instance=RequestContext(request))
    return response

def GetRecaptcha(request):
    value = random.randrange(10000, 99999, 1)
    request.session['ReCaptcha'] = value
    return value

@csrf_exempt
def CustomerLoginClass1(request):
    if request.method == 'POST':
        if 'target' in request.POST:
            target_page = request.POST['target']
        else:
            target_page = "/"
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

                    return HttpResponseRedirect('/')
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
    else:
        request.session['ErrorMessage'] = "Form submission is not as expected."
        return HttpResponseRedirect('/login')

class LoginPageClass(TemplateView):
    def get(self, request, *args, **kwargs):
        content = {'page_title': "Login",'form': LoginForm(),}
        return render_template(request, "login.html", content)

class LogoutClass(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/login')