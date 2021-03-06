from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str, force_text
from django.utils.translation import ugettext_lazy as _
from django import VERSION as django_version

from instajobs.helpers import last_hour, getIP
from instajobs.managers import ActiveJobsManager, TempJobsManager
from django.conf import settings as djobberbase_settings

from django.utils.timezone import now
import datetime
import uuid
import time
import django

from hashlib import md5


class Category(models.Model):
    ''' The Category model, very straight forward. Includes a get_total_jobs
        method that returns the total of jobs with that category.
        The save() method is overriden so it can automatically asign
        a category order in case no one is provided.
    '''
    name = models.CharField('Name', unique=True, max_length=32, blank=False)
    var_name = models.SlugField('Slug', unique=True, max_length=32, blank=False)
    title = models.TextField('Title', blank=True)
    description = models.TextField('Description', blank=True)
    keywords = models.TextField('Keywords', blank=True)
    category_order = models.PositiveIntegerField('Category order',
                                                    unique=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        app_label = 'instajobs'

    def get_total_jobs(self):
        return Job.active.filter(category=self).count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('instajobs:instajobs_job_list_category', [self.var_name])

    def save(self, *args, **kwargs):
        if not self.category_order:
            try:
                self.category_order = Category.objects.\
                                    latest('category_order').category_order + 1
            except Category.DoesNotExist:
                self.category_order = 0
        if not self.var_name:
            self.var_name = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Type(models.Model):
    ''' The Type model, nothing special, just the name and
        var_name fields. Again, the var_name is slugified by the overriden
        save() method in case it's not provided.
    '''
    name = models.CharField('Name', unique=True, max_length=16, blank=False)
    var_name = models.SlugField('Slug', unique=True, max_length=32, blank=False)

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'
        app_label = 'instajobs'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.var_name:
            self.var_name = slugify(self.name)
        super(Type, self).save(*args, **kwargs)


class City(models.Model):
    ''' A model for cities, with a get_total_jobs method to get
        the total of jobs in that city, save() method is overriden
        to slugify name to ascii_name.
    '''
    name = models.CharField('Name', unique=True, max_length=50, blank=False)
    ascii_name = models.SlugField('ASCII Name', unique=True, max_length=50, blank=False)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        app_label = 'instajobs'

    def get_total_jobs(self):
        return Job.active.filter(city=self).count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.ascii_name:
            self.ascii_name = slugify(self.name)
        super(City, self).save(*args, **kwargs)


class Job(models.Model):
    ''' The basic job model.
    '''
    INACTIVE = 0
    TEMPORARY = 1
    ACTIVE = 2
    JOB_STATUS_CHOICES = (
        (INACTIVE, 'Inactive'),
        (TEMPORARY, 'Temporary'),
        (ACTIVE, 'Active')
    )

    category = models.ForeignKey(Category, verbose_name='Category', blank=False, null=True, on_delete=models.SET_NULL)
    jobtype = models.ForeignKey(Type, verbose_name='Job Type', blank=False, null=True, on_delete=models.SET_NULL)
    title = models.CharField(verbose_name='Title', max_length=100, blank=False)
    description = models.TextField('Description', blank=False)
    description_html = models.TextField(editable=False)
    company = models.CharField('Company', max_length=150, blank=False)
    company_slug = models.SlugField(max_length=150,
                                            blank=False, editable=False)
    sender = models.SlugField(max_length=150, default="instajobs",
                                            blank=True, editable=False)
    external_id = models.SlugField(max_length=150, blank=True, editable=False)
    city = models.ForeignKey(City, verbose_name='City', null=True, blank=True, on_delete=models.SET_NULL)
    outside_location = models.CharField('Outside location', max_length=150, blank=True)
    #url of the company
    url = models.URLField(max_length=150, blank=True)
    created_on = models.DateTimeField('Created on', editable=False, \
                                        default=now)
    status = models.IntegerField(choices=JOB_STATUS_CHOICES, default=TEMPORARY)
    views_count = models.IntegerField(editable=False, default=0)
    auth = models.CharField(blank=True, editable=False, max_length=32)
    #url of the job post
    joburl = models.CharField(blank=True, editable=False, max_length=32)
    poster_email = models.EmailField('Poster email', blank=False, help_text='Applications will be sent to this address.')
    apply_online = models.BooleanField(default=True, verbose_name='Allow online applications.',
                                    help_text='If you are unchecking this, then add a description on how to apply online!')
    spotlight = models.BooleanField('Spotlight', default=False)
    objects = models.Manager()
    active = ActiveJobsManager()
    temporary = TempJobsManager()

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        app_label = 'instajobs'

    def __str__(self):
        return self.title

    def get_application_count(self):
        return JobStat.objects.filter(job=self, stat_type='A').count()

    def increment_view_count(self, request):
        lh = last_hour()
        ip = getIP(request)
        hits = JobStat.objects.filter(created_on__range=lh,
                                        ip=ip, stat_type='H', job=self).count()
        if hits < djobberbase_settings.DJOBBERBASE_MAX_VISITS_PER_HOUR:
            self.views_count = self.views_count + 1
            self.save()
            new_hit = JobStat(ip=ip, stat_type='H', job=self)
            new_hit.save()

    def is_active(self):
        return self.status == self.ACTIVE

    def is_temporary(self):
        return self.status == self.TEMPORARY

    def get_status_with_icon(self):
        from django.conf import settings

        image = {
            self.ACTIVE: 'icon-yes.gif',
            self.TEMPORARY: 'icon-unknown.gif',
            self.INACTIVE: 'icon-no.gif',
        }[self.status]

        try:
            # Django 1.2
            admin_media = settings.ADMIN_MEDIA_PREFIX
            icon = '<img src="%(admin_media)simg/admin/%(image)s" alt="%(status)s" /> %(status)s'

        except AttributeError:
            # Django 1.3+
            admin_media = settings.STATIC_URL
            icon = '<img src="%(admin_media)sadmin/img/%(image)s" alt="%(status)s" /> %(status)s'

        else:
            admin_media = ''
            icon = '%(status)s'

        return icon % {'admin_media': admin_media,
                       'image': image,
                       'status': unicode(self.JOB_STATUS_CHOICES[self.status][1])}
    get_status_with_icon.allow_tags = True
    get_status_with_icon.admin_order_field = 'status'
    get_status_with_icon.short_description = 'Status'

    def activate(self):
        self.status = self.ACTIVE
        self.save()

    def deactivate(self):
        self.status = self.INACTIVE
        self.save()

    def email_published_before(self):
        return Job.active.exclude(pk=self.id) \
                          .filter(poster_email=self.poster_email).count() > 0

    def get_edit_url(self):
        return reverse('instajobs:instajobs_job_edit', [self.id, self.auth])

    def get_absolute_url(self):
        return reverse('instajobs:instajobs_job_detail', [self.id, self.joburl])

    def get_activation_url(self):
        return reverse('instajobs:instajobs_job_activate', [self.id, self.auth])

    def get_deactivation_url(self):
        return reverse('instajobs:instajobs_job_deactivate', [self.id, self.auth])

    def clean(self):
        #making sure a job location is selected/typed in
        if self.city:
            self.outside_location = ''
        elif len(self.outside_location.strip()) > 0:
            self.city = None
        else:
            raise ValidationError('You must select or type a job location.')

    def save(self, *args, **kwargs):
        #saving auth code
        if not self.auth:
            self.auth = md5(unicode(self.id) + \
                            unicode(uuid.uuid1()) + \
                            unicode(time.time())).hexdigest()
        #saving company slug
        self.company_slug = slugify(self.company)

        #saving job url
        self.joburl = slugify(self.title) + \
                        '-' + djobberbase_settings.DJOBBERBASE_AT_URL + \
                        '-' + slugify(self.company)

        #saving with textile
        if djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE == 'textile':
            import textile
            self.description_html = mark_safe(
                                        force_text(
                                            textile.textile(
                                                smart_str(self.description))))
        #or markdown
        elif djobberbase_settings.DJOBBERBASE_MARKUP_LANGUAGE == 'markdown':
            import markdown
            self.description_html = mark_safe(
                                        force_text(
                                            markdown.markdown(
                                                smart_str(self.description))))
        else:
            self.description_html = self.description

        super(Job, self).save(*args, **kwargs)


class JobStat(models.Model):
    APPLICATION = 'A'
    HIT = 'H'
    SPAM = 'S'
    STAT_TYPES = (
        (APPLICATION, 'Application'),
        (HIT, 'Hit'),
        (SPAM, 'Spam'),
    )
    job = models.ForeignKey(Job, blank=False, null=True, on_delete=models.SET_NULL)

    created_on = models.DateTimeField(default=now)
    ip = models.GenericIPAddressField()
    stat_type = models.CharField(max_length=1, choices=STAT_TYPES)
    description = models.CharField('Description', max_length=250)

    class Meta:
        verbose_name = 'Job Stat'
        verbose_name_plural = 'Job Stats'

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.stat_type == 'A':
            self.description = 'Job application for [{0}]{1} from IP: {2}'.format( \
                                            (self.job.pk, self.job.title, self.ip))
        elif self.stat_type == 'H':
            self.description = u'Visit for [%d]%s from IP: %s' % \
                                            (self.job.pk, self.job.title, self.ip)
        elif self.stat_type == 'S':
            self.description = u'Spam report for [%d]%s from IP: %s' % \
                                            (self.job.pk, self.job.title, self.ip)
        else:
            self.description = "Unkwown stat"
        super(JobStat, self).save(*args, **kwargs)


class JobSearch(models.Model):
    keywords = models.CharField('Keywords', max_length=100, blank=False)
    created_on = models.DateTimeField('Created on', default=now)

    class Meta:
        verbose_name = 'Search'
        verbose_name_plural = 'Searches'

    def __str__(self):
        return self.keywords
