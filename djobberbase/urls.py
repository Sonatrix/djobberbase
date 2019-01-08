# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.urls import path, re_path
from djobberbase.models import Job, Category, Type, City
from djobberbase.conf import settings as djobberbase_settings
from djobberbase.feeds import LatestJobsFeed

if djobberbase_settings.DJOBBERBASE_CAPTCHA_POST == 'simple':
    from djobberbase.forms import CaptchaJobForm
    form_class = CaptchaJobForm
else:
    from djobberbase.forms import JobForm
    form_class = JobForm

app_name = 'djobberbase'

urlpatterns = [

    #An index view
    re_path(r'^$',
        'list_detail.object_list', 
        { 'queryset': Job.active.all(),          
          'extra_context': {'page_type': 'index'},
          'paginate_by': djobberbase_settings.DJOBBERBASE_JOBS_PER_PAGE},
        name='djobberbase_job_list'),
    
    #Cities view    
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_CITIES_URL+'/$',
        'list_detail.object_list', 
        { 'queryset': City.objects.all(),
          'extra_context': {'page_type': 'cities', 
                    'other_cities_total': Job.active.filter(city=None).count}},
        name='djobberbase_cities_list'),

    #post new job
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_POST_URL+'/$',
        'create_update.create_object', 
        { 'form_class': form_class, 
          'post_save_redirect': '../'+
          djobberbase_settings.DJOBBERBASE_VERIFY_URL+'/%(id)d/%(auth)s/'},
        name='djobberbase_job_post'),

    #job unavailable
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_UNAVAILABLE_URL+'/$',
        'simple.direct_to_template', 
        {'template': 'djobberbase/unavailable.html'},
        name='djobberbase_job_unavailable'),
]

urlpatterns += [

    #verify job
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_VERIFY_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_verify', 
        name='djobberbase_job_verify'),

    #all jobs
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_URL+'/$',
        'djobberbase.views.jobs_category',
        name='djobberbase_job_list_all'),

    #all jobs with category
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_URL+
        '/(?P<cvar_name>[-\w]+)/$',
        'djobberbase.views.jobs_category',
        name='djobberbase_job_list_category'),

    #all jobs with category and job type    
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_URL+
        '/(?P<cvar_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'djobberbase.views.jobs_category',
        name='djobberbase_job_list_category_type'),

    #Job detail    
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOB_URL+
        '/(?P<job_id>\d+)/(?P<joburl>[-\w]+)/$',
        'djobberbase.views.job_detail',
        name='djobberbase_job_detail'),
        
    #Jobs in city view
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_IN_URL+
        '/(?P<city_name>[-\w]+)/$',
        'djobberbase.views.jobs_in_city',
        name='djobberbase_jobs_in_city'),

    #Jobs in other cities
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_IN_OTHER_CITIES+'/$',
        'djobberbase.views.jobs_in_other_cities',
        name='djobberbase_jobs_in_other_cities'),

    #Jobs in city+jobtype view
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_IN_URL+
        '/(?P<city_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'djobberbase.views.jobs_in_city',
        name='djobberbase_jobs_in_city_jobtype'),

    #Companies
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_COMPANIES_URL+'/$',
        'djobberbase.views.companies',
        name='djobberbase_companies'),

    #Jobs at (company)
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_JOBS_AT_URL+
        '/(?P<company_slug>[-\w]+)/$',
        'djobberbase.views.jobs_at',
        name='djobberbase_jobs_at'),

    #Job confirm
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_CONFIRM_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_confirm',
        name='djobberbase_job_confirm'),

    #Edit job
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_POST_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_edit',
        name='djobberbase_job_edit'),

    #Activate job
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_ACTIVATE_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_activate',
        name='djobberbase_job_activate'),

    #Deactivate job
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_DEACTIVATE_URL+
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'djobberbase.views.job_deactivate',
        name='djobberbase_job_deactivate'),

    #Search
    re_path(r'^'+djobberbase_settings.DJOBBERBASE_SEARCH_URL+'/$',
        'djobberbase.views.job_search',
        name='djobberbase_job_search'),

    #Feed
    re_path(r'^rss/(?P<var_name>[-\w]+)/$',
        LatestJobsFeed(),
        name='djobberbase_feed'),

]
