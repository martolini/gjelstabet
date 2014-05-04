from django.db import models
from django.contrib.auth.models import User
from django import forms
import logging, random, hashlib, datetime, settings

def validate_not_spaces(value):
    if value.strip() == '':
        
        raise ValidationError(u"You must provide more than just whitespace.")

class Languages(models.Model):
    id = models.IntegerField()
    lang_text = models.CharField(max_length=224)
    enabled = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(default=False)
    class Meta:
        db_table = u'site_languages'
        app_label = ''

REGISTRATIONTYPE = (
    ('FB', 'Facebook'),
    ('GOOGLE', 'Google'),
    ('EMAIL', 'Email'),)

OBJECTTYPES = (
    ('PROFILE_PIC', 'ProfilePic'),
    ('BACKGROUND_PIC', 'BackgroundPIC'),
    ('EMAIL', 'Email'),)


class GENDER():
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

PALSTATUSTYPE = (
    ('PENDING', 'Pending'),
    ('BLOCKED', 'Blocked'),
    ('FRIENDS', 'Accepted'),)


class UserProfile(models.Model):
    """
    A model to store extra information for each user.
    """
    user = models.OneToOneField(User, related_name='profile')
    gender = models.CharField(max_length=50, choices=GENDER.CHOICES)
    birth_year = models.CharField(max_length=150, blank=True)
    age = models.SmallIntegerField()
    uuid_field = UUIDField()
    phone = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=15, blank=True)
    is_flag = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    activation_code = models.CharField(max_length=65, blank=False)
    #language = models.IntegerField(default=False)
    reset_code = models.TextField(null=True, blank=True)
    reset_status = models.IntegerField(null=True, blank=True)
    lattitude = models.CharField(max_length=50, blank=True)
    longitude = models.CharField(max_length=50, blank=True)
    identifierforvendor = models.CharField(max_length=100, blank=True)
    about_me = models.TextField(null=True, blank=True)    
    registration_type = models.CharField(_('Provide User Type FB, GOOGLE, EMAIL'),
                                 choices=REGISTRATIONTYPE, blank=True, null=True,
                                 max_length=10)
    class Meta:
        app_label = ''
        db_table = u'userprofile'

    def __str__(self):
        return self.user.get_full_name()


class Medialist(models.Model):
    id = models.IntegerField()
    media_text = models.CharField(max_length=224)
    language = models.ForeignKey(Languages)
    enabled = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(default=False)
    created_time = models.DateTimeField(null=True, blank=True)
    country = models.IntegerField(default=False)
    period = models.CharField(max_length=100)
    class Meta:
        db_table = u'site_medialist'
        app_label = ''

class Colorist(models.Model):
    id = models.IntegerField()
    color_text = models.CharField(max_length=224)
    language_id = models.IntegerField(null=True,)
    enabled = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(default=False)
    created_time = models.DateTimeField(null=True, blank=True)
    country = models.IntegerField(default=False)
    type = models.CharField(max_length=100)
    parent_lang = models.IntegerField(null=True)
    class Meta:
        db_table = u'site_colorlist'
        app_label = ''

class SeasonsManagement(models.Model):
    id = models.IntegerField()
    season_code = models.CharField(max_length=224)
    language = models.IntegerField(null=True,)
    enabled = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(default=False)
    created_time = models.DateTimeField(null=True, blank=True)
    season_description = models.TextField(null=True, blank=True)
    parent_season = models.IntegerField(null=True)
    class Meta:
        db_table = u'seasons_management'
        app_label = ''

class UserLogs(models.Model):
    id = models.IntegerField()
    content_type_id = models.IntegerField(null=True,)
    object_repr = models.TextField(null=True, blank=True)
    user_id = models.IntegerField(default=False)
    action_time = models.DateTimeField(null=True, blank=True)
    object_id = models.TextField(null=True, blank=True)
    change_message = models.TextField(null=True, blank=True)
    action_flag = models.IntegerField(null=True)
    class Meta:
        db_table = u'django_user_log'
        app_label = ''


