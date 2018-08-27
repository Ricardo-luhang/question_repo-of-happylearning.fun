from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import auth
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin
import logging
from django.views.generic import View
from .forms import LoginForm, RegisterForm
from apps.repo.models import Answers, Questions
from apps.user.models import User
from django.db.models import Count
from apps.lib.repo_data import user_answer_data
from django.contrib.auth.hashers import make_password
from django.core.cache import cache

logger = logging.getLogger('account')


# Create your views here.


class Index(LoginRequiredMixin, View):
    def get(self, request):
        answers = Answers.objects.filter(user_id=request.user.id).count()
        question_num = Questions.objects.all().count()
        recent_answer = Answers.objects.all()[:10]
        hot_questions = Questions.objects.order_by('-answer_num')[:5]
        hot_user = Answers.objects.hot_user()
        result = Answers.objects.values_list('user').annotate(Count('id'))
        user_id_list = [item[0] for item in result][-10:]
        userlist = User.objects.filter(id__in=user_id_list)
        kwsg = {
            'answers': answers,
            'question_num': question_num,
            'recent_answer': recent_answer,
            'hot_question': hot_questions,
            'hot_user': hot_user,
            'userlist': userlist,
            'user_data': user_answer_data(request.user)
        }
        return render(request, 'index.html', kwsg)


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {'form': form})

    # Ajax提交表单
    def post(self, request):
        ret = {"status": 400, "msg": "调用方式错误"}
        if request.is_ajax():
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                mobile = form.cleaned_data["mobile"]
                mobile_captcha = form.cleaned_data["mobile_captcha"]
                mobile_captcha_reids = str(cache.get(mobile))
                if mobile_captcha == mobile_captcha_reids:
                    user = User.objects.create(username=username, password=make_password(password), mobile=mobile)
                    user.save()
                    ret['status'] = 200
                    ret['msg'] = "注册成功"
                    logger.debug(f"新用户{user}注册成功！")
                    user = auth.authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        auth.login(request, user)
                        logger.debug(f"新用户{user}登录成功")
                    else:
                        logger.error(f"新用户{user}登录失败")
                else:
                    # 验证码错误
                    ret['status'] = 401
                    ret['msg'] = "验证码错误或过期"
            else:
                ret['status'] = 402
                ret['msg'] = form.errors
        logger.debug(f"用户注册结果：{ret}")
        print(ret)
        return JsonResponse(ret)


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        form = LoginForm()
        # request.session["next"] = request.GET.get('next', reverse('index'))
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        captcha = request.POST.get('captcha')
        print(captcha, type(captcha))
        session_captcha_code = request.session['captcha_code']
        print(session_captcha_code, type(session_captcha_code))
        if captcha.lower() == session_captcha_code.lower():
            # 验证码正确
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                logger.error(f"{username}登录成功")
                # 跳转到next
                # return redirect(request.session["next"])
                return HttpResponseRedirect(reverse('index'))
            msg = "用户名或密码错误"
            logger.error(f"{username}登录失败")
        else:
            msg = "验证码错误"
            logger.error(f"{username}验证码错误")
        return render(request, "login.html", {"form": form, "msg": msg})


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logger.debug(f'{request.user}退出系统!')
        auth.logout(request)
        return redirect(reverse('user:login'))
