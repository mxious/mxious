"""mxious URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from pages.views import HomeView
from accounts.views import profile
from accounts.decorators import AnonymousRequired
from posts.views import dashboard

urlpatterns = [
    # Special, non-local urls begin
	url(r'^$', AnonymousRequired(HomeView.as_view()), name='home'),
    url(r'^dashboard', dashboard, name='dashboard'),
    # App specific URLs begin
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^posts/', include('posts.urls')),
    # Low priority uris here (prevents accidental overrides)
]
