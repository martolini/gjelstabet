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

class UserProfile(models.Model):
    # Aggregate using a OneToOneField on User
    user = models.OneToOneField(User)
    is_journalist = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True)
    offline_magazine = models.CharField(max_length=150, null=True)
    online_magazine = models.CharField(max_length=150, null=True)
    tvname = models.CharField(max_length=150, null=True)
    postal_code = models.PositiveIntegerField(null=True)
    phone = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=15, blank=True)
    is_imageowner = models.IntegerField(default=False)
    is_vip = models.IntegerField(default=False)
    language = models.IntegerField(default=False)
    created_by = models.IntegerField(default=False)
    reset_code = models.TextField(null=True, blank=True)
    reset_status = models.IntegerField(null=True, blank=True)
    class Meta:
        app_label = ''
        db_table = u'userprofile'

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

# Create your models here.
class ImageStore(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    gs_object_name = models.CharField(max_length=1024)
    content_type = models.CharField(max_length=100)
    creation = models.DateTimeField()
    filename = models.CharField(max_length=1024)
    size = models.IntegerField()
    md5 = models.CharField(max_length=100)
    thumb_gs_object_name = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)
#    image = models.ImageField()

    def imageUrl(self):
        from google.appengine.api import blobstore, images
        imgdat=""
        try:
            blob_key = blobstore.create_gs_key(self.gs_object_name)
            imgdat=images.get_serving_url(blob_key)
        except Exception, e:
            logging.info('LoginfoMessage ImageID:: %s',self.gs_object_name)
            logging.info('LoginfoMessage error:: %s',e)
            imgdat=""
#        image.execute_transforms(output_encoding=images.JPEG)
#        return image.get_serving_url()
        return imgdat
    
    def imageUrlKey(self):
        from google.appengine.api import blobstore, images
        imgdat=""
        try:
            blob_key = blobstore.create_gs_key(self.gs_object_name)
            imgdat=images.get_serving_url(blob_key)
        except Exception, e:
            logging.info('LoginfoMessage ImageID:: %s',self.gs_object_name)
            logging.info('LoginfoMessage error:: %s',e)
            imgdat=""
#        image.execute_transforms(output_encoding=images.JPEG)
#        return image.get_serving_url()
        return blob_key
    
    def fullimageUrl(self):
        from google.appengine.api import blobstore, images
        urlimg=""
        try:
            blob_key = blobstore.create_gs_key(self.gs_object_name)
            urlimg = images.get_serving_url(blob_key, size=None, crop=False, secure_url=None)
        except Exception, e:
            logging.info('LoginfoMessage ImageID:: %s',self.gs_object_name)
            logging.info('LoginfoMessage error:: %s',e)
            urlimg=""
#        image.execute_transforms(output_encoding=images.JPEG)
#        return image.get_serving_url()
        return urlimg
    def imageresize(self):
        
        imgdat=""
        try:
            
            imgdat=self.size/(1024*1000)
            if imgdat < 1:
                imgdat=1
            else:
                imgdat = imgdat
        except Exception, e:
            logging.info('LoginfoMessage ImageID:: %s',self.gs_object_name)
            logging.info('LoginfoMessage error:: %s',e)
            imgdat=""
#        image.execute_transforms(output_encoding=images.JPEG)
#        return image.get_serving_url()
        return imgdat
    def imageshortName(self):
        import os
        imgsht = ""
        try:
            fileNamed, fileExtension = os.path.splitext(filename)
            imgsht=fileNamed
        except Exception, e:
            imgsht=""
        return imgsht
    class Meta:
        app_label = ''
        db_table = u'imagestore_imagestore'

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

class ImageContent(models.Model):
    id = models.IntegerField()
    img_id = models.IntegerField(null=False, blank=False)
    file_name = models.CharField(max_length=150, null=True)
    catid = models.IntegerField()
    brand_name = models.CharField(max_length=150, null=True)
    article_num = models.CharField(max_length=15, null=True)
    short = models.TextField(blank=True)
    long = models.TextField(blank=True)
    website_brand = models.CharField(max_length=150, blank=True)
    website_store = models.CharField(max_length=150, blank=True)
    market_avail=models.CharField(max_length=150, blank=True)
    copyright_avail=models.CharField(max_length=150, blank=True)
    copyright_till=models.CharField(max_length=150, blank=True)
    material = models.CharField(max_length=150, blank=True)
    sizes = models.CharField(max_length=15, blank=True)
    colorid = models.IntegerField()
    price = models.CharField(max_length=15, blank=True)
    language = models.IntegerField(null=True)
    created_by = models.IntegerField(null=True)
    created_time = models.DateTimeField(null=True, blank=True)
    parent_lang = models.IntegerField(null=True)
    image_Season = models.CharField(max_length=50, blank=True)
    
    def newprice(self):
        newprice=float(self.price)
        newprice2="%.2f" % newprice 
        return newprice2
    
    class Meta:
        app_label = ''
        db_table = u'image_content'

