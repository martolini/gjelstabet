from django import forms
from django.forms import ModelForm
from models import UserProfile, User, ShippingCountries, Languages
import logging
from django.contrib.auth import authenticate, login


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Username'}),max_length = 50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
    recaptcha = forms.CharField(max_length = 50, required=False,widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Enter Above Number'}))
    
class ForgetPwdForm(forms.Form):
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Email Address'}))

class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField()

class UploadForm(forms.Form):
    file = forms.FileField() 
    description = forms.CharField ( widget=forms.widgets.Textarea() )

class AddressForm(forms.Form):
    STATES = (('', 'Select State'), ('AL', 'Alabama'),('AK', 'Alaska'),('AZ', 'Arizona'),('AR', 'Arkansas'),
            ('CA', 'California'),('CO', 'Colorado'),('CT', 'Connecticut'),('DE', 'Delaware'),
            ('FL', 'Florida'),('GA', 'Georgia'),('HI', 'Hawaii'),('ID', 'Idaho'),('IL', 'Illinois'),
            ('IN', 'Indiana'),('IA', 'Iowa'),('KS', 'Kansas'),('KY', 'Kentucky'),('LA', 'Louisiana'),
            ('ME', 'Maine'),('MD', 'Maryland'),('MA', 'Massachusetts'),('MI', 'Michigan'),
            ('MN', 'Minnesota'),('MS', 'Mississippi'),('MO', 'Missouri'),('MT', 'Montana'),
            ('NE', 'Nebraska'),('NV', 'Nevada'),('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
            ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),('VT', 'Vermont'),('VA', 'Virginia'),
            ('WA', 'Washington'),('WV', 'West Virginia'),('WI', 'Wisconsin'),('WY', 'Wyoming'))  

    contact_id = forms.CharField(widget=forms.HiddenInput, required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'First Name'}),max_length = 200)
    last_name = forms.CharField(max_length = 50L, required=True)
    company = forms.CharField(max_length = 255L, required=False)
    phone = forms.CharField(max_length = 50L, required=True)
    address1 = forms.CharField(max_length = 255L, required=True)
    address2 = forms.CharField(max_length = 255L, required=False)
    city = forms.CharField(max_length = 50L, required=True)
    country = forms.CharField(max_length = 100L, required=True)
    state = forms.ChoiceField(choices=STATES,  initial='FL')
    zip = forms.CharField(max_length = 20L, required=True)
    address_type = forms.CharField(widget=forms.HiddenInput, required=False)


class BillingShippingAddressForm(forms.Form):
  COUNTRIES = (('USA','United States'), ('UK', 'United Kingdom'))

  STATES = (('', 'Select State'), ('AL', 'Alabama'),('AK', 'Alaska'),('AZ', 'Arizona'),('AR', 'Arkansas'),
            ('CA', 'California'),('CO', 'Colorado'),('CT', 'Connecticut'),('DE', 'Delaware'),
            ('FL', 'Florida'),('GA', 'Georgia'),('HI', 'Hawaii'),('ID', 'Idaho'),('IL', 'Illinois'),
            ('IN', 'Indiana'),('IA', 'Iowa'),('KS', 'Kansas'),('KY', 'Kentucky'),('LA', 'Louisiana'),
            ('ME', 'Maine'),('MD', 'Maryland'),('MA', 'Massachusetts'),('MI', 'Michigan'),
            ('MN', 'Minnesota'),('MS', 'Mississippi'),('MO', 'Missouri'),('MT', 'Montana'),
            ('NE', 'Nebraska'),('NV', 'Nevada'),('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
            ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),('VT', 'Vermont'),('VA', 'Virginia'),
            ('WA', 'Washington'),('WV', 'West Virginia'),('WI', 'Wisconsin'),('WY', 'Wyoming'))  

  contact_id = forms.CharField(widget=forms.HiddenInput, required=False)
  billing_first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'ON', 'size':130}),max_length = 50, required=True)
  billing_last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control','autocomplete':'ON', 'size':130}),max_length = 50, required=True)
  billing_company = forms.CharField(max_length = 255L, required=False)
  billing_phone_part1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':1, 'maxlength':3, 'style':'width:25px' }),max_length = 3, required=False)
  billing_phone_part2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':1, 'maxlength':3, 'style':'width:25px'}),max_length = 3, required=False)
  billing_phone_part3 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':2, 'maxlength':4, 'style':'width:30px'}),max_length = 4, required=False)
  billing_phone_ext = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)
  billing_address1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=False)
  billing_address2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=False)
  billing_city = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':10}),max_length = 50, required=False)
  billing_state = forms.ChoiceField(choices=STATES, required = False)
  billing_country =  forms.ChoiceField(choices=COUNTRIES, initial='USA')
  billing_zip = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':5, 'maxlength':5, 'style':'width:40px'}), max_length = 5, required=False)

  shipping_first_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':30}),max_length = 50, required=False)
  shipping_last_name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':30}),max_length = 50, required=False)
  shipping_company = forms.CharField(max_length = 255L, required=False)
  shipping_phone_part1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3, 'maxlength':3, 'style':'width:25px'}), max_length = 3, required=False)
  shipping_phone_part2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3, 'maxlength':3, 'style':'width:25px'}), max_length = 3, required=False)
  shipping_phone_part3 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3, 'maxlength':4, 'style':'width:30px'}), max_length = 4, required=False)
  shipping_phone_ext = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':3}),max_length = 50, required=False)
  shipping_address1 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=False)
  shipping_address2 = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':40}),max_length = 50, required=False)
  shipping_city = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':10}),max_length = 50, required=False)
  shipping_state = forms.ChoiceField(choices=STATES) 
  shipping_zip = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'ON', 'size':5, 'maxlength':5, 'style':'width:40px'}), max_length = 5, required=False) 