class StaticFiles(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    gs_object_name = models.CharField(max_length=1024)
    content_type = models.CharField(max_length=100)
    creation = models.DateTimeField()
    filename = models.CharField(max_length=1024)
    size = models.IntegerField()
    md5 = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    enabled = models.IntegerField(null=True, blank=True)
    language_id = models.IntegerField(default=False)
#    image = models.ImageField()

        
    def fullfileUrl(self):
        urlimg=self.gs_object_name
        urlimg=urlimg.replace("/gs/", "");
        return urlimg
    
    class Meta:
        app_label = ''
        db_table = u'staticfiles'


class Languages(models.Model):
    id = models.IntegerField()
    lang_text = models.CharField(max_length=224)
    enabled = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(default=False)
    class Meta:
        db_table = u'site_languages'
        app_label = ''

class SiteMenuLinks(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=224)
    enabled = models.IntegerField(null=True, blank=True)
    long = models.TextField(blank=True)
    link = models.CharField(max_length=224)
    created_by = models.IntegerField(default=False)
    created_time = models.DateTimeField(null=True, blank=True)
    language_id = models.IntegerField(null=True)
    parent_lang = models.IntegerField(null=True)
    is_profficer = models.IntegerField(default=False)
    is_admin = models.IntegerField(default=False)
    is_imageowner = models.IntegerField(default=False)
    is_journalist = models.IntegerField(default=False)
    menu_id = models.IntegerField(default=False)
    class Meta:
        db_table = u'site_menulinks'
        app_label = ''

class SiteMenuHeader(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=224)
    enabled = models.IntegerField(null=True, blank=True)
    long = models.TextField(blank=True)
    link = models.CharField(max_length=224)
    created_by = models.IntegerField(default=False)
    created_time = models.DateTimeField(null=True, blank=True)
    language_id = models.IntegerField(null=True)
    parent_lang = models.IntegerField(null=True)
    is_profficer = models.IntegerField(default=False)
    is_admin = models.IntegerField(default=False)
    is_imageowner = models.IntegerField(default=False)
    is_journalist = models.IntegerField(default=False)
    class Meta:
        db_table = u'site_menuheader'
        app_label = ''

class Admins(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=150, blank=True)
    pass_field = models.CharField(max_length=150, db_column='pass', blank=True) # Field renamed because it was a Python reserved word.
    userlevel = models.IntegerField(null=True, blank=True)
    permissions = models.TextField(blank=True)
    ip_restricted = models.CharField(max_length=150, blank=True)
    lastlogin = models.DateTimeField(null=True, blank=True)
    lastchange = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=765, blank=True)
    usersession = models.CharField(max_length=96, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    terms_accepted = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=150, blank=True)
    resetpasskey = models.CharField(max_length=150, blank=True)
    resetpassexp = models.DateTimeField(null=True, blank=True)
    class Meta:
        app_label = ''
 
   

class GlobalTextsContent(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=124)
    title_short = models.CharField(max_length=224)
    class Meta:
        db_table = u'global_texts'
        app_label = ''

class SiteTextsContent(models.Model):
    id = models.IntegerField()
    title = models.CharField(max_length=124)
    title_short = models.CharField(max_length=224)
    title_long = models.TextField(blank=True)
    parent_lang = models.IntegerField(null=True)
    language_id = models.IntegerField(null=True)
    class Meta:
        db_table = u'site_content'
        app_label = ''


class Emails(models.Model):
    id = models.IntegerField()
    etype = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=150, blank=True)
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    to = models.CharField(max_length=150, blank=True)
    order_status = models.IntegerField(null=True, blank=True)
    body_html = models.TextField(blank=True)
    from_email = models.CharField(max_length=765, blank=True)
    reply_email = models.CharField(max_length=765, blank=True)
    bcc_email = models.CharField(max_length=765, blank=True)
    section = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'emails'
        app_label = ''

