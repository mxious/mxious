from django.conf.urls import url
from . import views

app_name = 'covers'

urlpatterns = [
	url(r'^search', views.search, name='search')
]