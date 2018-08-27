from django.shortcuts import HttpResponse
from io import BytesIO
import base64
from apps.lib import patcha
from django.http import JsonResponse
from django.views.generic import View
from apps.repo.models import Questions
from django.db.models import Q
from apps.repo.models import Answers, AnswersCollection
from django.template import loader
import logging
from apps.user.models import User

logger = logging.getLogger('captcha')


# Create your views here.


def get_captcha(request):
    # 直接在内存开辟一点空间存放临时生成的图片
    f = BytesIO()
    # 调用check_code生成照片和验证码
    img, code = patcha.create_validate_code()
    # 将验证码存在服务器的session中，用于校验
    request.session['captcha_code'] = code
    # 生成的图片放置于开辟的内存中
    img.save(f, 'PNG')
    # 将内存的数据读取出来，并以HttpResponse返回
    # return HttpResponse(f.getvalue())
    ret_type = "data:image/jpg;base64,".encode()
    ret = ret_type + base64.encodebytes(f.getvalue())
    del f
    return HttpResponse(ret)


def get_mobile_captcha(request):
    ret = {"code": 200, "msg": "验证码发送成功！"}
    try:
        mobile = request.GET.get("mobile")
        Mobile = User.objects.filter(mobile=mobile)
        if Mobile:
            ret = {"code": 400, "msg": "该手机号已绑定"}
            return JsonResponse(ret)
        if mobile is None: raise ValueError("手机号不能为空！")
        import random
        mobile_captcha = "".join(random.choices('0123456789', k=6))
        from django.core.cache import cache
        # 将短信验证码写入redis
        cache.set(mobile, int(mobile_captcha), 300)
        if not sms.send_sms(mobile, mobile_captcha):
            raise ValueError('发送短信失败')
    except Exception as ex:
        ret = {"code": 400, "msg": "验证码发送失败！"}
    return JsonResponse(ret)


class QuestionsView(View):
    def get(self, request):
        page = int(request.GET.get("page", 1))
        pagesize = int(request.GET.get("pagesize", 20))
        offset = int(request.GET.get("offset", 0))
        grade = int(request.GET.get("grade", 0))
        status = int(request.GET.get("status", 2))
        # 2: 不筛选， 1，已刷，0，待刷
        if status == 1:
            status = True
        elif status == 0:
            status = False
        category = int(request.GET.get("category", 0))
        search = request.GET.get("search", 0)
        questions_list = Questions.objects.all()
        if search:
            if search.isdigit():
                questions_list = questions_list.filter(
                    Q(id=search) | Q(content__icontains=search) | Q(title__icontains=search))
            else:
                questions_list = questions_list.filter(Q(content__icontains=search) | Q(title__icontains=search))
        if grade: questions_list = questions_list.filter(grade=grade)
        if category: questions_list = questions_list.filter(category__id=category)
        if status != 2: questions_list = questions_list.filter(status=status)
        total = len(questions_list)
        # func1(返回页器对象)
        # questions_list = list(Paginator(questions_list, per_page=pagesize).page(page).object_list)


        # # func2
        questions_list = list(questions_list.values('id', 'title', 'grade', 'answer')[offset:offset + pagesize])

        # 格式是bootstrap-table要求的格式
        questions_dict = {'total': total, 'rows': questions_list}
        return JsonResponse(questions_dict, safe=False)


class ReferenceAnswer(View):
    def get(self, request, answer_id):
        my_answer = Answers.objects.filter(question=answer_id, user=request.user)
        if not my_answer:
            html = "请回答后再查看其他答案"
            return HttpResponse(html)
        reference_answer = Answers.objects.filter(question=answer_id)
        if reference_answer:
            html = loader.get_template('question_reference_answer.html').render({"reference_answer": reference_answer})
        else:
            html = "暂无回答"
        return HttpResponse(html)


class OtherAnswerView(View):
    def get(self, request, id):
        # other_answer = list(Answers.objects.filter(question=id).values())
        # other_answer = serializers.serialize('json', Answers.objects.filter(question=id))
        # return JsonResponse(other_answer, safe=False)

        my_answer = Answers.objects.filter(question=id, user=request.user)
        if not my_answer:
            html = "请回答后再查看其他答案"
            return HttpResponse(html)

        # other_answer = Answers.objects.filter(question=id).exclude(user=request.user)
        other_answer = Answers.objects.filter(question=id)
        if other_answer:
            for answer in other_answer:
                if AnswersCollection.objects.filter(answer=answer, user=request.user, status=True):
                    answer.collect_status = 1
                # answer.collect_nums = answer.answers_collection_set.filter(status=True).count()
            # html = loader.render_to_string('question_detail_other_answer.html', {"other_answer": other_answer})
            html = loader.get_template('question_detail_other_answer.html').render({"other_answer": other_answer})
        else:
            html = "暂无回答"
        return HttpResponse(html)







