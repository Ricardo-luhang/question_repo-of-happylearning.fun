from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
import base64
import os
import time
import datetime
from tiku.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import auth
from apps.repo.models import Answers, Questions, Category
from utils.mixin_utils import LoginRequiredMixin


class UserCenter(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')


class MyCollection(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')


class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')


class MyAnswer(LoginRequiredMixin, View):
    def get(self, request):
        myanswer = Answers.objects.filter(user=request.user)
        return render(request, 'uc_answer.html', {'my_answers': myanswer})


class MyContribute(LoginRequiredMixin, View):
    def get(self, request):
        search_key = request.GET.get("search", '')
        category = Category.objects.all().values("id", "name")
        grades = Questions.DIF_CHOICES
        kwgs = {"category": category, "grades": grades, "search_key": search_key}
        return render(request, 'question.html', kwgs)

    def post(self, request):
        try:
            title = request.POST.get("title")
            category = request.POST.get("category")
            if category == 0:
                category = None
            content = request.POST.get('content')
            Questions.objects.create(title=title, category_id=category, content=content, contributor=request.user)
        except Exception as ex:
            return HttpResponse('提交失败' + ex)
        return HttpResponse("提交成功")


class ChangeAvator(LoginRequiredMixin, View):
    def post(self, request):
        today = datetime.date.today().strftime("%Y%m%d")
        # 图片的data-img格式
        img_src_str = request.POST.get("image")
        img_str = img_src_str.split(',')[1]
        # 取出格式
        img_type = img_src_str.split(';')[0].split('/')[1]
        # 取出数据
        img_data = base64.b64decode(img_str)
        # 相对上传路径
        avator_path = os.path.join("avator", today)
        # 绝对上传路径
        avator_path_full = os.path.join(MEDIA_ROOT, avator_path)
        if not os.path.exists(avator_path_full):
            os.mkdir(avator_path_full)
        filename = str(time.time()) + "." + img_type
        # 绝对文件路径，用于保存图片
        filename_full = os.path.join(avator_path_full, filename)
        # 相对MEDIA_URL路径，用于展示数据
        img_url = f"{MEDIA_URL}{avator_path}/{filename}"
        try:
            with open(filename_full, 'wb') as fp:
                fp.write(img_data)
            ret = {
                "result": "ok",
                "file": img_url
            }
        except Exception as ex:
            ret = {
                "result": "error",
                "file": "upload fail"
            }
        request.user.avator = os.path.join(avator_path, filename)
        request.user.save()
        return JsonResponse(ret)


class ChangePasswd(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_change_passwd.html')

    def post(self, request):
        old_passwd = request.POST.get('old_passwd', '')
        new_passwd = request.POST.get('new_passwd', '')
        new_passwd1 = request.POST.get('new_passwd1', '')

        if new_passwd != new_passwd:
            ret_mes = {'code': 400, 'mes': '两次输入的密码不正确！'}
        else:
            user = auth.authenticate(username=request.user.username, password=old_passwd)
            if user:
                user.set_password(new_passwd1)
                user.save()
                auth.logout(request)
                ret_mes = {'code': 200, 'mes': '密码修改成功'}
            else:
                ret_mes = {'code': 400, 'mes': '密码不正确'}
        return render(request, 'user_change_passwd.html', {'ret_mes': ret_mes})


class ChangeProfile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')

    def post(self, request):
        username = request.POST.get('username', '')
        telphone = request.POST.get('telphone', '')
        return render(request, 'profile.html')
