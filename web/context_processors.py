from web.models import MembershipRequest


def basic_context_processor(request):
    # 仅登录用户查看消息
    if request.mis.user:
        unread_count = MembershipRequest.objects.filter(status="pending").count()
        return {"unread_count": unread_count}
    return {"unread_count": 0}
