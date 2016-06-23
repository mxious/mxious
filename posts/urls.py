from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
	url(r'^load_more', views.load_more, name='load_more'),
	url(r'^poll', views.poll, name='poll')
]