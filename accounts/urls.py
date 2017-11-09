"""debtomator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from . import views
from .views import DebtorView, DebtorTotalListView, DebtorDeleteView, HomeView

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^login', auth_views.login,
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout', auth_views.logout,
        {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^make-debt', DebtorView.as_view(), name='make-debt'),
    url(r'^show', DebtorTotalListView.as_view(), name='show'),
    url(r'^delete/(?P<pk>\d+)', DebtorDeleteView.as_view(), name='delete'),
    url(r'^', HomeView.as_view(), name='home'),
]

urlpatterns += staticfiles_urlpatterns()