class RegistrationForm(forms.Form):
  email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Email Address'}),max_length = 200)
  first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'First Name'}),max_length = 50L)
  last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Last Name'}),max_length = 50L)
  password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
  cpassword = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Confirm Password'}), max_length=50)
  phone = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Phone'}),max_length = 50, required=False)
  country =  forms.ChoiceField(choices=[ (o.id, o.name) for o in ShippingCountries.objects.all().filter(enabled=1)], initial='USA',widget=forms.Select(attrs={'class' : 'form-control', 'autocomplete':'OFF'}))
  
  def __init__(self, *args, **kwargs):
      super(RegistrationForm, self).__init__(*args, **kwargs)
  
  def clean_email(self):
      if User.objects.filter(email=self.cleaned_data['email']).count() > 0:
          raise forms.ValidationError('Email Address already registered')
      return self.cleaned_data['email']
  def save(self, request):
      
      user = User()
      user.username = self.cleaned_data['email']
      user.first_name = self.cleaned_data['first_name']
      user.last_name = self.cleaned_data['last_name']
      if self.cleaned_data['password'] != '':
          user.set_password(self.cleaned_data['password'])
      user.email = self.cleaned_data['email']
      user.save()
      if self.cleaned_data['password'] != '':
          user = authenticate(username=user.username, password=self.cleaned_data['password'])
        
      userprofile = UserProfile()
      userprofile.user = user
      userprofile.is_journalist = 1
      userprofile.phone = self.cleaned_data['phone']
      userprofile.offline_magazine = self.cleaned_data['offline_magazine']
      userprofile.online_magazine = self.cleaned_data['online_magazine']
      userprofile.tvname = self.cleaned_data['tvname']
      userprofile.language = self.cleaned_data['languages']
      userprofile.save()
      
      mail.send_mail(sender="support <accounts@example.com>",
                     to="PrMediaStore.com Support <accounts@prmediastore.com>",
                     subject=user.first_name+" "+user.last_name+"<"+user.email+"> Account Registration",
                     body="""
                     Greetings:
                     We would like to thank you for registering with PR Media Store. We hope you enjoy 
                     our service and please do let us know any suggestion you might have either via 
                     sales@prmediastore.com or our website. 
                     Thank you and have a nice day ! 
                     Your PR Media Store Team
                     """)
      return userprofile


class ProfileDetailsForm(forms.Form):
    USERTYP = (('1','Image Owner'), ('2', 'PR Officer'))
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Email Address'}),max_length = 200)
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Username'}),max_length = 50, required=False)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50, required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'First Name'}),max_length = 50L)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Last Name'}),max_length = 50L)
    u_type = forms.ChoiceField(widget=forms.RadioSelect, choices=USERTYP)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Phone'}),max_length = 50, required=False)
    
    def __init__(self, *args, **kwargs):
        super(ProfileDetailsForm, self).__init__(*args, **kwargs)

    def clean_email(self):        
        if User.objects.filter(email=self.cleaned_data['email']).count() > 0:
            raise forms.ValidationError('Email Address already registered')
        return self.cleaned_data['email']

    def save(self, request):
        logging.info('User Type:: %s',self.cleaned_data['u_type'])
        user = User()
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['password'] != '':
            user.set_password(self.cleaned_data['password'])
        if self.cleaned_data['u_type'] == "2":
            user.is_staff=1
        user.email = self.cleaned_data['email']
        user.save()

        if self.cleaned_data['password'] != '':
            user = authenticate(username=user.username, password=self.cleaned_data['password'])
        
        userprofile = UserProfile()
        userprofile.user = user
        if self.cleaned_data['u_type'] == "1":
            userprofile.is_imageowner = self.cleaned_data['u_type']
        userprofile.phone = self.cleaned_data['phone']
        current_user = request.user
        userprofile.created_by = current_user.id
        userprofile.save()
        return userprofile

