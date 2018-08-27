"""tiku URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from user import views
from django.views.static import serve
from tiku.settings import MEDIA_ROOT
import user
from apps.user.views import Index
from apps.usercenter.views import ChangeAvator


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^apis/', include('apis.urls', namespace='apis')),
    url(r'^repo/', include('repo.urls', namespace='repo')),
    url(r'^center/', include('usercenter.urls', namespace='center')),
    url(r'^change_avator/$', ChangeAvator.as_view(), name='change_avator'),


]
