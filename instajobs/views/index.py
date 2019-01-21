from django.shortcuts import get_object_or_404, redirect, render
from instajobs.models import Job, Category, Type, JobStat, JobSearch, City
from django.conf import settings as djobberbase_settings
from django.db.models import Count
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

def index(request):
	return render(request, 'instajobs/index.html', {"title": "Welcome to Instajobs"})
