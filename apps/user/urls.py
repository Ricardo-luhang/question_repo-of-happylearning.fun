from django.conf.urls import url
from .views import Login, Register
from apps.user.views import Logout


urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
]