class ImageUploadForm(forms.Form):
    type = forms.ChoiceField(choices=(('6', 'Sunday')))

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
 
   
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=450, blank=True)
    category_description = models.TextField(blank=True)
    category_main = models.IntegerField()
    category_parent = models.IntegerField(null=True, blank=True)
    category_header = models.TextField(blank=True)
    category_footer = models.TextField(blank=True)
    category_title = models.TextField(blank=True)
    category_meta = models.TextField(blank=True)
    sorting = models.IntegerField(null=True, blank=True)
    numtolist = models.IntegerField(null=True, blank=True)
    displaytype = models.IntegerField(null=True, blank=True)
    columnum = models.IntegerField(null=True, blank=True)
    iconimage = models.CharField(max_length=300, blank=True)
    special_numtolist = models.IntegerField(null=True, blank=True)
    special_displaytype = models.IntegerField(null=True, blank=True)
    special_columnum = models.IntegerField(null=True, blank=True)
    category_columnum = models.IntegerField(null=True, blank=True)
    category_displaytype = models.IntegerField(null=True, blank=True)
    related_displaytype = models.IntegerField(null=True, blank=True)
    related_columnum = models.IntegerField(null=True, blank=True)
    listing_displaytype = models.IntegerField(null=True, blank=True)
    hide = models.IntegerField(null=True, blank=True)
    category_defaultsorting = models.IntegerField(null=True, blank=True)
    createdby = models.CharField(max_length=150, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    itemicon = models.IntegerField(null=True, blank=True)
    redirectto = models.CharField(max_length=450, blank=True)
    accessgroup = models.CharField(max_length=750, blank=True)
    link = models.TextField(blank=True)
    link_target = models.CharField(max_length=150, blank=True)
    upsellitems_displaytype = models.IntegerField(null=True, blank=True)
    upsellitems_columnum = models.IntegerField(null=True, blank=True)
    filename = models.CharField(max_length=765, blank=True)
    category_country = models.CharField(max_length=20, blank=True)
    isfilter = models.IntegerField(null=True, db_column='isFilter', blank=True) # Field name made lowercase.
    keywords = models.TextField(blank=True)
    parent_lang = models.IntegerField(null=True,)
    class Meta:
        app_label = ''
        db_table = u'category'

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

# Create your models here.
class ImageStore2(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    gs_object_name = models.CharField(max_length=1024)
    content_type = models.CharField(max_length=100)
    creation = models.DateTimeField()
    filename = models.CharField(max_length=1024)
    size = models.IntegerField()
    md5 = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    class Meta:
        db_table = u'imagestore_imagestore'
        app_label = ''
    def imageUrl(self):
        from google.appengine.api import blobstore, images
        imgurl = ""
        try:
            #blob_reader = blobstore.BlobReader(self.gs_object_name)
            #imgurl = images.Image(blob_reader.read())
            logging.info('Key NAme %s \n\n',self.gs_object_name)
            blob_key = blobstore.create_gs_key(self.gs_object_name)
            imgurl=images.get_serving_url(blob_key)
        except Exception, e:
            imgurl=""
        return imgurl
    def fullimageUrl(self):
        from google.appengine.api import blobstore, images
        urlimg=""
        try:
            blob_key = blobstore.create_gs_key(self.gs_object_name)
            urlimg = get_serving_url(blob_key, size=None, crop=False, secure_url=None)
        except Exception, e:
            logging.info('LoginfoMessage ImageID:: %s',self.gs_object_name)
            logging.info('LoginfoMessage error:: %s',e)
            urlimg=""
#        image.execute_transforms(output_encoding=images.JPEG)
#        return image.get_serving_url()
        return urlimg

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






