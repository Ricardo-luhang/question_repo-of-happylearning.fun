from django.conf.urls import url
from apps.repo.views import Question, Questiondetail
from apps.repo.views import AnswerCollectionView, QuestionCollectionView

urlpatterns = [
    url(r'^question/$', Question.as_view(), name='question'),
    url(r'^question_detail/(?P<question_id>\d+)/$', Questiondetail.as_view(), name='question_detail'),
    url(r'^answer/collection/(?P<answer_id>\d+)/$', AnswerCollectionView.as_view(), name='answer_collection'),
    url(r'^question/collection/(?P<question_id>\d+)/$', QuestionCollectionView.as_view(), name='question_collection'),
]