class UserForm(forms.Form):
    STATUSES = (('1','Super Admin'), ('1', 'PR Officer'), ('1', 'Image Owner'))
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Email Address'}),max_length = 200)
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Username'}),max_length = 50)
    user_type = forms.ChoiceField(choices=STATUSES, required = False, widget=forms.Select(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
    confirmpass = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Confirm Password'}), max_length=50)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'First Name'}),max_length = 50L)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Last Name'}),max_length = 50L)

class ChangePwdForm(forms.Form):
    #username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address', 'disabled':"disabled"}),max_length = 50)
    #old_password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
    #new_password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=50)
    #username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address', 'disabled':"disabled"}),max_length = 50, required=False)
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'Old Password'}), max_length = 25L)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control', 'autocomplete':'OFF', 'placeholder':'New Password'}), max_length = 25L)
    


#--- Murthy Added Forms from 2013-16-17 --

class CreditCardForm(forms.Form):
  previous_cards = forms.ChoiceField(choices=[], widget=forms.RadioSelect(), required=False)
  card_holder_name = forms.CharField(max_length = 50L)
  card_type = forms.ChoiceField(choices=[('V', 'Visa'), ('M', 'Master')])
  card_number = forms.CharField(max_length = 50L)
  card_expdate = forms.CharField(max_length = 5L)
  card_cvn = forms.CharField(max_length = 5L)
  is_save_card = forms.BooleanField(required=False, label="Check this")
  
  def __init__(self, *args, **kwargs):
    card_list = kwargs.pop('card_list')
    super(CreditCardForm, self).__init__(*args,**kwargs)
    self.fields['previous_cards'].choices = card_list 
 
 
  
class NewAccountForm(forms.Form):
  username1 = forms.CharField(widget=forms.TextInput(attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Email Address'}),max_length = 50)
  password1 = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Password'}), max_length=25)
  confirm_password1 = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class' : 'txt-box1', 'autocomplete':'OFF', 'placeholder':'Confirm Password'}), max_length=25) 
  
class PaypalOrderFormNoLogin(BillingShippingAddressForm, NewAccountForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)
 
class PaypalOrderFormLoggedIn(BillingShippingAddressForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class AuthorizeNetFormNoLogin(BillingShippingAddressForm, CreditCardForm, NewAccountForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class AuthorizeNetFormLoggedIn(BillingShippingAddressForm, CreditCardForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)



class NoGateWay(BillingShippingAddressForm):
  comment = forms.CharField(widget=forms.Textarea, max_length = 255L, required=False)

class RadioForm(forms.Form):
  STATES = (('AL', 'Alabama'),('AK', 'Alaska'),('AZ', 'Arizona'),('AR', 'Arkansas'),
            ('CA', 'California'),('CO', 'Colorado'),('CT', 'Connecticut'),('DE', 'Delaware'),
            ('FL', 'Florida'),('GA', 'Georgia'),('HI', 'Hawaii'),('ID', 'Idaho'),('IL', 'Illinois'),
            ('IN', 'Indiana'),('IA', 'Iowa'),('KS', 'Kansas'),('KY', 'Kentucky'),('LA', 'Louisiana'),
            ('ME', 'Maine'),('MD', 'Maryland'),('MA', 'Massachusetts'),('MI', 'Michigan'),
            ('MN', 'Minnesota'),('MS', 'Mississippi'),('MO', 'Missouri'),('MT', 'Montana'),
            ('NE', 'Nebraska'),('NV', 'Nevada'),('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
            ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),('VT', 'Vermont'),('VA', 'Virginia'),
            ('WA', 'Washington'),('WV', 'West Virginia'),('WI', 'Wisconsin'),('WY', 'Wyoming'))  

  shipping_state = forms.ChoiceField(choices=STATES, initial='CA')
