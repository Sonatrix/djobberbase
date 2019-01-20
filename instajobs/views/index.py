from django.shortcuts import get_object_or_404, redirect, render_to_response
from djobberbase.models import Job, Category, Type, JobStat, JobSearch, City
from djobberbase.postman import *
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from djobberbase.helpers import *
from djobberbase.forms import ApplicationForm, JobForm
from djobberbase.conf import settings as djobberbase_settings
from django.db.models import Count
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.utils import timezone