"""picapprove URL Configuration

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
from pic import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^pic/(?P<vid>\d+)/$',views.picDetail, name='picDetail'),
    url(r'^login/$', views.logIn, name="login"),
    url(r'^logout/$', views.logOut, name="logout"),
    url('data_fresh/(?P<vid>\d+)', views.data_fresh, name="data_fresh"),
    url(r'^media/(?P<vid>\d+)', views.file_down, name="download"),
    url(r'^search/$', views.search, name="search"),
    url(r'^get_search_data/$', views.get_search_data, name="get_search_data"),
    url(r'^upload/$', views.upload_main, name="upload_main"),
    url(r'^up_search_companyname/$', views.upload_search_companyname, name="upload_search_companyname"),
    url(r'^testurl/$', views.testurl, name="testurl"),
    url(r'^admin/', admin.site.urls),
]