class Extrapages(models.Model):
    id = models.IntegerField()
    htmlpage = models.CharField(max_length=750, blank=True)
    title = models.TextField(blank=True)
    meta = models.TextField(blank=True)
    content = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    hide = models.IntegerField(null=True, blank=True)
    link = models.TextField(blank=True)
    link_target = models.CharField(max_length=150, blank=True)
    page_parent = models.IntegerField(null=True, blank=True)
    isdatabase = models.IntegerField(null=True, blank=True)
    recordsperpage = models.IntegerField(null=True, blank=True)
    page_displaytype = models.IntegerField(null=True, blank=True)
    showindex = models.IntegerField(null=True, blank=True)
    showrss = models.IntegerField(null=True, blank=True)
    feed_sorting = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    accessgroup = models.IntegerField(null=True, blank=True)
    redirectto = models.CharField(max_length=450, blank=True)
    filename = models.CharField(max_length=765, blank=True)
    hide_left = models.IntegerField(null=True, blank=True)
    hide_right = models.IntegerField(null=True, blank=True)
    frame_displaytype = models.IntegerField(null=True, blank=True)
    keywords = models.TextField(blank=True)
    class Meta:
        db_table = u'extrapages'
        app_label = ''

class Html(models.Model):
    id = models.IntegerField()
    htmlpage = models.CharField(max_length=150, blank=True)
    title = models.TextField(blank=True)
    meta = models.TextField(blank=True)
    header = models.TextField(blank=True)
    footer = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    userid = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    hide_left = models.IntegerField(null=True, blank=True)
    hide_right = models.IntegerField(null=True, blank=True)
    keywords = models.TextField(blank=True)
    class Meta:
        db_table = u'html'
        app_label = ''


class ProductCategory(models.Model):
    id = models.IntegerField()
    catalogid = models.IntegerField(db_index=True,null=True, blank=True)
    categoryid = models.IntegerField(db_index=True,null=True, blank=True)
    ismain = models.CharField(db_index=True,max_length=150, blank=True)
    sorting = models.IntegerField(db_index=True,null=True, blank=True)
    class Meta:
        db_table = u'product_category'
        app_label = ''

class ProductEmailfriend(models.Model):
    id = models.IntegerField(primary_key=True)
    catalogid = models.IntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=150, blank=True)
    user_email = models.CharField(max_length=150, blank=True)
    friend_name = models.CharField(max_length=150, blank=True)
    friend_email = models.CharField(max_length=450, blank=True)
    message = models.TextField(blank=True)
    record_date = models.DateTimeField(null=True, blank=True)
    userid = models.IntegerField(null=True, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'product_emailfriend'
        app_label = ''

class ProductReview(models.Model):
    id = models.IntegerField(db_index=True,primary_key=True)
    catalogid = models.IntegerField(db_index=True,null=True, blank=True)
    user_name = models.CharField(db_index=True,max_length=150, blank=True)
    user_email = models.CharField(db_index=True,max_length=150, blank=True)
    user_city = models.CharField(db_index=True,max_length=150, blank=True)
    short_review = models.CharField(db_index=True,max_length=450, blank=True)
    long_review = models.TextField(db_index=True,blank=True)
    rating = models.IntegerField(db_index=True,null=True, blank=True)
    review_date = models.DateTimeField(db_index=True,null=True, blank=True)
    approved = models.IntegerField(db_index=True,null=True, blank=True)
    userid = models.IntegerField(db_index=True,null=True, blank=True)
    userip = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'product_review'
        app_label = ''

class ShippingCountries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True)
    name_short = models.CharField(max_length=150, db_column='name_short', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    enabled = models.IntegerField(null=True, blank=True)
    enabled_billing = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_countries'
        app_label = ''

class ShippingStates(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=150, blank=True)
    name_short = models.CharField(max_length=150, db_column='name-short', blank=True) # Field renamed to remove dashes. Field name made lowercase.
    enabled = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'shipping_states'
        app_label = ''

class Template(models.Model):
    template = models.CharField(max_length=150, blank=True)
    stylesheet = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'template'
        app_label = ''






