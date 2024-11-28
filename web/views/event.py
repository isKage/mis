from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.models import Event, UserInfo


def event_list(request):
    # GET 请求时加载创建话题页面
    events = Event.objects.all()
    # 将 events 传递给模板
    return render(request, 'event.html', {'events': events})


@csrf_exempt
def event_add(request):
    user = request.mis.user  # 从中间件获取当前用户
    if not user:
        return redirect('login.html')  # 未登录跳转到登录页面

    # 查询当前用户的偏好数据
    if request.method == "POST":
        topic_name = request.POST.get("topic_name")
        topic_description = request.POST.get("topic_description")
        topic_type = request.POST.get("topic_type")
        invited_members = request.POST.get("invited_members", "")
        # 获取当前用户作为发起者
        initiator = user

        # 如果邀请成员为空，直接设置为空列表
        if invited_members.strip() == "":
            invited_ids = []
        else:
            # 解析被邀请的成员（按用户名查找用户ID）
            invited_ids = []
            usernames = [username.strip() for username in invited_members.split(",") if username.strip()]
            for username in usernames:
                try:
                    # 查找用户名对应的用户
                    user_obj = UserInfo.objects.get(username=username)
                    invited_ids.append(user_obj.id)
                except UserInfo.DoesNotExist:
                    pass

        participants_count = len(invited_ids) + 1  # 加上发起者自己

        # 创建新事件
        event = Event.objects.create(
            topic_name=topic_name,
            topic_description=topic_description,
            initiator=initiator,
            topic_type=topic_type,
            participants=participants_count,
        )
        return redirect('event_list')

    # GET 请求时加载创建话题页面
    events = Event.objects.all()
    # 将 events 传递给模板
    return render(request, 'event.html', {'events': events})
