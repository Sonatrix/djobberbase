from django.urls import path, include
from instajobs.views.index import index
app_name = 'instajobs'

urlpatterns = [
    path('', index, name="home"),
]