from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
	url(r'^login', views.login, name='login'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^register', views.register, name='register'),
	url(r'^(?P<username>[-\w.]+)/$', views.profile, name='profile')
]