from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.models import Preference
from web import models
from web.forms.prefer import PreferenceForm


@csrf_exempt
def preference_view(request):
    user = request.mis.user  # 从中间件获取当前用户
    if not user:
        return redirect('login.html')  # 未登录跳转到登录页面

    # 查询当前用户的偏好数据
    preference = Preference.objects.filter(userid=user).first()

    if request.method == 'POST':
        if preference:
            form = PreferenceForm(request.POST, instance=preference)  # 更新记录
        else:
            form = PreferenceForm(request.POST)  # 创建新记录

        if form.is_valid():
            obj = form.save(commit=False)
            obj.userid = user
            obj.save()
            return render(request, 'prefer.html', {
                'form': form,
                'success_message': 'Preferences saved successfully!',
            })
        else:
            return render(request, 'prefer.html', {
                'form': form,
                'error_message': 'Please correct the errors below.',
            })

    # GET 请求加载表单
    form = PreferenceForm(instance=preference) if preference else PreferenceForm()
    return render(request, 'prefer.html', {'form': form})
