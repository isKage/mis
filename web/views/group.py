from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from web.models import Group, Event, MembershipRequest
from django.contrib.auth.decorators import login_required
from django.http import Http404


def group_list(request):
    groups = Group.objects.all().order_by('-created_at')
    return render(request, 'group_list.html', {'groups': groups})


def group_add(request):
    if request.method == "POST":
        # 获取请求数据并创建小组
        group_name = request.POST.get("group_name")
        description = request.POST.get("description")
        topic_id = request.POST.get("topic_id")

        # 处理空话题的情况
        topic = None
        if topic_id:
            try:
                topic = Event.objects.get(id=topic_id)
            except Event.DoesNotExist:
                raise Http404("话题不存在")

        # 创建小组
        group = Group.objects.create(
            group_name=group_name,
            description=description,
            creator=request.mis.user,
            topic=topic,
        )
        return redirect("group_list")

    # 渲染创建小组的页面
    events = Event.objects.filter(initiator=request.mis.user)
    return render(request, "group_add.html", {"events": events})


def group_join_request(request, group_id):
    if request.method == "POST":
        reason = request.POST.get("reason")
        group = get_object_or_404(Group, id=group_id)
        MembershipRequest.objects.create(
            group=group, applicant=request.mis.user, reason=reason
        )
        # return JsonResponse({"message": "申请已发送！"})
        return redirect('group_list')
    return JsonResponse({"error": "无效请求"}, status=400)


def membership_requests(request):
    # 当前用户作为小组创建者的申请记录
    managed_groups = Group.objects.filter(creator=request.mis.user)
    requests_to_manage = MembershipRequest.objects.filter(group__in=managed_groups).order_by('-created_at')

    # 当前用户作为申请者的申请记录
    user_requests = MembershipRequest.objects.filter(applicant=request.mis.user).order_by('-created_at')

    return render(request, 'notice.html', {
        'requests_to_manage': requests_to_manage,
        'user_requests': user_requests,
    })


def approve_request(request, request_id):
    # 获取申请对象
    req = get_object_or_404(MembershipRequest, id=request_id)

    # 确认当前用户是否为小组创建者
    if req.group.creator != request.mis.user:
        return JsonResponse({"error": "无权限操作此申请"}, status=403)

    # 通过 URL 参数获取操作类型
    action = request.GET.get('action', 'approve')
    if action == 'approve':
        req.status = 'approved'
        req.group.members.add(req.applicant)  # 将申请人加入小组
    elif action == 'reject':
        req.status = 'rejected'
    else:
        return JsonResponse({"error": "无效的操作"}, status=400)

    req.save()
    return redirect('membership_requests')


def delete_group(request, group_id):
    # 获取目标小组
    group = get_object_or_404(Group, id=group_id)

    # 确认当前用户是小组的创建者
    if group.creator != request.mis.user:
        return JsonResponse({"error": "您没有权限删除此小组"}, status=403)

    # 删除小组
    group.delete()
    return redirect('group_list')  # 跳转到小组列表页面


def group_leave(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # 确保当前用户是小组的成员
    if request.mis.user in group.members.all():
        group.members.remove(request.mis.user)  # 从小组成员列表中移除当前用户

    return redirect('group_list')  # 重定向到小组列表页面（根据你的 URL 配置）
