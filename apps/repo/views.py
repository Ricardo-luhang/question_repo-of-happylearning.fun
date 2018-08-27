from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from apps.repo.models import Category, Questions, Answers, UserLog, AnswersCollection, QuestionsCollection
from django.forms.models import model_to_dict
from django.views.generic import DetailView
import json
from django.core import serializers
from django.db import transaction
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class Question(View):
    def get(self, request):
        category = Category.objects.all().values("id", "name")
        grades = Questions.DIF_CHOICES
        return render(request, 'question.html', {'category': category, 'grades': grades})


class Questiondetail(LoginRequiredMixin, DetailView):
    model = Questions
    template_name = 'question_detail.html'
    # 查询参数
    pk_url_kwarg = 'question_id'

    def post(self, request, question_id):
        try:
            with transaction.atomic():
                # data_answer: 用户提交的数据
                data_answer = request.POST.get('answer', "没有回答")
                new_answer = Answers.objects.get_or_create(question=self.get_object(), user=request.user)
                new_answer[0].answer = data_answer
                new_answer[0].save()
                question = Questions.objects.get(id=question_id)
                question.answer_num += 1
                question.save()
                my_answer = json.loads(serializers.serialize("json", [new_answer[0]]))[0]
                # OPERATE = ((1, "收藏"), (2, "取消收藏"), (3, "回答"))
                # raise  TypeError
                UserLog.objects.create(user=request.user, operate=3, question=self.get_object(), answer=new_answer[0])
                result = {'status': 1, 'msg': '提交成功', 'my_answer': my_answer}
                return JsonResponse(result)
                # todo: 做一些判断=》 提交失败或其他异常情况
        except Exception as ex:
            print('some error')
            return JsonResponse({'status': 0, 'msg': 'some error'})

    def get_context_data(self, **kwargs):
        if self.object:
            kwargs['object'] = self.object
            kwargs['my_answer'] = Answers.objects.filter(question=self.get_object(), user=self.request.user)
            kwargs['other_answer'] = Answers.objects.filter(question=self.get_object())
        return super().get_context_data(**kwargs)


class AnswerView(View):
    def get(self, request, question_id):
        # answer = Questions.objects.get(id=id)
        my_answer = Answers.objects.filter(question=question_id, user=request.user)
        if not my_answer:
            question = {"answer": "请回答后再查看其他答案"}
            return JsonResponse(question, safe=False)

        try:
            # model_to_dict适合Model
            # serializers适合queryset
            # question = model_to_dict(Questions.objects.get(id=id))
            # question = serializers.serialize('json', Questions.objects.filter(id=id))
            # question = serializers.serialize('json', Questions.objects.filter(id=id))
            question = Questions.objects.filter(id=id).values()[0]
        except Exception as ex:
            print(ex)
            question = None
        return JsonResponse(question, safe=False)


class AnswerCollectionView(View):
    def get(self, request, answer_id):
        mes = 'fail'
        user = request.user.id
        is_user = AnswersCollection.objects.filter(answer_id=answer_id, user_id=user)
        if is_user:
            AnswersCollection.objects.filter(answer_id=answer_id, user_id=user).delete()
        else:
            collection = AnswersCollection()
            collection.status = True
            collection.answer_id = answer_id
            collection.user_id = request.user.id
            collection.save()
            mes = 'success'
        collection_num = AnswersCollection.objects.filter(answer_id=answer_id).count()
        wsg = {'mes': mes, 'collection_num': collection_num}
        return JsonResponse(wsg)


class QuestionCollectionView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question = Questions.objects.get(id=question_id)
        print(question_id)
        result = QuestionsCollection.objects.get_or_create(user=request.user, question=question)
        # True表示新创建,False表示老数据
        question_collection = result[0]
        if not result[1]:
            if question_collection.status:
                question_collection.status = False
            else:
                question_collection.status = True
        question_collection.save()
        #
        msg = model_to_dict(question_collection)
        ret_info = {"code": 200, "msg": msg}
        return JsonResponse(ret_info)
