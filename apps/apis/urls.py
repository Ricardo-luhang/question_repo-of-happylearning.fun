from django.conf.urls import url, include
from apps.apis import views
from apps.apis.views import ReferenceAnswer


urlpatterns = [
    url(r'^get_captcha/$', views.get_captcha, name='get_captcha'),
    url(r'^questions/$', views.QuestionsView.as_view(), name='questions'),
    url(r'^answer/(?P<answer_id>\d+)/$', ReferenceAnswer.as_view(), name='answer'),
    url(r'^other_answer/(?P<id>\d+)/$', views.OtherAnswerView.as_view(), name='other_answer'),
    url(r'^get_mobile_captcha/$', views.get_mobile_captcha, name='get_mobile_captcha'),
]
