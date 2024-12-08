from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.models import Preference
from web import models
from web.forms.prefer import PreferenceForm
from web_utils.kimi import partner


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


@csrf_exempt
def recommend_partner(request):
    # 获取当前用户的用户名
    user_name = request.mis.user.username

    if request.method == 'POST':
        # 调用 partner 函数获取推荐结果
        recommended_partners = partner(user_name)

        # 将推荐结果保存到数据库中
        user_preference = Preference.objects.get(userid__username=user_name)
        user_preference.recommendation_text = recommended_partners  # 存储推荐结果
        user_preference.save()  # 保存到数据库

        # 将推荐结果传递到模板中并返回页面
        return render(request, 'recommend_partner.html', {'recommended_partners': recommended_partners})

    # 如果没有提交 POST 请求，获取当前用户的推荐结果
    try:
        user_preference = Preference.objects.get(userid__username=user_name)
        recommended_partners = user_preference.recommendation_text if user_preference.recommendation_text else "尚未生成推荐"
    except Preference.DoesNotExist:
        recommended_partners = "没有找到偏好信息"

    # 渲染模板并返回结果
    return render(request, 'recommend_partner.html', {'recommended_partners': recommended_partners})
