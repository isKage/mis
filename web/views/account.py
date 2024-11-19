"""
用户账户相关：注册、登录、注销
"""
import uuid
import datetime
from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q

from web.forms.account import RegisterModelForm, LoginForm
from web import models
from web_utils.image_code import check_code


def register(request):
    """注册界面"""
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库（密码要是密文）
        # instance = forms.save，会自动存储进数据库，新增的这条数据赋值给instance，且会剔除数据库里没有的数据名
        instance = form.save()

        # 存储后返回url给前端
        return JsonResponse({'status': True, 'data': '/login/'})

    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    """用户名登录"""
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # 不再是 user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        # 而是验证 (手机=username and pwd=pwd) or (邮箱=username and pwd=pwd)
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(username=username)).filter(
            password=password).first()
        if user_object:
            # 登录成功为止
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 5)  # 5天有效
            return redirect('index')

        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    image_object, code = check_code(char_length=4)

    request.session['image_code'] = code  # 将code存到session中
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s

    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')
