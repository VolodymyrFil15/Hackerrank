from django.conf.urls import url
from django.contrib.auth.urls import *
from . import views

app_name = 'Tasks'

urlpatterns = [
    url(r'^$', views.domains_list, name='index'),
    url(r'^registration/$', views.UserFormView.as_view(), name='registration'),
    url(r'^(?P<domain_name>[a-zA-Z0-9]+)/(?P<subdomain_name>[a-zA-Z]*)/$', views.challenges, name='challenges_list'),
    url(r'^(?P<domain_name>[a-zA-Z0-9]+)/(?P<subdomain_name>[a-zA-Z]*)/(?P<challenge_name>[\w|\W]*)/$',
        views.challenge, name='challenges_list1'),
    # url(r'login/$', views.login_view, name = 'login'),
    # url(r'logout/$', views.logout_view, name = 'logout'),
    url(r'^(?P<domain_name>[a-zA-Z0-9]+)/(?P<subdomain_name>)', views.challenges, name='domain'),
]
