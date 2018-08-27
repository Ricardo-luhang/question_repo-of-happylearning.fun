from django.conf.urls import url
from apps.usercenter.views import MyCollection, MyAnswer, MyContribute, MyProfile, ChangePasswd, ChangeProfile, UserCenter

urlpatterns = [
    url(r'^$', UserCenter.as_view(), name='usercenter'),
    url(r'^mycollection/$', MyCollection.as_view(), name='mycollection'),
    url(r'^myprofile/$', MyProfile.as_view(), name='myprofile'),
    url(r'^myanswer/$', MyAnswer.as_view(), name='myanswer'),
    url(r'^mycontribute/$', MyContribute.as_view(), name='mycontribute'),
    url(r'^changepwd/$', ChangePasswd.as_view(), name='changepwd'),
    url(r'^changeprofile/$', ChangeProfile.as_view(), name='changeprofile'),

]
